import requests
from bs4 import BeautifulSoup
import os

# URL of the web page to scrape
url = "https://www.cnn.com/"

# Send a GET request to the URL and retrieve the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Directory to save downloaded images
download_dir = "downloaded_images"
os.makedirs(download_dir, exist_ok=True)

# Search for div, a, and span elements with background images
for element in soup.find_all(['div', 'a', 'span']):
    # Get the background-image CSS property
    bg_style = element.get('style')
    if bg_style:
        bg = bg_style.replace('background-image:', '').replace('url(', '').replace(')', '').replace('"', '').strip()

        # Skip elements with invalid or 'none' background images
        if not bg or bg == 'none':
            continue

        # Extract the background image URL
        bg_url = bg

        # Get the filename from the URL
        filename = bg_url.split('/')[-1]

        # Download the image
        img_response = requests.get(bg_url)
        img_path = os.path.join(download_dir, filename)
        
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        
        print(f"Downloaded: {filename}")
