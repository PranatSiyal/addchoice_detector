import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchFrameException

from PIL import Image
from io import BytesIO
def capture_screenshots(url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    
    # Specify the path to the ChromeDriver executable
    
    # Create ChromeOptions and set the binary location

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.binary_location = "/Users/pranatsiyal/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
     
    # Navigate to the URL
    driver.get("https://www.cnn.com/")
    
    # Wait for the page to load (increase this time as needed)
    time.sleep(6)  # Wait for 5 seconds (adjust as needed)
    
    # Capture screenshots of each image in <img> tags
    image_elements = driver.find_elements(By.TAG_NAME, 'img')
    iframe_elements = driver.find_elements(By.TAG_NAME, 'iframe')
    #div_elements = driver.find_elements(By.TAG_NAME, 'div')

    #div_elements = driver.find_elements(By.TAG_NAME, 'div')
    # for idx, img_element in enumerate(image_elements):
    #     #loop over iframe 
    #     #switch to iframe and screenshot img/iframe tags from the iframe/image
    #     #

    #     width = img_element.size['width']
    #     height = img_element.size['height']
    #     if width > 0 and height > 0:
    #         screenshot_path = os.path.join(folder, f"img_{idx}.png")
    #         img_element.screenshot(screenshot_path)
    #         print(f"Captured screenshot: {screenshot_path}")
        
    for idx, iframe_ele in enumerate(iframe_elements):
        try:
            driver.switch_to.frame(iframe_ele)
            im_elements = driver.find_elements(By.TAG_NAME, "img")
            if_elements = driver.find_elements(By.TAG_NAME, "iframe")
            for idx, im_element in enumerate(im_elements+if_elements):
                width = im_element.size['width']
                height = im_element.size['height']
                if width > 0 and height > 0:
                    screenshot_path = os.path.join(folder, f"iframe_{idx}.png")
                    im_element.screenshot(screenshot_path)
                    print(f"Captured screenshot: {screenshot_path}")
                    screenshot_path = f"iframe_{idx}.png"
                    im_element.screenshot(screenshot_path)
                    print(f"Captured screenshot: {screenshot_path}")
            driver.switch_to.default_content()
        except NoSuchFrameException:
            print(f"Iframe {idx} not found. Skipping...")
            continue

    # Close the WebDriver
    driver.quit()

capture_screenshots('https://www.cnn.com/', 'cnn_screenshots')