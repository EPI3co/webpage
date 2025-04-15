# Webpage Downloader

A tool for downloading and processing web pages while preserving their structure and modifying links for offline viewing.

## Features

- Download complete web pages with their assets
- Process HTML content to modify links for offline viewing
- Copy directory structures while preserving file metadata
- Replace URLs in downloaded content with custom domains
- Clean up "powered by" scripts from downloaded content

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/webpage-downloader.git
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from main import process_html_content, copy_directory_contents
import os
from urllib.parse import urlparse

# Download and process a webpage
url = urlparse("https://example.com")
params = {
    "download_url": "https://example.com",
    "replace_url": "local-example"
}

# Process HTML content
processed_content, links = process_html_content(url, html_content, "utf-8")

# Save processed content to file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(processed_content)

# Copy assets
source_dir = "downloaded_assets"
target_dir = "processed_assets"
os.makedirs(target_dir, exist_ok=True)
copy_directory_contents(source_dir, target_dir)
```

### Configuration Options

- `download_url`: The original URL of the website being downloaded
- `replace_url`: The URL to replace the original with (for offline viewing)

## How It Works

1. The tool downloads web pages and their assets
2. It processes HTML content using BeautifulSoup to:
   - Identify and collect all links within the same domain
   - Modify links to point to the local/replacement domain
   - Remove "powered by" scripts
   - Replace occurrences of the original domain with the replacement domain
3. It preserves the directory structure of the website

## Requirements

- Python 3.11+
- BeautifulSoup4
- Other dependencies listed in requirements.txt

## License

[MIT License](LICENSE)
