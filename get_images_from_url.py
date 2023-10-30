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
def capture_fullscreenshots(url, output):
    # Specify the path to the ChromeDriver executable
    # desired_version = "116.0.5845.96"
    # service = Service(ChromeDriverManager().install())
    # service = Service(ChromeDriverManager(desired_version).install())
    # Create ChromeOptions and set the binary location
    options = webdriver.ChromeOptions()
    # options.binary_location = "/Users/pranatsiyal/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
        
    driver.get(url)
    #document_height = driver.execute_script("return document.body.scrollHeight")
    # document_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    initial_height = driver.execute_script('return document.documentElement.scrollHeight')
    initial_width  = driver.execute_script('return document.documentElement.scrollWidth')

    driver.set_window_size(initial_width, initial_height)

    driver.save_screenshot("screenshot1.png")

    scroll_height = initial_height
    viewport_height = driver.execute_script('return window.innerHeight')
    scroll_step = viewport_height - 10  
    current_scroll = 0
    screenshot_count = 1
    while current_scroll < scroll_height:

        driver.execute_script(f"window.scrollTo(0, {current_scroll});")

        driver.save_screenshot(f"screenshot{str(screenshot_count)}.png")
        screenshot_count += 1
        current_scroll += scroll_step

    # Close the WebDriver
    driver.quit()

    screenshot_directory = os.getcwd()
    screenshot_files = [f for f in os.listdir(screenshot_directory) if f.startswith("screenshot")]

    # Sort the screenshot files based on their filename (to maintain order)
    screenshot_files.sort()

    # Initialize an empty list to store image objects
    images = []

    # Load each screenshot and append it to the 'images' list
    for screenshot_file in screenshot_files:
        screenshot_path = os.path.join(screenshot_directory, screenshot_file)
        image = Image.open(screenshot_path)
        images.append(image)

    # Determine the total height of the stitched image
    total_height = sum(image.height for image in images)

    # Create a new image with the same width as the first screenshot and the total height
    stitched_image = Image.new("RGB", (images[0].width, total_height))

    # Initialize the vertical position where the next screenshot should be pasted
    y_offset = 0

    # Paste each screenshot onto the stitched image
    for image in images:
        stitched_image.paste(image, (0, y_offset))
        y_offset += image.height

    # Save the final stitched image
    stitched_image.save(output)

    # Optionally, you can delete the individual screenshot files
    for screenshot_file in screenshot_files:
        os.remove(os.path.join(screenshot_directory, screenshot_file))
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
capture_fullscreenshots("https://www.cnn.com", "CNNfullpage.png")



def capture_screenshots(url, folder, output_txt):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except: 
        pass
    
    # Specify the path to the ChromeDriver executable
    #desired_version = "116.0.5845.96"
    # service = Service(ChromeDriverManager().install())
    #service = Service(ChromeDriverManager(desired_version).install())
    # Create ChromeOptions and set the binary location
    options = webdriver.ChromeOptions()
    #options.binary_location = "/Users/pranatsiyal/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome( options=options)
     
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load (increase this time as needed)
    time.sleep(1)  # Wait for 5 seconds (adjust as needed)
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
    image_sources_dict = {}
    for idx, (element, bg_element) in enumerate(zip(image_elements + iframe_elements + gwd_elements, div_elements + a_elements)):
    #for idx, element in enumerate(iframe_elements + image_elements + gwd_elements, div_elements + a_elements ):
        #loop over iframe 
        #switch to iframe and screenshot img/iframe tags from the iframe/image
        try:
            #element = driver.find_elements(By.TAG_NAME, element.tag_name)[idx]
            #background_image = div_element.value_of_css_property('background-image')
            width = element.size['width']
            height = element.size['height']
            
            element_identifier = f"{element.tag_name}_{element.location['x']}_{element.location['y']}"
        
            if element_identifier not in processed_elements and width > 100 and height >100:
                screenshot_path = os.path.join(folder, f"img_{idx}.png")
                element.screenshot(screenshot_path)
                print(f"Captured screenshot: {screenshot_path}")
                img_src = element.get_attribute("src")
                print(f"Image source for img, iframe, gwd elements (src): {img_src}")
                #Adding image source to the dictionary
                image_sources_dict[img_src] = screenshot_path
                #adding processed element to the set
                processed_elements.add(element_identifier)
            bg_image = bg_element.value_of_css_property('background')
            bg_width = bg_element.size['width']
            bg_height = bg_element.size['height']

            bg_element_identifier = f"{bg_image}"

            if (bg_element_identifier not in processed_elements) and (bg_width > 100 and bg_height > 100) and bg_image != "none":
                bg_screenshot_path = os.path.join(folder, f"bg_element_{idx}.png")
                bg_element.screenshot(bg_screenshot_path)
                print(f"Captured screenshot: {bg_screenshot_path}")
                img_src = bg_element.get_attribute("src")
                print(f"background Image source (src): {img_src}")
                #Add image element source to the dictionary
                image_sources_dict[img_src] = bg_screenshot_path
                processed_elements.add(bg_element_identifier)
        except StaleElementReferenceException:
            print("Stale element reference. Skipping...")
        except NoSuchElementException:
            print("No image or iframe elements found on the page.")
        shadow_dom_elements = driver.find_element(By.CSS_SELECTOR, 'div')
    
    # for shadow_dom_element in shadow_dom_elements:
    #     # Open shadow DOM using JavaScript
    #     driver.execute_script("arguments[0].openShadowRoot();", shadow_dom_element)
        
    #     # Find all iframe elements within the shadow DOM
    #     if_elements = driver.find_elements(By.TAG_NAME, 'iframe')
    #     try:
            
    #         for idx, iframe_element in enumerate(if_elements):
    #             screenshot_path = os.path.join(folder, f"iframe_{idx}.png")
                
    #             # Switch to the iframe and capture screenshot
    #             driver.switch_to.frame(iframe_element)
    #             driver.save_screenshot(screenshot_path)
    #             print(f"Captured screenshot: {screenshot_path}")
                
    #             # Switch back to the default content
    #             driver.switch_to.default_content()
    #     except NoSuchFrameException:
    # #         print(f"Iframe {idx} not found. Skipping...")
    #          continue
    #     # Close the shadow DOM using JavaScript
    #     driver.execute_script("arguments[0].closeShadowRoot();", shadow_dom_element)
    # shadow_elements = []
    # element = driver.find_element(By.TAG_NAME, 'html')
    # stack = [element]

    # while stack:
    #     current_element = stack.pop()
    #     shadow_root = driver.execute_script('return arguments[0].shadowRoot;', current_element)
        
    #     if shadow_root:
    #         shadow_elements.append(shadow_root)
        
    #     stack.extend(current_element.find_elements(By.TAG_NAME, '*'))

    
    # for iddx, iframe_ele in enumerate(iframe_elements + shadow_elements):
    # #for idx, (iframe_ele, bg_ele) in enumerate(zip(iframe_elements, div_elements + a_elements)):
    #     try:
    #         driver.switch_to.frame(iframe_ele)
    #         im_elements = driver.find_elements(By.TAG_NAME, "img")
    #         # if_elements = driver.find_elements(By.TAG_NAME, "iframe")
    #         for idx, im_element in enumerate(im_elements):
    #             width = im_element.size['width']
    #             height = im_element.size['height']
    #             if width > 100 and height > 100:
    #                 screenshot_path = os.path.join(folder, f"iframe{iddx}_{idx}.png")
    #                 im_element.screenshot(screenshot_path)
    #                 print(f"Captured screenshot: {screenshot_path}")
    #                  # Extract the src attribute
    #                 img_src = im_element.get_attribute("src")
    #                 print(f"Image source looping within iframe and shadow dom (src): {img_src}")
    #         driver.switch_to.default_content()
    #     except NoSuchFrameException:
    #         print(f"Iframe {idx} not found. Skipping...")
    #         continue

    # Close the WebDriver
    driver.quit()
    output_txt = os.path.join(os.getcwd(), output_txt)
    with open(output_txt, 'w') as txt_file:
        for src, src_type in image_sources_dict.items():
            txt_file.write(f"Source URL: {src}, Type: {src_type}\n")
capture_screenshots("https://www.cnn.com", "images", "output_txt")