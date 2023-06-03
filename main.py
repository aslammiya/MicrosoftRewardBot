from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
import config
import os

PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 11.0; SM-M30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36'
PATH_OF_DRIVER = "C:\\Users\\aslam\\chromedriver_win32\\chromedriver.exe"

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
    print(f">> Email {email}")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    print(f">> Password {password}")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
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

    driver.get(f'https://www.bing.com/')
    hideLines(3)
    print(f"\nLog In To {email}")
    # time.sleep(30000)

def hideLines(num_lines):
    for _ in range(num_lines):
        print("\033[F\033[K", end='')

def generate_sentence():
    sentence_length = random.randint(3, 10)
    sentence = ' '.join(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 8))) for _ in range(sentence_length))
    return sentence

def totalPoints(driver):
    driver.refresh()
    time.sleep(3)
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@id="id_rc"]')))

def checkLogin(driver,name):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_n")))
    text = str(element.text)
    if text == name and text.strip() != "":
        print(text,"Login checked successfull")
        return True
    else:
        time.sleep(5)
        if text == name and text.strip() != "":
            print(text,"Login checked successfull")
            return True
        print("Login check failed ", name, text)
        return False

def search(driver,numOfSearch,email,mode):
    for i in range(numOfSearch):
        print(f"\r{email} {mode} Search : {i+1}/{numOfSearch}", end="")
        driver.get(f'https://www.bing.com/search?q={generate_sentence()}')

def logout(driver,email):
    driver.get("https://login.live.com/logout.srf")
    print(f"Log Out From {email}")

def do_search(numOfSearch,numOfMobileSearch,email,password,pc,mobile,name):
    driver_pc = get_driver()
    login(driver_pc, email, password)
    driver_pc.refresh()
    time.sleep(3)
    if checkLogin(driver_pc,name) == True:
        pass
    else:
        time.sleep(10)
    if pc==True:
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

def is_list_empty(lst):
    if not lst:
        return True
    else:
        return False

pc_numOfSearch = config.pc_numOfSearch
mobile_numOfSearch = config.mobile_numOfSearch
last4Digit = config.last4Digit
emails = config.emails
passwords = config.passwords
pcBool = config.pc_search
mobileBool = config.mobile_search
startNumber = config.startNumber
endNumber = config.endNumber
expect = config.expect
names = config.names
if pc_numOfSearch <= 0:
    pcBool = False
if mobile_numOfSearch <= 0:
    mobileBool = False
onlyValue = config.only
newBees = config.newBees
newBeesStart = config.newBeesStart

errAcc = []
for i in range(startNumber, len(emails) - endNumber):
    if newBees == True:
        if i == newBeesStart:
            mobileBool = False
            pc_numOfSearch = 12
    try:
        if i in expect:
            continue
        if is_list_empty(onlyValue) == False:
            if i in onlyValue:
                email = emails[i]
                password = passwords[i]
                name = names[i]
                do_search(pc_numOfSearch, mobile_numOfSearch, email, password, pc=pcBool, mobile=mobileBool, name=name)
        else:
            email = emails[i]
            password = passwords[i]
            name = names[i]
            # print(f"Email : {email}\nPassw : {password}\nPC NO. {pc_numOfSearch}\nMobile No. {mobile_numOfSearch}\nPC Bool {pcBool}\nMobile Bool {mobileBool}\n")
            do_search(pc_numOfSearch, mobile_numOfSearch, email, password, pc=pcBool, mobile=mobileBool, name=name)
    except Exception as er:
        print(f"Error! {email}")
        errAcc.append(i)
        continue

print(errAcc)
for i in range(3):
    if is_list_empty(errAcc) == True:
        break
    for i in range(startNumber, len(emails) - endNumber):
        try:
            if i in errAcc:
                email = emails[i]
                password = passwords[i]
                name = names[i]
                do_search(pc_numOfSearch, mobile_numOfSearch, email, password, pc=pcBool, mobile=mobileBool, name=name)
                errAcc.remove(i)
        except Exception as er:
            print(f"Error! {email}")
            continue
    print(errAcc)
    
if config.shutdown == True:
    os.system("shutdown /s /t 0")

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