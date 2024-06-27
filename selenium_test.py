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

import extract_functions
import read_functions
from read_functions import wait_and_click,wait_and_delegate,wait_and_send_keys
import logging

env = ".env"

load_dotenv(env)

user = os.environ.get("USER")
pw = os.environ.get("PASSWORD")

warnings.simplefilter('ignore')

driver = webdriver.Edge()  
driver.get('https://dominion.games')

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


# log in to dominion online
def login(user,pw):
    
    wait_and_send_keys(driver,logger,By.NAME,"username",user,tag="login_username")
    wait_and_send_keys(driver,None,By.NAME,"password",pw)
    wait_and_click(driver,logger,By.CLASS_NAME,"login-button",tag="login_button")


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
    wait_and_click(driver,logger,By.CLASS_NAME,"replay-button",tag="Load Old Game")

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
        print("cant collect game data")
        return 
    except:
        print("game page loading  error") 
        
        
    time.sleep(1)
    
    lg=extract_functions.get_log_raw(driver)
    cd=extract_functions.get_card_list(driver)
    ps=extract_functions.get_player_list(lg)
    
    print(lg)
    print(cd)
    print(ps)
    
    time.sleep(1)
    # resigh
    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[2]/div/div/metagame-buttons/div/div[7]/img"
        resigh = wait.until(EC.element_to_be_clickable((By.XPATH,p)))
        resigh.click()
    except TimeoutException as e:
        print("resigh timeout")
    except:
        print("resigh error")     
        
    time.sleep(1)
    
    # click resign yes
    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[2]/div/div/modal-game-windows/resign-request/modal-window/div/div/ng-transclude/div[2]/button[1]"
        resigh = wait.until(EC.element_to_be_clickable((By.XPATH,p)))
        resigh.click()
    except TimeoutException as e:
        print("resigh timeout")
    except:
        print("resigh error")    

    time.sleep(1)

    # click  yes
    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[2]/div/div/modal-game-windows/game-ended-notification/modal-window/div/div/ng-transclude/button"
        resigh = wait.until(EC.element_to_be_clickable((By.XPATH,p)))
        resigh.click()
    except TimeoutException as e:
        print("resigh timeout")
    except:
        print("resigh error") 

    time.sleep(1)





    # check can load game page
    try:
        wait = WebDriverWait(driver, 15)
        scorepage = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"score-page")))
        print("score page loading success ")
    except TimeoutException as e:
        print("score page loading timeout")  
    except:
        print("score page loading  error") 








    try:
        wait = WebDriverWait(driver, 10)
        p="/html/body/div[3]/div/score-table-buttons/div/button[2]"
        resigh = wait.until(EC.element_to_be_clickable((By.XPATH,p)))
        resigh.click()
    except TimeoutException as e:
        print("resigh timeout")
    except:
        print("resigh error") 

    time.sleep(2)

    # check can load game page
    try:
        wait = WebDriverWait(driver, 15)
        lobbypage = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"lobby-page")))
        print("lobby page loading success ")
    except TimeoutException as e:
        print("lobby page loading timeout")  
    except:
        print("lobby page loading  error") 




login(user,pw)
extract_log(139960001)
time.sleep(2)
extract_log(139960000)
