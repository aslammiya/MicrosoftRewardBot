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

def get_driver():
    options = Options()
    options.add_argument(f'user-agent={PC_USER_AGENT}')
    options.add_argument('log-level=3')
    options.add_argument("--start-maximized")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-images')
    options.add_argument('--no-sandbox')
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
    print(f">> Email {email}")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    print(f">> Password {password}")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    # time.sleep(20)
    try:
        print("▣ Clicking button")
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(NOBUTTON)).click()
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
    print(f"\nLog In To {email}")

def generate_sentence():
    sentence_length = random.randint(3, 10)
    sentence = ' '.join(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 8))) for _ in range(sentence_length))
    return sentence

def totalPoints(driver):
    driver.refresh()
    time.sleep(3)
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@id="id_rc"]')))

def search(driver,numOfSearch,email,mode):
    for i in range(numOfSearch):
        print(f"\r{email} {mode} Search : {i+1}/{numOfSearch}", end="")
        driver.get(f'https://www.bing.com/search?q={generate_sentence()}')

def logout(driver,email):
    driver.get("https://login.live.com/logout.srf")
    print(f"Log Out From {email}")

def do_search(numOfSearch,numOfMobileSearch,email,password,pc,mobile):
    driver_pc = get_driver()
    login(driver_pc, email, password)
    driver_pc.refresh()
    time.sleep(10)
    if pc==True:
        print(totalPoints(driver_pc).text)
        search(driver_pc,numOfSearch,email,"PC")
        print("")
    if mobile==True:
        command = "Network.setUserAgentOverride"
        cmd_args = {"userAgent": MOBILE_USER_AGENT}
        driver_pc.execute_cdp_cmd(command, cmd_args)
        search(driver_pc,numOfMobileSearch,email,"Mobile")
        print("")
    logout(driver_pc,email)
    driver_pc.quit()

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

pc_numOfSearch = config.pc_numOfSearch
mobile_numOfSearch = config.mobile_numOfSearch
last4Digit = config.last4Digit
emails = config.emails
passwords = config.passwords
pcBool = config.pc_search
mobileBool = config.mobile_search
startNumber = config.startNumber
endtNumber = config.endNumber
if pc_numOfSearch <= 0:
    pcBool = False
if mobile_numOfSearch <= 0:
    mobileBool = False

for i in range(startNumber,len(emails)-endtNumber):
    email = emails[i]
    password = passwords[i]
    do_search(pc_numOfSearch, mobile_numOfSearch, email, password, pc=pcBool, mobile=mobileBool)

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


######## PRIVICY PAGE ###########
# BUTTON ID = id="id__0"
# TITLE = <span role="heading" aria-level="1" class="css-105">Your Microsoft account brings everything together&nbsp;</span>