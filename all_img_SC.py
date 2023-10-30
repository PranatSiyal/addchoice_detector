import time
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,NoSuchFrameException
from PIL import Image
from io import BytesIO
import numpy as np
import os

def capture_imgSC(url, folder, output_txt, driver):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except FileExistsError: 
        pass
    
    driver.get(url)
    
    time.sleep(1)  
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

        #loop over iframe 
        try:

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
        


    output_txt = os.path.join(os.getcwd(), output_txt)
    with open(output_txt, 'a') as txt_file:
        for src, src_type in image_sources_dict.items():
            txt_file.write(f"Source URL: {src}, Type: {src_type}\n")



def capture_fullpageSC(url, output, driver):
        
    driver.get(url)
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
        time.sleep(1)  
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")

        driver.save_screenshot(f"screenshot{str(screenshot_count)}.png")
        screenshot_count += 1
        current_scroll += scroll_step

    # Close the WebDriver


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

# capture_fullpageSC("https://www.cnn.com", "CNNfullpage.png")

# capture_imgSC("https://www.cnn.com", 'cnn_screenshots','cnn_image_sources.txt')    


def capture_shadowdomSC(url, folder, output_txt, driver):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except FileExistsError:  
        pass
    
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load (increase this time as needed)
    time.sleep(1)  # Wait for 5 seconds (adjust as needed)
    

    image_sources_dict = {}
    shadow_dom_elements = driver.find_element(By.CSS_SELECTOR, 'div')

    for shadow_dom_element in shadow_dom_elements:
        # Open shadow DOM using JavaScript
        driver.execute_script("arguments[0].openShadowRoot();", shadow_dom_element)
        
        # Find all iframe elements within the shadow DOM
        if_elements = driver.find_elements(By.TAG_NAME, 'iframe')
        # im_elements = driver.find_elements(By.TAG_NAME, 'img')
        try:
            
            for idx, iframe_element in enumerate(if_elements):
                screenshot_path = os.path.join(folder, f"iframe_{idx}.png")
                img_src = iframe_element.get_attribute("src")
                # Switch to the iframe and capture screenshot
                driver.switch_to.frame(iframe_element)
                driver.save_screenshot(screenshot_path)
                print(f"Captured screenshot: {screenshot_path}")
                # Adding image source to the dictionary
                image_sources_dict[img_src] = screenshot_path
                
                # Switch back to the default content
                driver.switch_to.default_content()
        except NoSuchFrameException:
    #         print(f"Iframe {idx} not found. Skipping...")
             continue
        # Close the shadow DOM using JavaScript
        driver.execute_script("arguments[0].closeShadowRoot();", shadow_dom_element)
    # shadow_elements = []
    # element = driver.find_element(By.TAG_NAME, 'html')
    # stack = [element]

    # while stack:
    #     current_element = stack.pop()
    #     shadow_root = driver.execute_script('return arguments[0].shadowRoot;', current_element)
        
    #     if shadow_root:
    #         shadow_elements.append(shadow_root)
        
    #     stack.extend(current_element.find_elements(By.TAG_NAME, '*'))

    output_txt = os.path.join(os.getcwd(), output_txt)
    with open(output_txt, 'a') as txt_file:
        for src, src_type in image_sources_dict.items():
            txt_file.write(f"Source URL: {src}, Type: {src_type}\n")


def capture_iframeSC(url, folder, output_txt, driver):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except FileExistsError: 
        pass
    
     
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load (increase this time as needed)
    time.sleep(1)  
    try:
        # Capture screenshots of each image in <img> tags
        iframe_elements = driver.find_elements(By.TAG_NAME, 'iframe')
        
    except NoSuchElementException:
        print("No image or iframe elements found on the page.")
    

    image_sources_dict = {}
    for iddx, iframe_ele in enumerate(iframe_elements):
    #for idx, (iframe_ele, bg_ele) in enumerate(zip(iframe_elements, div_elements + a_elements)):
        try:
            driver.switch_to.frame(iframe_ele)
            im_elements = driver.find_elements(By.TAG_NAME, "img")
            if_elements = driver.find_elements(By.TAG_NAME, "iframe")
            for idx, im_element in enumerate(im_elements+if_elements):
                width = im_element.size['width']
                height = im_element.size['height']
                if width > 100 and height > 100:
                    screenshot_path = os.path.join(folder, f"iframe{iddx}_{idx}.png")
                    im_element.screenshot(screenshot_path)
                    print(f"Captured screenshot: {screenshot_path}")
                     # Extract the src attribute
                    img_src = im_element.get_attribute("src")
                    image_sources_dict[img_src] = screenshot_path
                    print(f"Image source looping within iframe and shadow dom (src): {img_src}")
            driver.switch_to.default_content()
        except NoSuchFrameException:
            print(f"Iframe {idx} not found. Skipping...")
            continue

    # Close the WebDriver

    output_txt = os.path.join(os.getcwd(), output_txt)
    with open(output_txt, 'a') as txt_file:
        for src, src_type in image_sources_dict.items():
            txt_file.write(f"Source URL: {src}, Type: {src_type}\n")


# THIS IS HELPER FUNCTION FOR HAR CAPTURE METHOD
def har_helper(url, output_file, driver):
   
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



def HAR_capture(url, driver, proxy, server):
    # Specify the directory to save screenshots
    SCREENSHOT_DIRECTORY = 'image_screenshots'

    try:
        # Start capturing HTTP requests
        proxy.new_har("example", options={'captureHeaders': True, 'captureContent': True})

        # Open a website
        driver.get(url)
        time.sleep(15)  # Give the page some time to load

        # Get the HAR data and captured network events
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
        with open('image_urls.txt', 'a') as file:
            for url in image_urls:
                screenshot_filename = f"Image {screenshot_counter}.png"
                screenshot_file = os.path.join(SCREENSHOT_DIRECTORY, screenshot_filename)

                if har_helper(url, screenshot_file, driver):
                    file.write(url + '\n')

                # Increment the screenshot counter
                screenshot_counter += 1

        print('Image URLs saved to image_urls.txt')
        # Add a pause to keep the browser window open
        input("Press Enter to close the browser...")
    finally:
        # Quit the browser and stop the proxy server
        driver.quit()
        server.stop()

# Call the function to execute the capture process
def main():
    # Start BrowserMob Proxy server
    server = Server("/Users/pranatsiyal/addchoice_detector/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()

    options = webdriver.ChromeOptions()
    #options.binary_location = "/Users/pranatsiyal/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    #options.add_argument('--headless')
    options.add_argument("--proxy-server={}".format(proxy.proxy))
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Launch the browser with configured proxy
    driver = webdriver.Chrome(options=options)

    HAR_capture("https://www.cnn.com",driver, proxy, server)
    capture_fullpageSC("https://www.cnn.com", "fullpageSC.png", driver)
    capture_imgSC("https://www.cnn.com", "images", "output.txt", driver)

    # capture_iframeSC("https://www.cnn.com", 'images', "output_txt", driver)

    # capture_fullpageSC("https://www.cnn.com", "CNNfullpage.png", driver)

    # capture_imgSC("https://www.cnn.com", 'cnn_screenshots','cnn_image_sources.txt', driver)   

    # capture_shadowdomSC("https://www.cnn.com", 'cnn_screenshots_SD','cnn_image_sources_SD.txt', driver) 

    # capture_iframeSC("https://www.cnn.com", 'cnn_screenshots_SD','cnn_image_sources_SD.txt', driver)

    driver.quit()
main()