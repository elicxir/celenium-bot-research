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


import logging


def wait_and_send_keys(webdriver,log:logging.Logger,by,value,keys,tag="",waittime=5,sleep=0.5):
    if log:
        if tag:    
            log.debug(f"{tag} : send key {keys} ")
        else:
            log.debug(f"send key {keys} to ({by} {value})")
        
        
    try:
        wait = WebDriverWait(webdriver, waittime)
        element = wait.until(EC.element_to_be_clickable((by,value)))
        element.send_keys(keys)
        time.sleep(sleep)
    except TimeoutException as e:
        if log:
            if tag:    
                log.debug(f"{tag} : timeout")
            else:
                log.debug(f"timeout in find {by} {value}")
        raise 
    except :
        if log:
            if tag:    
                log.debug(f"{tag} : error")
            else:
                log.debug(f"error in find {by} {value}")


def wait_and_click(webdriver,log:logging.Logger,by,value,tag="",waittime=5,sleep=0.5):
    if log:
        if tag:    
            log.debug(f"{tag} : click")
        else:
            log.debug(f"click ({by} {value})")

    try:
        wait = WebDriverWait(webdriver, waittime)
        element = wait.until(EC.element_to_be_clickable((by,value)))
        element.click()
        time.sleep(sleep)
    except TimeoutException as e:
        if log:
            if tag:    
                log.debug(f"{tag} : timeout")
            else:
                log.debug(f"timeout in find {by} {value}")
        raise 
    except :
        if log:
            if tag:    
                log.debug(f"{tag} : error")
            else:
                log.debug(f"error in find {by} {value}")


# 
# True: can load page successfully
# False:cant load page
def check_is_loaded(webdriver,log:logging.Logger,by,value,tag="",waittime=8,sleep=0.5):
    if log:
        if tag:    
            log.debug(f"{tag} : try to loading")
        else:
            log.debug(f"try to loading ({by} {value})")
    try:
        wait = WebDriverWait(webdriver, waittime)
        page = wait.until(EC.element_to_be_clickable((by,value)))
        if log:
            if tag:    
                log.debug(f"{tag} : load success")
            else:
                log.debug(f"success loading ({by} {value})")
        time.sleep(sleep)
        return True
    except TimeoutException as e:
        if log:
            if tag:    
                log.debug(f"{tag} : failed to load")
            else:
                log.debug(f"failed to load ({by} {value})")
        return False
    except:
        if log:
            if tag:    
                log.debug(f"{tag} : failed to load")
            else:
                log.debug(f"failed to load ({by} {value})")
        return False