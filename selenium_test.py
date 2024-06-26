from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import warnings
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

env = ".env"

load_dotenv(env)

user = os.environ.get("USER")
pw = os.environ.get("PASSWORD")

warnings.simplefilter('ignore')

driver = webdriver.Edge()  
driver.get('https://dominion.games')



# log in to dominion online
def login(user,pw):
    
    try:
        wait = WebDriverWait(driver, 10)
    
        username = wait.until(EC.element_to_be_clickable((By.NAME,"username")))
        password = wait.until(EC.element_to_be_clickable((By.NAME,"password")))
        loginbutton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"login-button")))
        
    except TimeoutException as e:
        print("loading timeout")
        
    username.send_keys(user)
    password.send_keys(pw)
    loginbutton.click()

    


def extract_log(game_id):
    print(f"extracting game id : {game_id}")
    
    # MyTable
    try:
        wait = WebDriverWait(driver, 10)
        lobbytabs = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"lobby-tabs")))
    except TimeoutException as e:
        print("loading timeout")    

    tabs=driver.find_elements(By.CLASS_NAME,"tab-button")
    tabs[1].click()
    time.sleep(1)

    # Load Old Game
    try:
        wait = WebDriverWait(driver, 10)
        loadgame = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"replay-button")))
    except TimeoutException as e:
        print("loading timeout")    

    # 新規卓 をクリック
    loadgame.click()
    time.sleep(1)


    # input game id 
    try:
        wait = WebDriverWait(driver, 10)
        gameid = wait.until(EC.element_to_be_clickable((By.ID,"table-replay-id")))
    except TimeoutException as e:
        print("loading timeout")    

    gameid.send_keys(game_id)
    time.sleep(1)

    
    # load from end 
    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[2]/div/div/div[1]/div/my-table/div[1]/div[1]/kingdom-rules/div/div[4]/div[2]"
        loadfromend = wait.until(EC.element_to_be_clickable((By.XPATH,p)))
    except TimeoutException as e:
        print("loading timeout")    

    loadfromend.click()
    time.sleep(2)
    
    # add bot
    try:
        wait = WebDriverWait(driver, 10)
        addbot = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"table-add-bot-icon")))
    except TimeoutException as e:
        print("add bot timeout error")    
        
    time.sleep(1)
    addboticons=driver.find_elements(By.CLASS_NAME,"table-add-bot-icon")
    
    for bot in addboticons:
        bot.click()

    time.sleep(1)
    
    return
    
    # ready
    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[2]/div/div/div[1]/div/my-table/table-buttons/div/div[1]"
        ready = wait.until(EC.element_to_be_clickable((By.XPATH,p)))
        ready.click()
    except TimeoutException as e:
        print("ready loading timeout")
    except:
        print("ready error") 
    
    
    # check can load game page
    try:
        wait = WebDriverWait(driver, 15)
        gamepage = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"game-page")))
        print("game page loading success ")
    except TimeoutException as e:
        print("game page loading timeout")  
    except:
        print("game page loading  error") 

    # log scroll get
    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[2]/div/div/game-area/div[7]/div/div"
        log_scroll = driver.find_element()
        ready.click()
    except TimeoutException as e:
        print("ready loading timeout")
    except:
        print("ready error")     
    
    
    
    
    


login(user,pw)
extract_log(139960000)

input()