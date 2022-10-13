# python -m pip install selenium
# python -m pip install requests
# python -m pip install webdriver_manager
# python -m pip install user_agent
# python -m pip install pyautogui

import requests, math, pyautogui
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# from subprocess import CREATE_NO_WINDOW 
from user_agent import generate_user_agent
from datetime import time, datetime, date, timedelta
from random import random, uniform, randint
import numpy as np




WIDTH = 320                         # 화면 너비
HEIGHT = 720                        # 화면 높이

TITLE = "게더타운"

class GetherTown():
    def __init__(self):
        super().__init__()
        print("init")
        self.Open()
        
    def Open(self):
        print("게더타운 오픈")
        try:
            option = webdriver.ChromeOptions()
            option.add_experimental_option("useAutomationExtension", False)     
            option.add_experimental_option("excludeSwitches", ['enable-automation'])

            # 봇으로 의심받지 않게 User-agent 추가
            option.add_argument('--no-sandbox')
            option.add_argument('--disable-dev-shm-usage')
            userAgent = generate_user_agent(navigator='chrome',os='win', device_type='desktop')

            print(userAgent)
            option.add_argument(f'user-agent={userAgent}')
            
            service = Service("/usr/lib/chromium-browser/chromedriver")
            driver = webdriver.Chrome(service=service, options=option)
        except Exception as e:
            print("크롬 연결실패",e)

        targetUrl = 'http://m.naver.com'
        targetUrl = "https://app.gather.town/app/WF84QVdIhiE0smuf/home"
        targetUrl = "https://zep.us/play/yxWJjz"
        
        #driver.fullscreen_window()
        #driver.maximize_window()
        driver.implicitly_wait(10) # seconds
        driver.get(targetUrl)
        
        self.driver = driver
        
        #sleep(100)
        for i in range (1000):
            sleep(1)
            driver.find_elements(By.TAG_NAME, "body")[0].send_keys("1")
            ActionChains(driver).key_down("s").pause(0.1).key_up("s").perform()
            print("sendKeys")
            
    
    def Close(self):
        driver = self.driver
        print('종료 3초전')
        sleep(1)
        print('종료 2초전')
        sleep(1)
        print('종료 1초전')
        sleep(1)
        print('종료')
        driver.quit()

    def rand_sec(self, start,end):
        result = uniform(start, end)
        return result            

if __name__ == "__main__" :
    try:
        gt = GetherTown()

    except Exception as e:
        print(e)
