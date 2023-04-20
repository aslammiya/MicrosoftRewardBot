from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from essential_generators import DocumentGenerator
import time
import random
import string
import config

PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 11.0; SM-M30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36'
PATH_OF_DRIVER = "C:\\Users\\aslam\\chromedriver_win32\\chromedriver.exe"
# PROXY_HOST = '165.227.81.188'
# PROXY_PORT = 9987

def get_driver(mode):
    options = Options()
    if mode == 'pc':
        options.add_argument(f'user-agent={PC_USER_AGENT}')
        options.add_argument("--start-maximized")
    elif mode == 'mobile':
        mobile_emulation = {
            "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
            "userAgent": MOBILE_USER_AGENT
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        raise ValueError('Invalid mode')
    
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=PATH_OF_DRIVER, options=options)

    return driver

def login(driver, email, password):
    EMAILFIELD = (By.ID, "i0116")
    PASSWORDFIELD = (By.ID, "i0118")
    NEXTBUTTON = (By.ID, "idSIButton9")
    NOBUTTON = (By.ID,"idBtn_Back")
    num_submit = (By.ID,"iSelectProofAction")
    num_input_field = (By.ID, "iProofPhone")
    otpInput = (By.ID, "iOttText")
    otpBtn = (By.ID, "iVerifyCodeAction")
    driver.get('https://login.live.com')
    # driver.get('https://whatismyipaddress.com/')
    # time.sleep(20000)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    # time.sleep(20)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NOBUTTON)).click()
    except Exception:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(num_input_field)).send_keys(last4Digit)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(num_submit)).click()
        time.sleep(2)
        while True:
            otp = input("\nEnter OTP: ")
            if otp:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(otpInput)).send_keys(otp)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(otpBtn)).click()
                break
    except:
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'iNext'))).click()

    driver.get(f'https://www.bing.com/search?q={generate_sentence()}')
    print("\n\nLOGIN DONE\n\n")

def generate_sentence():
    sentence_length = random.randint(3, 10)
    sentence = ' '.join(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 8))) for _ in range(sentence_length))
    return sentence

def totalPoints(driver):
    driver.refresh()
    time.sleep(3)
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@id="id_rc"]')))

def search(driver,numOfSearch):
    for i in range(numOfSearch):
        print(f"Search : {i}")
        driver.get(f'https://www.bing.com/search?q={generate_sentence()}')

def logout(driver):
    driver.get("https://login.live.com/logout.srf")

def pc_search(numOfSearch,email,password):
    driver_pc = get_driver('pc')
    login(driver_pc, email, password)
    driver_pc.refresh()
    time.sleep(10)
    print(totalPoints(driver_pc).text)
    search(driver_pc,numOfSearch)
    logout(driver_pc)
    driver_pc.quit()


def mobile_search(numOfSearch,email,password):
    driver_mobile = get_driver('mobile')
    login(driver_mobile, email, password)
    time.sleep(10)
    driver_mobile.refresh()
    time.sleep(1)
    driver_mobile.execute_script("window.scrollTo(0, 0);")
    WebDriverWait(driver_mobile, 10).until(EC.element_to_be_clickable((By.ID, "mHamburger"))).click()
    time.sleep(5)
    search(driver_mobile,numOfSearch)
    logout(driver_mobile)
    driver_mobile.quit()

def punchCards(driver):
    print("Rewards start")
    driver.get('https://rewards.bing.com/')
    time.sleep(10)
    rewards_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "id_rh")))
    rewards_button.click()
    time.sleep(15)
    # card_list = driver.find_elements(By.XPATH,"//div[@id='bingRewards']/div[1]/div[5]//div[contains(@class, 'card')]")
    print("ele finded")
    count = 1
    while True:
        try:
            card_list = driver.find_elements(By.XPATH, f"//div[@id='bingRewards']/div[1]/div[5]/div[{count}]//div[contains(@class, 'card')]")
            if not card_list:
                break
            for card in card_list:
                card.click()
                time.sleep(2)
                rewards_button.click()
            count += 1
        except NoSuchElementException:
            break
    time.sleep(10)
    # for card in driver.find_elements(By.XPATH,"//div[@id='bingRewards']/div[1]/div[5]//div[contains(@class, 'card')]"):
    #     print("for loop")
    #     driver.execute_script("arguments[0].scrollIntoView();", card)
    #     card.click()
    #     time.sleep(2)
    #     rewards_button.click()
    return "All cards have been clicked"

def click_all_cards(driver):
    # set up webdriver
    wait = WebDriverWait(driver, 10)
    
    # navigate to rewards.bing.com
    driver.get('https://rewards.bing.com/')
    time.sleep(3)
    
    while True:
        card_list = driver.find_elements(By.XPATH,"//div[@id='bingRewards']/div[1]/div[5]//div[contains(@class, 'card')]")
        if len(card_list) == 0:
            break
        for card in card_list:
            card.click()
            time.sleep(2)
            rewards_button = wait.until(EC.element_to_be_clickable((By.ID, "id_rh")))
            rewards_button.click()
            time.sleep(3)
        driver.get('https://rewards.bing.com/')
        time.sleep(3)
    driver.quit()



# email = "sohelmiya0007@outlook.com"
# password = "123@Sohel"

pc_numOfSearch = config.pc_numOfSearch
mobile_numOfSearch = config.mobile_numOfSearch
last4Digit = config.last4Digit

# driver = get_driver('pc')
# login(driver, email, password)
# click_all_cards(driver)

# pc_search(pc_numOfSearch,email,password)
# mobile_search(mobile_numOfSearch,email,password)

emails = config.emails
passwords = config.passwords

for i in range(len(emails)):
    email = emails[i]
    password = passwords[i]
    pc_search(pc_numOfSearch, email, password)
    mobile_search(mobile_numOfSearch, email, password)

# for email in lst_email:

# aslammiya12372@outlook.com
# aslammiya007@outlook.com
# sahilmiya0842@outlook.com
# sahil@miya
# 123@Aslam
# oneacc1189@outlook.com
# twoacc2287@outlook.com
# threeacc3386@outlook.com
# fouracc3386@outlook.com
# sohelmiya0007@gmail.com


## help us to protecct your account
# iProofLbl0 radio button
# iProofEmail proof  email email enter field
# iSelectProofAction Send code button