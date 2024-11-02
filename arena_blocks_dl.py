import os
import requests
from urllib.parse import urlparse
import sys
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn

console = Console()

def extract_block_id(url):
    try:
        return url.rstrip('/').split('/')[-1]
    except IndexError:
        return None

def construct_api_url(block_id):
    return f"https://api.are.na/v2/blocks/{block_id}"

def get_block_class(json_data):
    return json_data.get('class', None)

def get_image_url(json_data):
    try:
        return json_data['image']['original']['url']
    except KeyError:
        return None

def get_link_url(json_data):
    try:
        return json_data['source']['url']
    except KeyError:
        return None

def get_attachment_url(json_data):
    try:
        return json_data['attachment']['url']
    except KeyError:
        return None

def download_file(file_url, save_dir, block_id, file_type, progress, task_id):
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        parsed_url = urlparse(file_url)
        file_name = os.path.basename(parsed_url.path).split('?')[0]
        file_name = f"{block_id}_{file_name}"
        save_path = os.path.join(save_dir, file_name)
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        console.print(f"[bold green]{file_type} downloaded:[/bold green] {file_name}")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error downloading {file_type} from '{file_url}':[/bold red] {e}")

def save_webloc(link_url, save_dir, block_id):
    webloc_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>URL</key>
    <string>{link_url}</string>
</dict>
</plist>
"""
    try:
        webloc_name = f"{block_id}.webloc"
        save_path = os.path.join(save_dir, webloc_name)
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(webloc_content)
        console.print(f"[bold blue]Link saved:[/bold blue] {webloc_name}")
    except IOError as e:
        console.print(f"[bold red]Error saving .webloc file for block {block_id}:[/bold red] {e}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lst_path = os.path.join(script_dir, 'lst.txt')
    images_dir = os.path.join(script_dir, 'images')
    links_dir = os.path.join(script_dir, 'links')
    attachments_dir = os.path.join(script_dir, 'attachments')
    
    for directory in [images_dir, links_dir, attachments_dir]:
        os.makedirs(directory, exist_ok=True)
    
    if not os.path.isfile(lst_path):
        console.print(f"[bold red]Error:[/bold red] The file 'lst.txt' does not exist in {script_dir}.")
        sys.exit(1)
    
    with open(lst_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    
    if not urls:
        console.print(f"[bold red]Error:[/bold red] The file 'lst.txt' is empty.")
        sys.exit(1)
    
    total_urls = len(urls)
    unsupported_blocks = []
    
    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40, style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[bold cyan]Processing Blocks...", total=total_urls)
        
        for url in urls:
            block_id = extract_block_id(url)
            if not block_id:
                console.print(f"[bold red]Error:[/bold red] Invalid URL format: {url}")
                unsupported_blocks.append({'block_id': 'N/A', 'class': 'Invalid URL'})
                progress.advance(task)
                continue
            
            api_url = construct_api_url(block_id)
            
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                json_data = response.json()
            except requests.exceptions.RequestException as e:
                console.print(f"[bold red]Error querying API for block {block_id}:[/bold red] {e}")
                unsupported_blocks.append({'block_id': block_id, 'class': 'API Request Error'})
                progress.advance(task)
                continue
            except ValueError:
                console.print(f"[bold red]Error:[/bold red] Invalid JSON response for block {block_id}.")
                unsupported_blocks.append({'block_id': block_id, 'class': 'Invalid JSON'})
                progress.advance(task)
                continue
            
            block_class = get_block_class(json_data)
            if not block_class:
                console.print(f"[bold red]Error:[/bold red] Class not found for block {block_id}.")
                unsupported_blocks.append({'block_id': block_id, 'class': 'Class Not Specified'})
                progress.advance(task)
                continue
            
            if block_class == "Image":
                image_url = get_image_url(json_data)
                if image_url:
                    download_file(image_url, images_dir, block_id, "Image", progress, task)
                else:
                    console.print(f"[bold red]Error:[/bold red] No image URL found for block {block_id}.")
                    unsupported_blocks.append({'block_id': block_id, 'class': block_class})
            
            elif block_class == "Link":
                link_url = get_link_url(json_data)
                if link_url:
                    save_webloc(link_url, links_dir, block_id)
                else:
                    console.print(f"[bold red]Error:[/bold red] No link URL found for block {block_id}.")
                    unsupported_blocks.append({'block_id': block_id, 'class': block_class})
            
            elif block_class == "Attachment":
                attachment_url = get_attachment_url(json_data)
                if attachment_url:
                    download_file(attachment_url, attachments_dir, block_id, "Attachment", progress, task)
                else:
                    console.print(f"[bold red]Error:[/bold red] No attachment URL found for block {block_id}.")
                    unsupported_blocks.append({'block_id': block_id, 'class': block_class})
            
            else:
                console.print(f"[bold red]Error:[/bold red] Unsupported class '{block_class}' for block {block_id}.")
                unsupported_blocks.append({'block_id': block_id, 'class': block_class})
            
            progress.advance(task)
    
    if unsupported_blocks:
        console.print("\n[bold magenta]Unsupported Blocks:[/bold magenta]")
        for block in unsupported_blocks:
            console.print(f"Block ID: {block['block_id']} | Class: {block['class']}")
    else:
        console.print("\n[bold green]All blocks were processed successfully.[/bold green]")
    
    console.print("\n[bold green]Download process completed successfully.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Process interrupted by user.[/bold red]")
        sys.exit(0)
