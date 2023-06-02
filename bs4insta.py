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

options = Options()
options.add_argument('log-level=3')
options.add_argument("--start-maximized")
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-images')
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=PATH_OF_DRIVER, options=options)
# driver.get("https://google.com/")
# time.sleep(20000)

numv = 1
with open('linksLikes.csv', 'r') as file:
    reader = csv.reader(file)
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for row in reader:
            link = row[0]
            driver.get(link)
            time.sleep(2)
            try:
                elements = driver.find_element(By.XPATH, "(//section/div/div/span)[1]").text
            except Exception:
                elements = "0 Not found"
            writer.writerow([link, elements])
            print(numv," ",link," ", elements)
            numv = numv+1