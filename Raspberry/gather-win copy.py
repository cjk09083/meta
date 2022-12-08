# python -m pip install selenium
# python -m pip install requests
# python -m pip install webdriver_manager
# python -m pip install user_agent
# python -m pip install pyautogui
# python -m pip install beautifulsoup4 lxml

import requests, math, pyautogui
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# from subprocess import CREATE_NO_WINDOW 
from user_agent import generate_user_agent
from datetime import time, datetime, date, timedelta
from random import random, uniform, randint

import serial, keyboard
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


gatherUrl = "https://app.gather.town/app/MgIuTVsBpnepb1I6/1225"
gatherUrl = "https://app.gather.town/app/tpxShwZn97RLCqMm/cjk09083"
blackUrl = "https://cjk09083.cafe24.com/gather/black.html"

PORT = "COM4"
BAUD = "115200"

KEYMAP = {
    '64' : 'w',     # top
    '66' : 'a',     # left
    '68' : 'x',     # center
    '67' : 'd',     # right
    '65' : 's',     # bottom
    }

# ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 1)


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

            # option.add_argument('--user-data-dir=chrome-data')
            option.add_argument('--no-sandbox')
            option.add_argument('--disable-dev-shm-usage')
                        
            # option.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
            option.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
            userAgent = generate_user_agent(navigator='chrome',os='win', device_type='desktop')
            
            print(userAgent)
            option.add_argument(f'user-agent={userAgent}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=option)
        except Exception as e:
            print("크롬 연결실패",e)

        targetUrl = 'http://m.naver.com'
        targetUrl = "https://app.gather.town/app/WF84QVdIhiE0smuf/home"
        targetUrl = "https://cjk09083.cafe24.com/gather/black.html"

        # driver.fullscreen_window()
        #driver.maximize_window()
        driver.implicitly_wait(10) # seconds
        driver.get(blackUrl)
        # driver.fullscreen_window()
        self.driver = driver
        wait = WebDriverWait(driver, 25)
        # driver.find_element(By.TAG_NAME, 'body  ').send_keys(Keys.F11)
        self.gatherMode = True
        size = driver.get_window_size()
        width = size.get("width")
        height = size.get("height")
        pyautogui.moveTo(0,height-1) ## 절대좌표
        sleep(1)
        print("goBlack")
        self.goBlack()

    def goBlack(self):
        if not self.gatherMode:
            return False

        self.gatherMode = False
        driver = self.driver
        driver.get(blackUrl)
        # driver.fullscreen_window()
        print("Black page: 신호대기중")
        while True:
            key = keyboard.read_key() 
            print("black page: "+key)
            if(key == '-'):
                element = driver.find_element(By.TAG_NAME, 'body')
                driver.execute_script("arguments[0].innerHTML = '<h1 style=\"color: white; margin: auto;\">게더타운으로 이동합니다..</h1>';",element)
                print("goGather")
                if self.goGather():
                    break
            sleep(0.1)

    def goGather(self):
        if self.gatherMode:
            return False

        self.gatherMode = True
        driver = self.driver
        driver.get(gatherUrl)
        # driver.fullscreen_window()
        sleep(1)
        print("권한 허가 대기")
        wait = WebDriverWait(driver, 25)
        userName = "user"+str(randint(1000,9999))
        NeedRequest = True
        NeedJoin = True
        NeedEdit = True

        tryNum = 0
        while True:
            tryNum += 1
            if NeedRequest:
                try:
                    element = driver.find_element(By.CLASS_NAME, 'css-1j0npoo')
                    print("Request Btn 준비됨")
                    element.click()
                    NeedRequest = False
                except:
                    print('Wait for Request',tryNum)

            if NeedEdit:
                try:
                    element = driver.find_element(By.CLASS_NAME, 'css-s85wzu')
                    print("Edit Btn 준비됨")
                    element.click()
                    NeedEdit = False
                    break
                except:
                    print('Wait for Edit',tryNum)

            if tryNum > 10:
                break
                
            sleep(1)

        print("캐릭터 커스텀창 대기")
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-oleig8')))
        print("캐릭터 커스텀창 로딩 완료")

        self.btnCategory = 0
        self.btnIndex = [2,0,0,0]
        allItems = []
        itemsCnt = 0
        allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, True)

        while True:
            key = keyboard.read_key()
            print(key)
            if(key == 'enter'):
                element = driver.find_element(By.CLASS_NAME, 'css-5mqzab')
                element.click()
                print("Enter")
                break
            elif(key == 'a'):
                self.btnIndex[self.btnCategory] -= 1
                if self.btnIndex[self.btnCategory] < 0:
                    self.btnIndex[self.btnCategory] = itemsCnt-1
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, True)
            elif(key == 'd'):
                self.btnIndex[self.btnCategory] += 1
                if self.btnIndex[self.btnCategory] == itemsCnt:
                    self.btnIndex[self.btnCategory] = 0
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, True)
            elif(key == 's'):
                self.btnCategory += 1
                if self.btnCategory > 3:
                    self.btnCategory = 3
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, False)
            elif(key == 'w'):
                self.btnCategory -= 1
                if self.btnCategory < 0:
                    self.btnCategory = 0
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, False)
            sleep(0.1)

        sleep(1)
        tryNum = 0
        while True:
            tryNum += 1
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
                    print('Wait for Join',tryNum)

            if tryNum > 10:
                break
                
            sleep(1)
        
        print('화면 로딩 대기')
        
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'GameCanvas-body')))
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
        inGame = False
        self.gameMode = False
        
        insert_ms = 50 / 1000

        while True:
            if not self.gameMode:
                key = keyboard.read_key()
                print(key)
                if(key == '='):
                    self.goBlack()
                    print("goBlack")
                    break
                elif(key == 'x'):
                    iframeList = driver.find_elements(By.TAG_NAME,'iframe')
                    print("ifame",len(iframeList),"개")
                    if(len(iframeList) > 0):
                        if self.goGame(iframeList):
                            continue

            sleep(insert_ms)
            # input_ms, key = self.getSignal(driver, input_ms)
            
    def moveCustom(self, allItems, itemsCnt, search):
        driver = self.driver
        wait = WebDriverWait(driver, 25)
        print("커스텀 커서 이동",self.btnCategory,self.btnIndex[self.btnCategory]+1,"/",itemsCnt,
                    search,self.btnIndex)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-1xytt4v')))
        if itemsCnt > 0:
            selectedItem = allItems[self.btnCategory][self.btnIndex[self.btnCategory]]
            if not search:
                driver.execute_script("arguments[0].setAttribute('style', 'background:white')", selectedItem)
                sleep(0.1)
                driver.execute_script("arguments[0].setAttribute('style', 'background:')", selectedItem)
            selectedItem.click()

        if (self.btnCategory < 3 ) or itemsCnt == 0:
            if self.btnCategory == 0:
                if self.btnIndex[self.btnCategory] == 0:
                    self.btnIndex = [self.btnIndex[0],0,2,0]
                else:
                    self.btnIndex = [self.btnIndex[0],0,0,0]
            elif self.btnCategory == 1:
                self.btnIndex = [self.btnIndex[0],self.btnIndex[1],0,0]


            sample_button = driver.find_elements(By.CSS_SELECTOR, '.css-ix8tkr')[0]
            categoryDiv = sample_button.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
            print("카테고리 div 확인",categoryDiv)
            buttonList = categoryDiv.find_elements(By.TAG_NAME,'button')
            print("카테고리 하위 button : ",len(buttonList))

            colorBtn = categoryDiv.find_element(By.XPATH, '..')
            colorDiv = colorBtn.find_elements(By.CLASS_NAME,'Layout')
            print("colorDiv",len(colorDiv))
            colorList = colorDiv[3].find_elements(By.TAG_NAME,'button')
            print("colorList : ",len(colorList),"idx:",self.btnIndex[0])
            
            itemsDiv = driver.find_element(By.CLASS_NAME, 'css-1xytt4v')
            itemList = itemsDiv.find_elements(By.TAG_NAME,'button')
            print("itemList : ",len(itemList))
            # else:
            #     colorList = allItems[2]
            #     itemList = allItems[3]

            first = buttonList[:4]
            second = buttonList[4:]
            colors = colorList
            items = itemList

            allItems = [first, second, colors, items]

        itemsCnt = len(allItems[self.btnCategory])

        return allItems, itemsCnt


    def goGame(self, iframeList):
        driver = self.driver
        self.gameMode = True
        print("게임모드에 진입")
        sleep(1)

        for i, iframe in enumerate(iframeList):
            gameUrl = iframe.get_attribute('src').split('/')[-1]
            # gamdId = iframe.get_attribute('id')
            print(gameUrl, "스위칭")
            driver.switch_to.frame(iframe)
            sleep(2)
            gamePage = driver.find_elements(By.TAG_NAME,'span')
            print("게임 클릭",len(gamePage))
            gamePage[0].click()
            driver.execute_script("arguments[0].setAttribute('style', 'display:none')", gamePage[0])
            # iframe.click()

            print("키 입력 대기")
            while True:
                key = keyboard.read_key()
                print(key)

                if(key == 'esc'):
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME,'css-fib3fn').click()
                    self.gameMode = False
                    print("ifame 복귀")
                    break

        # gamearea << 게임 영역
        # css-fib3fn <<< 게임 종료 버튼


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
        return output_ms, key
    
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