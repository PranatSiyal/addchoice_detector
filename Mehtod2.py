from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.tmz.com/")

section_one = driver.find_element(By.ID, "")
section_one.screenshot("random.png")
wait = WebDriverWait(driver, 20)

try:
    # Wait for the element with ID "ad_unit" to be present, with a timeout of 20 seconds
    ad_unit_element = wait.until(EC.presence_of_element_located((By.ID, "ad_unit")))
    
    # Once the element is found, you can perform actions on it, e.g., click, get text, etc.
    # For example:
    ad_unit_element.click()

except Exception as e:
    # If the element is not found within the specified time, an exception will be raised.
    print("Error:", e)
driver.quit()