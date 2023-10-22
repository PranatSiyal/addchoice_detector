import time
from browsermobproxy import Server
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import numpy as np
import os


# Specify the directory to save screenshots
SCREENSHOT_DIRECTORY = 'image_screenshots'

# Function to take a screenshot
def take_screenshot(url, output_file):
    # Set up Chrome options for headless browsing
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # Create a WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        driver.save_screenshot(output_file)

        # Open the saved screenshot using PIL
        screenshot = Image.open(output_file)

        # Convert the screenshot to grayscale
        grayscale_screenshot = screenshot.convert('L')

        # Convert the grayscale screenshot to a NumPy array
        screenshot_array = np.array(grayscale_screenshot)

        # Calculate the percentage of white and black pixels
        white_pixel_count = np.sum(screenshot_array >= 255)  # Adjust the threshold as needed
        black_pixel_count = np.sum(screenshot_array <= 35)   # Adjust the threshold as needed
        total_pixel_count = screenshot_array.size
        white_pixel_percentage = white_pixel_count / total_pixel_count
        black_pixel_percentage = black_pixel_count / total_pixel_count

        # Define thresholds for considering a screenshot as blank or black
        max_blank_threshold = 0.1  # Adjust as needed
        max_black_threshold = 0.99  # Adjust as needed

        if white_pixel_percentage < max_blank_threshold and black_pixel_percentage < max_black_threshold:
            print(f"Screenshot saved as {output_file}")
            return True
        else:
            os.remove(output_file)
            print(f"Screenshot {output_file} deleted")
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
# Start BrowserMob Proxy server
server = Server("/Users/pranatsiyal/addchoice_detector/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()
chrome_options = Options()
chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")
# Launch the browser with configured proxy
driver = webdriver.Chrome(options=chrome_options)


# Start capturing HTTP requests
proxy.new_har("example", options={'captureHeaders': True, 'captureContent': True})

# Open a website
driver.get("http://zdnet.com")

time.sleep(5)  # Give the page some time to load
# Get the HAR data
# Get the captured network events
har_entries = proxy.har['log']['entries']

# Filter requests with mimeType containing "image"
filtered_entries = [entry for entry in har_entries if entry['response']['content'].get('mimeType', '').startswith('image/')]

# Extract image URLs
image_urls = [entry['request']['url'] for entry in filtered_entries]
# Create the screenshot directory if it doesn't exist
os.makedirs(SCREENSHOT_DIRECTORY, exist_ok=True)
# Counter for naming screenshots
screenshot_counter = 1
# Save the image URLs to a text file
with open('image_urls.txt', 'w') as file:
    for url in image_urls:
        screenshot_filename = f"Image {screenshot_counter}.png"
        screenshot_file = os.path.join(SCREENSHOT_DIRECTORY, screenshot_filename)
        if take_screenshot(url, screenshot_file):
            file.write(url + '\n')
        # Increment the screenshot counter
        screenshot_counter += 1
print('Image URLs saved to image_urls.txt')
# Add a pause to keep the browser window open
input("Press Enter to close the browser...")
# Quit the browser and stop the proxy server
driver.quit()
server.stop()