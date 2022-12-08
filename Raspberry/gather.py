# python -m pip install selenium requests webdriver_manager user_agent
# sudo apt install chromium-chromedriver

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# from subprocess import CREATE_NO_WINDOW
from user_agent import generate_user_agent
from datetime import time, datetime, date, timedelta
from random import random, uniform, randint
import numpy as np

import serial

PORT = "/dev/ttyACM0"
BAUD = "115200"

ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 1)

KEYMAP = {
    '64' : 'w', # up
    '65' : 's', # down 
    '66' : 'a', # left
    '67' : 'd', # right
    '68' : 'x', # ok
    }

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
            option.add_argument('--user-data-dir=chrome-data')
            option.add_argument('--no-sandbox')
            option.add_argument('--disable-dev-shm-usage')
            userAgent = generate_user_agent(navigator='chrome',os='win', device_type='desktop')
            # userAgent = generate_user_agent(navigator='chrome', device_type='smartphone')
            # userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
            
            print(userAgent)
            option.add_argument(f'user-agent={userAgent}')
            
            service = Service('/usr/lib/chromium-browser/chromedriver')
            driver = webdriver.Chrome(service=service, options=option)
        except Exception as e:
            print("크롬 연결실패",e)

        targetUrl = 'http://m.naver.com'
        targetUrl = "https://app.gather.town/app/WF84QVdIhiE0smuf/home"
        # targetUrl = "https://zep.us/play/yxWJjz"
        
        # driver.fullscreen_window()
        #driver.maximize_window()
        driver.implicitly_wait(10) # seconds
        driver.get(targetUrl)
        driver.fullscreen_window()
        self.driver = driver
        sleep(1)
        print("권한 허가 대기")
    
        wait = WebDriverWait(driver, 25)
        userName = "test"+str(randint(1000,9999))
        NeedRequest = True
        NeedJoin = True
        
        while True:
            if NeedRequest:
                try:
                    element = driver.find_element(By.CLASS_NAME, 'css-1j0npoo')
                    print("Request Btn 준비됨")
                    element.click()
                    NeedRequest = False
                except:
                    print('Wait for Request')
            if NeedJoin:
                try:
                    element = driver.find_element(By.CLASS_NAME, 'css-bfov55')
                    print("Join Btn 준비됨",userName)
                    NameField = driver.find_element(By.CLASS_NAME, 'css-1f19yvh')
                    NameField.send_keys(Keys.CONTROL + 'a')
                    NameField.send_keys(Keys.DELETE)
                    NameField.send_keys(userName)
                    NeedJoin = False
                    element.click()
                    break
                except:
                    print('Wait for Join')
                
            sleep(1)

        print('화면 로딩 대기')
        
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'GameCanvas-body')))
        print("화면 로딩됨")
        # pyautogui.moveTo(298,159) ## 절대좌표
        # sleep(uniform(0.1,0.5))
        # pyautogui.click()
        # sleep(uniform(0.1,0.5))
        # pyautogui.moveTo(0,1079) ## 절대좌표
        
        
        sleep(uniform(0.1,0.5))
        try:
            driver.find_element(By.CLASS_NAME, 'css-1h5x3dy').click()
        except:
            print("카메라 혹은 마이크 연결됨")
        sleep(uniform(0.1,0.5))

        
        print("리모콘 신호 대기")
        input_ms = datetime.now()
        start_ms = input_ms
        now_ms = input_ms
        while True:
            input_ms = self.getSignal(driver, input_ms)
            
            ''' 
            duration = (datetime.now() - start_ms).total_seconds() * 1000
            if duration > 100:
                start_ms = datetime.now()
                try:
                    driver.find_element(By.CLASS_NAME, 'css-1h5x3dy').click()
                except:
                    print("카메라 혹은 마이크 연결됨",duration)
            '''
            
            # driver.find_elements(By.TAG_NAME, "body")[0].send_keys("1")
            # print('Move left')
            # ActionChains(driver).key_down('a').pause(0.05).key_up('a').perform()
            # sleep(1)

            # currentPos = pyautogui.position()
            # print(driver.title,"마우스 현재 좌표:",currentPos.x,currentPos.y)
            # sleep(1)

    def getSignal(self, driver, then):
        output_ms = then
        if ser.readable():
            res = ser.readline().strip().decode('utf-8')
            if res and res != '0':
                code = res
                # print(code)
                try:
                    key = KEYMAP[code]
                except KeyError:
                    key = "ERROR"

                duration = (datetime.now() - then).total_seconds() * 1000
                print(key,"(",str(code),")",duration,"ms")

                if key != 'ERROR' and duration > 50:
                    ActionChains(driver).key_down(key).pause(0.05).key_up(key).perform()
                    output_ms = datetime.now()
                    
                    
        return output_ms
    
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
        print('NFC TAG ON')
        gt = GetherTown()

    except Exception as e:
        print(e)

