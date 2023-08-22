from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Specify the path to the ChromeDriver executable
#chrome_driver_path = "/Users/pranatsiyal/Downloads/chromedriver_mac_arm64/chromedriver"
service = Service(executable_path='ChromeDriverManager().install()')
options = webdriver.ChromeOptions()
options.binary_location = "/Users/pranatsiyal/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)
# ...

# Set up the ChromeDriver with ChromeOptions

# Navigate to the URL
url = "https://www.tmz.com/"  # Replace with the actual URL
driver.get(url)

# Perform any required actions on the page

# Close the WebDriver
driver.quit()