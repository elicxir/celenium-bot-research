#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge import service
from selenium.webdriver.common.by import By
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
import pandas as pd
import extract_functions
import read_functions
from read_functions import wait_and_click,check_is_loaded,wait_and_send_keys
import logging





env = ".env"

load_dotenv(env)

user = os.environ.get("USER")
pw = os.environ.get("PASSWORD")


logpath = os.environ.get("LOGPATH")
summarypath = os.environ.get("SUMMARYPATH")
datadir = os.environ.get("DATADIR")

warnings.simplefilter('ignore')




#driverの準備
executable_path=r"/usr/local/bin/msedgedriver"
edge_service = service.Service(executable_path=executable_path)
options = Options()

## ユーザーエージェントの指定
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36' 
options.add_argument('--user-agent=' + UA)  ## ユーザーエージェントの設定

### その他optionsの指定
options.add_argument('--no-sandbox')  ## Sandboxの外でプロセスを動作させる
options.add_argument('--headless')  ## ブラウザを表示しない　CLIで起動する際は必須
options.add_argument('--disable-dev-shm-usage')  ## /dev/shmパーティションの使用を禁止し、パーティションが小さすぎることによる、クラッシュを回避する。

driver = webdriver.Edge(service=edge_service, options=options)












driver.get('https://dominion.games')

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
file_handler=logging.FileHandler(logpath)
logger.addHandler(file_handler)

# log in to dominion online
def login(user,pw):
    
    wait_and_send_keys(driver,logger,By.NAME,"username",user,tag="login_username")
    wait_and_send_keys(driver,None,By.NAME,"password",pw)
    wait_and_click(driver,logger,By.CLASS_NAME,"login-button",tag="login_button")


# 
def extract_log(game_id):
    print(f"extracting game id : {game_id}")
    
    # check can load game page
    check_is_loaded(driver,logger,By.CLASS_NAME,"lobby-page",tag="lobby page")
    
    # MyTable
    p="/html/body/div[2]/div/div/ul/li[2]/button"
    wait_and_click(driver,logger,By.XPATH,p,tag="MyTable")

    # Load Old Game
    wait_and_click(driver,logger,By.CLASS_NAME,"replay-button",tag="Load Old Game")

    # input game id 
    wait_and_send_keys(driver,logger,By.ID,"table-replay-id",game_id,tag="enter game ID")
    
    # load from end 
    p="/html/body/div[2]/div/div/div[1]/div/my-table/div[1]/div[1]/kingdom-rules/div/div[4]/div[2]"
    wait_and_click(driver,logger,By.XPATH,p,tag="load from end")
    
    time.sleep(1)
    p="/html/body/div[2]/div/div/div[1]/div/my-table/div[1]/div[1]/kingdom-rules/div/div[3]/input"
    num=driver.find_element(By.XPATH,p)
    n=num.get_attribute('value')
    
    if int(n) <60:
     
        p="/html/body/div[2]/div/div/div[1]/div/my-table/table-buttons/div/div[3]"
        wait_and_click(driver,logger,By.XPATH,p,tag="leave table")
        
        return False,None,None   
    
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
    
    
    # randomize player order 
    p="/html/body/div[2]/div/div/div[1]/div/my-table/div[1]/div[2]/participant-list/div/div[3]/div[2]"
    wait_and_click(driver,logger,By.XPATH,p,tag="randomize player order")

    # ready
    p="/html/body/div[2]/div/div/div[1]/div/my-table/table-buttons/div/div[1]"
    wait_and_click(driver,logger,By.XPATH,p,tag="ready")

    # check can load game page
    if not check_is_loaded(driver,logger,By.CLASS_NAME,"game-page",tag="game page"):
        
        p="/html/body/div[2]/div/div/div[1]/div/my-table/table-buttons/div/div[3]"
        wait_and_click(driver,logger,By.XPATH,p,tag="leave table")
        
        return False,None,None
        
        
    time.sleep(6)
    cd=extract_functions.get_card_list(driver)
    lg=extract_functions.get_log_raw(driver)

    
    # resigh
    p="/html/body/div[2]/div/div/metagame-buttons/div/div[7]/img"
    wait_and_click(driver,logger,By.XPATH,p,tag="resigh")
    
    # click resign yes
    p="/html/body/div[2]/div/div/modal-game-windows/resign-request/modal-window/div/div/ng-transclude/div[2]/button[1]"
    wait_and_click(driver,logger,By.XPATH,p,tag="resign yes")

    # click  yes
    p="/html/body/div[2]/div/div/modal-game-windows/game-ended-notification/modal-window/div/div/ng-transclude/button"
    wait_and_click(driver,logger,By.XPATH,p,tag="yes")

    # check can load game page
    if not check_is_loaded(driver,logger,By.CLASS_NAME,"score-page",tag="score page"):
        return False,None,None

    # score page exit
    p="/html/body/div[3]/div/score-table-buttons/div/button[2]"
    wait_and_click(driver,logger,By.XPATH,p,tag="score page exit")

    # check can load game page
    check_is_loaded(driver,logger,By.CLASS_NAME,"lobby-page",tag="lobby page")

    return len(cd)==17,lg,cd












header=["id","player_num","player1","player2","player3","player4",
        "supply1","supply2","supply3","supply4","supply5","supply6","supply7","supply8","supply9","supply10"]


basedf=pd.DataFrame(columns=header)

if os.path.isfile(summarypath):
    basedf=pd.read_csv(summarypath)

login(user,pw)

time.sleep(3)

for index in range(100000000,139000001):
        
    status,log,card=extract_log(index)
    
    # get log successfully
    if status:               
        ps=extract_functions.get_player_list(log)
        
        ps_fill=["","","",""]
        for i in range(len(ps)):
            ps_fill[i]=ps[i]
        
        dat=[index,len(ps)]+ps_fill+card[7:]
        df=pd.DataFrame([dat],columns=header)
        basedf=pd.concat([basedf,df])
        basedf.reset_index()
        print(basedf)
        
        logfile=datadir+str(index)+".txt"
        with open(logfile,"w") as f:
            f.write(log)
            
        basedf.to_csv(summarypath,index = False)

    index+=1
        