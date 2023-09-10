import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,NoSuchFrameException
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
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
     
    # Navigate to the URL
    driver.get("https://www.cnn.com/")
    
    # Wait for the page to load (increase this time as needed)
    time.sleep(1)  # Wait for 5 seconds (adjust as needed)
    
    # scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
    # driver.execute_script(scroll_script)
    scroll_step = 100  # Adjust this value as needed
    scroll_interval = 0.2
    document_height = driver.execute_script("return document.body.scrollHeight")

# Scroll through the page using smooth scrolling
    current_position = 0
    while current_position < document_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        current_position += scroll_step
        time.sleep(scroll_interval)

        
    

    try:
        # Capture screenshots of each image in <img> tags
        image_elements = driver.find_elements(By.TAG_NAME, 'img')
        iframe_elements = driver.find_elements(By.TAG_NAME, 'iframe')
        div_elements = driver.find_elements(By.TAG_NAME, 'div')
        a_elements = driver.find_elements(By.TAG_NAME, 'a')
        gwd_elements  = driver.find_elements(By.TAG_NAME, 'gwd-image')
        
        #svg_elements = driver.find_elements(By.TAG_NAME, 'svg')

        #screenshot using xpath 

        # image_elements = driver.find_elements(By.XPATH, "//img[@src]")
        # a_elements = driver.find_elements(By.XPATH, "//a[@href]")
        # div_elements = driver.find_element(By.XPATH, "//div[@style]")
        # iframe_elements = driver.find_elements(By.XPATH, "//iframe[@src]")


    except NoSuchElementException:
        print("No image or iframe elements found on the page.")
    
    #keeping a set to keep track of elements looped to avoid duplicates
    processed_elements = set()
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
                processed_elements.add(bg_element_identifier)
        except StaleElementReferenceException:
            print("Stale element reference. Skipping...")
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
    shadow_elements = []
    element = driver.find_element(By.TAG_NAME, 'html')
    stack = [element]

    while stack:
        current_element = stack.pop()
        shadow_root = driver.execute_script('return arguments[0].shadowRoot;', current_element)
        
        if shadow_root:
            shadow_elements.append(shadow_root)
        
        stack.extend(current_element.find_elements(By.TAG_NAME, '*'))

    
    for iddx, iframe_ele in enumerate(iframe_elements + shadow_elements):
    #for idx, (iframe_ele, bg_ele) in enumerate(zip(iframe_elements, div_elements + a_elements)):
        try:
            driver.switch_to.frame(iframe_ele)
            im_elements = driver.find_elements(By.TAG_NAME, "img")
            # if_elements = driver.find_elements(By.TAG_NAME, "iframe")
            for idx, im_element in enumerate(im_elements):
                width = im_element.size['width']
                height = im_element.size['height']
                if width > 100 and height > 100:
                    screenshot_path = os.path.join(folder, f"iframe{iddx}_{idx}.png")
                    im_element.screenshot(screenshot_path)
                    print(f"Captured screenshot: {screenshot_path}")
                     # Extract the src attribute
                    img_src = im_element.get_attribute("src")
                    print(f"Image source looping within iframe and shadow dom (src): {img_src}")
            driver.switch_to.default_content()
        except NoSuchFrameException:
            print(f"Iframe {idx} not found. Skipping...")
            continue

    # Close the WebDriver
    driver.quit()

capture_screenshots("https://www.cnn.com/", 'cnn_screenshots')