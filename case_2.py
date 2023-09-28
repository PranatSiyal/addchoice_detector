import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,NoSuchFrameException
from PIL import Image
from io import BytesIO
def capture_screenshots(url, folder, output_txt):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    # Specify the path to the ChromeDriver executable
    # Create ChromeOptions and set the binary location
    desired_version = "116.0.5845.96"
    service = Service(ChromeDriverManager(desired_version).install())
    # service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    # Navigate to the URL
    driver.get(url)
    # Wait for the page to load (increase this time as needed)
    time.sleep(1)  # Wait for 5 seconds (adjust as needed)
    # Recursive function to capture image sources from iframes
    def capture_iframe_images(iframe, image_sources_dict):
        try:
            driver.switch_to.frame(iframe)
            iframe_images = driver.find_elements(By.TAG_NAME, 'img')
            for idx, img in enumerate(iframe_images):
                img_src = img.get_attribute("src")
                if img_src:
                    image_sources_dict[len(image_sources_dict)] = img_src
                    print(f"Image source for iframe {iframe.get_attribute('src')}, img_{idx} (src): {img_src}")
        except NoSuchElementException:
            print("No image elements found in the iframe.")
        finally:
            driver.switch_to.default_content()
        return image_sources_dict
    # scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
    # driver.execute_script(scroll_script)
    scroll_step = 100  # Adjust this value as needed
    scroll_interval = 0.2
    document_height = driver.execute_script("return document.body.scrollHeight")
# Scroll through the page using smooth scrolling
    current_position = 0
    scroll_position = 0
    while current_position < document_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        current_position += scroll_step
        time.sleep(scroll_interval)
        if scroll_position < document_height:
            time.sleep(1)
            screenshot_name = f'fullpage_screenshot_{scroll_position}.png'
            screenshot_path = os.path.join(folder, screenshot_name)
            driver.save_screenshot(screenshot_path)
            print(f'Screenshot captured: {screenshot_name}')
            scroll_position += 500
    try:
        # Capture screenshots of each image in <img> tags
        image_elements = driver.find_elements(By.TAG_NAME, 'img')
        iframe_elements = driver.find_elements(By.TAG_NAME, 'iframe')
        div_elements = driver.find_elements(By.TAG_NAME, 'div')
        a_elements = driver.find_elements(By.TAG_NAME, 'a')
        gwd_elements  = driver.find_elements(By.TAG_NAME, 'gwd-image')
    except NoSuchElementException:
        print("No image or iframe elements found on the page.")
    #keeping a set to keep track of elements looped to avoid duplicates
    processed_elements = set()
    image_sources_dict = {}  # Dictionary to store image sources
    for idx, (element, bg_element) in enumerate(zip(image_elements + iframe_elements + gwd_elements, div_elements + a_elements)):
    #for idx, element in enumerate(iframe_elements + image_elements + gwd_elements, div_elements + a_elements ):
        #loop over iframe
        #switch to iframe and screenshot img/iframe tags from the iframe/image
        try:
            #element = driver.find_elements(By.TAG_NAME, element.tag_name)[idx]
            #background_image = div_element.value_of_css_property('background-image')
            width = element.size['width']
            height = element.size['height']
            element_identifier = f"{element.tag_name}{element.location['x']}{element.location['y']}"
            if element_identifier not in processed_elements and width > 100 and height >100:
                screenshot_path = os.path.join(folder, f"img_{idx}.png")
                element.screenshot(screenshot_path)
                img_src = element.get_attribute("src")
                print(f"Image source for img, iframe, gwd elements (src): {img_src}")
                # Add the image source to the dictionary
                image_sources_dict[idx] = img_src
                #adding processed element to the set
                processed_elements.add(element_identifier)
            bg_image = bg_element.value_of_css_property('background')
            bg_width = bg_element.size['width']
            bg_height = bg_element.size['height']
            bg_element_identifier = f"{bg_image}"
            if (bg_element_identifier not in processed_elements) and (bg_width > 100 and bg_height > 100) and bg_image != "none":
                bg_screenshot_path = os.path.join(folder, f"bg_element_{idx}.png")
                bg_element.screenshot(bg_screenshot_path)
                img_src = bg_element.get_attribute("src")
                print(f"background Image source (src): {img_src}")
                # Add the image source to the dictionary
                image_sources_dict[idx] = img_src
                processed_elements.add(bg_element_identifier)
        except StaleElementReferenceException:
            print("Stale element reference. Skipping...")
    print(image_sources_dict)
    driver.quit()
    output_txt = os.path.join(os.getcwd(), 'image_sources.txt')
    with open(output_txt, 'w') as txt_file:
        for key, value in image_sources_dict.items():
            if value:
                txt_file.write(f"Image source {key}: {value}\n")
capture_screenshots("https://www.nytimes.com/", 'nyt_screenshots', 'image_sources.txt')