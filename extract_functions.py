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
import re

card_collection=[
    "Copper","Silver","Gold","Platinum","Estate","Duchy","Province","Colony","Curse","Cellar","Chapel","Moat","Harbinger",
    "Merchant","Vassal","Village","Workshop","Bureaucrat","Gardens","Militia","Moneylender","Poacher","Remodel","Smithy",
    "Throne Room","Bandit","Council Room","Festival","Laboratory","Library","Market","Mine","Sentry","Witch","Artisan"
]


# get card list
def get_card_list(webdriver):
    
    # Rearrange A according to the order of B
    def sort_according_to_order(A, B):
        index_dict = {value: index for index, value in enumerate(B)}
        sorted_A = sorted(A, key=lambda x: index_dict[x])
        return sorted_A
    
    p=f"//div[@class='card-stack-layer name-layer']"
    cards=webdriver.find_elements(By.XPATH,p)

    card_list=[c.text for c in cards]

    # extract unique and remove empty
    card_list=list(set(card_list))
    card_list=list(filter(None, card_list))

    card_list=sort_according_to_order(card_list, card_collection)

    #print(card_list)
    return card_list

# get raw log contents
def get_log_raw(webdriver):
    p="//div[@class='log-line-block']/span"
    lines=webdriver.find_elements(By.XPATH,p)

    # get text content
    loglines=[c.text.strip() for c in lines]
    # remove empty string
    loglines=list(filter(None, loglines))
    # join list elements and generate string
    lograw=' '.join(loglines)

    return lograw
    
def get_player_list(lograw:str):
    abbre=r'Coppers \. (.*?) starts with 3 Estates'

    ab_c=re.compile(abbre)

    abb_list = ab_c.findall(lograw)

    return abb_list
    