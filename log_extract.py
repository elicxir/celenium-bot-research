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

url="file:///c:/Users/moriyoshi/Documents/research/celenium-bot-research/logtest.html"
driver.get(url)


lines=driver.find_elements(By.CLASS_NAME,"log-line")
print(len(lines))

for l in range(len(lines)):
    p=f"/html/body/div[2]/div/div/game-area/div[7]/div/div/div[{l}]//div[@class='log-line-block']/span"
    e=driver.find_elements(By.XPATH,p)

    t=""

    for w in e:
        t+=w.text+" "

    print(t)
    pass

input()