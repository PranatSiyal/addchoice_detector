from Screenshot import Screenshot
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,NoSuchFrameException
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Saving screenshot

# Specify the path to the ChromeDriver executable
desired_version = "116.0.5845.96"
# service = Service(ChromeDriverManager().install())
service = Service(ChromeDriverManager(desired_version).install())
# Create ChromeOptions and set the binary location
options = webdriver.ChromeOptions()
options.binary_location = "/Users/pranatsiyal/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)
    
driver.get("https://www.cnn.com/")
#document_height = driver.execute_script("return document.body.scrollHeight")
# document_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
initial_height = driver.execute_script('return document.documentElement.scrollHeight')
initial_width  = driver.execute_script('return document.documentElement.scrollWidth')

driver.set_window_size(initial_width, initial_height)

# Capture the initial screenshot
driver.save_screenshot("screenshot1.png")

# Define scroll height and step values for scrolling
scroll_height = initial_height
viewport_height = driver.execute_script('return window.innerHeight')
scroll_step = viewport_height - 10  # Adjust this value as needed

# Initialize variables for tracking scroll position
current_scroll = 0
screenshot_count = 1

# Scroll and capture screenshots until the entire page is covered
while current_scroll < scroll_height:
    # Scroll down by the specified step
    driver.execute_script(f"window.scrollTo(0, {current_scroll});")

    # Capture a screenshot of the current view
    driver.save_screenshot(f"screenshot{str(screenshot_count)}.png")

    # Increment the screenshot count
    screenshot_count += 1

    # Update the current scroll position
    current_scroll += scroll_step

# Close the WebDriver
driver.quit()


# folder = 'fullpageSC'
# print(height)
# os.mkdir(os.path.join(os.getcwd(), folder))
# # Scroll through the page using smooth scrolling
# current_position = 0
# scroll_position = 0
# while current_position < document_height:
#     current_position += 800
#     time.sleep(scroll_interval)
# driver.quit()