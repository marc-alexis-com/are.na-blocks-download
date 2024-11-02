# Are.na Blocks Downloader

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

## Description

Are.na Blocks Downloader is a Python script designed to automate the downloading of various types of blocks from [Are.na](https://www.are.na/). It supports downloading images, saving links as `.webloc` files, and downloading attachments. The script reads a list of Are.na block URLs from a text file and processes each block accordingly, organizing the downloaded content into designated folders.

## Features

- **Automated Downloading**: Easily download images, links, and attachments from Are.na blocks.
- **Organized Storage**: Downloads are saved into `images/`, `links/`, and `attachments/` folders respectively.
- **Error Handling**: Provides clear error messages for unsupported block types or download failures.
- **Progress Tracking**: Displays a real-time progress bar to monitor the download status.
- **User-Friendly Interface**: Utilizes the `rich` library for aesthetically pleasing terminal output.

## Installation

1. **Clone the Repository** (or download the script directly):

    ```bash
    git clone https://github.com/marc-alexis-com/arena-blocks-downloader.git
    cd arena-blocks-downloader
    ```

2. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    Ensure you have `pip` installed. Then run:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare the List of Are.na Blocks**:

    - Create a `lst.txt` file in the root directory of the project.
    - Add one Are.na block URL per line. For example:

        ```
        https://www.are.na/block/23064577
        https://www.are.na/block/5906305
        ```

2. **Run the Script**:

    ```bash
    python arena_blocks_dl.py
    ```

    - The script will automatically create three folders in the same directory as the script:
        - `images/`: Stores downloaded images.
        - `links/`: Stores `.webloc` files for links.
        - `attachments/`: Stores downloaded attachments.

3. **Monitor the Progress**:

    - The terminal will display a progress bar indicating the download status.
    - Upon completion, a summary of the downloads and any unsupported blocks will be displayed

## Limitations

- **Supported Block Types**:
    - **Image**: Downloads images associated with the block.
    - **Link**: Saves links as `.webloc` files.
    - **Attachment**: Downloads attachments associated with the block.
- **Unsupported Block Types**: The script currently does not support other block types such as `Text` or `Media`. Attempting to process these will result in an error message indicating the unsupported class.
- **Platform Specificity**:
    - `.webloc` files are specific to macOS. Users on other operating systems may need to use alternative formats (e.g., `.url` for Windows).
- **Error Handling**:
    - The script handles basic errors such as invalid URLs and failed downloads but may not cover all edge cases.
- **Rate Limiting**:
    - Excessive requests to the Are.na API may result in rate limiting. Users should avoid processing large numbers of blocks in a short period.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under no license; thx
