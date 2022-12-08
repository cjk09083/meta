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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from subprocess import CREATE_NO_WINDOW 
from user_agent import generate_user_agent
from datetime import time, datetime, date, timedelta
from random import random, uniform, randint

import serial
import tkinter

def get_display_size():
    root = tkinter.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return height, width


PORT = "COM4"
BAUD = "115200"

KEYMAP = {
    '64' : 'w',     # top
    '66' : 'a',     # left
    '68' : 'x',     # center
    '67' : 'd',     # right
    '65' : 's',     # bottom
    }

ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 1)


WIDTH = 1920                         # 화면 너비
HEIGHT = 1080                        # 화면 높이

height, width = get_display_size()

ratio = [width/WIDTH, height/HEIGHT]


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

            option.add_argument('--no-sandbox')
            option.add_argument('--disable-dev-shm-usage')
            userAgent = generate_user_agent(navigator='chrome',os='win', device_type='desktop')
            
            print(userAgent)
            option.add_argument(f'user-agent={userAgent}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=option)
        except Exception as e:
            print("크롬 연결실패",e)

        targetUrl = 'http://m.naver.com'
        targetUrl = "게더타운 링크"
        targetUrl = "https://app.gather.town/app/WF84QVdIhiE0smuf/home"

        
        # driver.fullscreen_window()
        #driver.maximize_window()
        driver.implicitly_wait(10) # seconds
        driver.get(targetUrl)
        driver.fullscreen_window()
        self.driver = driver

        sleep(1)
        print("권한 허가 대기")
        wait = WebDriverWait(driver, 25)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-1j0npoo')))
        print(element,"준비됨")
        sleep(1)
        # driver.find_element(By.XPATH, '//button[text()="Some text"]').click()
        driver.find_element(By.CLASS_NAME, 'css-1j0npoo').click()
        sleep(1)
        

        print("이름 지정 대기")
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-bfov55')))
        print(element,"준비됨")
        sleep(1)
        userName = "test"+str(randint(1000,9999))
        driver.find_element(By.CLASS_NAME, 'css-1f19yvh').send_keys(userName)
        driver.find_element(By.CLASS_NAME, 'css-bfov55').click()
        sleep(1)

        print("Custom Room 입장")
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'GameCanvas-body')))
        sleep(1)
        print("화면 로딩됨")
        pyautogui.moveTo(298,159) ## 권한 수락
        sleep(uniform(0.1,0.5))
        pyautogui.click()
        sleep(uniform(0.1,0.5))
        try:
            driver.find_element(By.CLASS_NAME, 'css-1h5x3dy').click()
        except:
            print("카메라 혹은 마이크 연결됨")
        sleep(uniform(0.1,0.5))
        pyautogui.moveTo(0,height-1) ## 화면 밖으로
        
        print("리모콘 신호 대기")
        input_ms = datetime.now()
        while True:
            input_ms = self.getSignal(driver, input_ms)
            # driver.find_elements(By.TAG_NAME, "body")[0].send_keys("1")
            sleep(0.01)

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
        gt = GetherTown()

    except Exception as e:
        print(e)