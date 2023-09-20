from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import time

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--ignore-certificate-errors")

# driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()
# URL of the website
url = "https://pib.gov.in/PhotogalleryNew.aspx"
# driver.get(url)

drive_path='W:\\Programming\\SIH-2023\\AlekhyaaBackend\\env\\Scripts\\geckodriver.exe'

firefox_service = FirefoxService(executable_path=drive_path)
firefox_options = FirefoxOptions()
firefox_driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
firefox_driver.get(url)
# Get the current day
from datetime import date
current_day = date.today().day

# Select the day from the dropdown
day_dropdown = Select(firefox_driver.find_element(By.ID, "ContentPlaceHolder1_ddlday"))
day_dropdown.select_by_value(str(current_day))
# Find all the album links and store them in a list
album_links = firefox_driver.find_elements(By.XPATH, '//a[starts-with(@href, "ShowAlbum.aspx?albumid=")]')

# Loop through the album links
for album_link in album_links:
    album_id = album_link.get_attribute("href").split("albumid=")[1]
    album_directory = f"Album_{album_id}"

    # Create a directory for the album if it doesn't exist
    if not os.path.exists(album_directory):
        os.makedirs(album_directory)

    # # Use an explicit wait to wait for the element to become clickable
    # wait = WebDriverWait(firefox_driver, 10)
    # album_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[starts-with(@href, "ShowAlbum.aspx?albumid=")]')))

    # Scroll the album link into view
    firefox_driver.execute_script("arguments[0].scrollIntoView(true);", album_link)
    
    # Wait for a short period to ensure the link is fully in view
    time.sleep(1)
    


    # Click on the album link
    album_link.click()

    # Inside the album, find and download images
    image_elements = firefox_driver.find_elements(By.XPATH, '//img[contains(@src, "Photogallery")]')
    for index, image_element in enumerate(image_elements):
        image_url = image_element.get_attribute("src")
        image_filename = f"{album_directory}/Image_{index+1}.jpg"

        # Download the image
        urllib.request.urlretrieve(image_url, image_filename)

    # Go back to the main page
    firefox_driver.back()
firefox_driver.quit()
