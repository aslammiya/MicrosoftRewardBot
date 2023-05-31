from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import csv

PATH_OF_DRIVER = "C:\\Users\\aslam\\chromedriver_win32\\chromedriver.exe"

def get_driver():
    options = Options()
    options.add_argument('log-level=3')
    options.add_argument("--start-maximized")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-images')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=PATH_OF_DRIVER, options=options)
    return driver

def get_drive_video_links(driver,folder_url):

    # Navigate to the Google Drive folder URL
    driver.get(folder_url)

    # Wait for the page to load
    time.sleep(5)

    # Find the video links in the page source
    video_links = driver.find_elements_by_css_selector('a[data-target="doc"]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS, "//span[text()='Next']")))
    video_urls = [link.get_attribute('href') for link in video_links]

    # Close the WebDriver
    driver.quit()

    return video_urls

def save_links_to_csv(video_links, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Link'])
        for link in video_links:
            writer.writerow([link])

# Usage
folder_url = 'https://drive.google.com/drive/folders/1ArN3Tfd1aJGpy3PahWd6SHxVJISOkW9a'
output_file = 'video_links.csv'

video_links = get_drive_video_links(folder_url)
save_links_to_csv(video_links, output_file)

print(f"Video links saved to {output_file}.")