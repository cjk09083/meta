# python -m pip install selenium
# python -m pip install requests
# python -m pip install user_agent
# python -m pip install pyautogui
# python -m pip install beautifulsoup4 lxml
# python -m pip install webdriver_manager

import serial, pyautogui
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# from subprocess import CREATE_NO_WINDOW 
from user_agent import generate_user_agent
from datetime import time, datetime, date, timedelta
from random import random, uniform, randint


"""
버블버블    : https://cjk09083.cafe24.com/gather/bublbobl/bublbobl.html

갤러그      : https://cjk09083.cafe24.com/gather/galaga/galaga.html

테트리스    : https://cjk09083.cafe24.com/gather/tetris/tetris.html
"""

gatherUrl = "https://app.gather.town/app/rdFosTQmwzU9IZl3/jjjjj"
gatherUrl = "https://app.gather.town/app/tpxShwZn97RLCqMm/cjk09083"
blackUrl = "https://cjk09083.cafe24.com/gather/black.html"

KEYMAP = {
    '60' : 'power',         # Power
    '11' : Keys.UP,         # Up
    '12' : Keys.DOWN,       # Down
    '13' : Keys.LEFT,       # Left
    '14' : Keys.RIGHT,      # Right
    '20' : 'back',          # Back
    '21' : 'mute',          # Mute
    '22' : 'end',           # End
    '23' : '3',             # 3
    '30' : '6',             # 6
    '31' : 'e',             # E
    '32' : 'g',             # G
    '33' : 'x',             # X
    '34' : 'z',             # Z
    '41' : 'start',         # Start
    '42' : 'select',        # Select
    '43' : Keys.CONTROL,    # B
    '44' : Keys.ALT,        # A
    }
    

KEYMAP_STR = {
    '60' : 'power', # Power
    '11' : 'UP',    # Up
    '12' : 'DOWN',  # Down
    '13' : 'LEFT',  # Left
    '14' : 'RIGHT', # Right
    '20' : 'back',  # Back
    '21' : 'mute',  # Mute
    '22' : 'end',   # End
    '23' : '3',     # 3
    '30' : '6',     # 6
    '31' : 'e',     # E
    '32' : 'g',     # G
    '33' : 'x',     # X
    '34' : 'z',     # Z
    '41' : 'start', # Start
    '42' : 'select',# Select
    '43' : 'b',     # B
    '44' : 'a',     # A
    }


PORT = "COM5"
# PORT = "/dev/ttyACM0"
BAUD = "115200"
ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 0.1)

GAME_URL = [
    'bublbobl.html',
    'galaga.html',
    'tetris.html',
]


TITLE = "게더타운"

ext_file = 'C:/Users/USER/Downloads/extension.zip'
# ext_file = '/usr/lib/extension.zip'
driver_path = "C:/Users/USER/Downloads/chromedriver.exe"
# driver_path = '/usr/lib/chromium-browser/chromedriver'

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
            option.add_extension(ext_file)     # 음소거 익스텐션 추가

            # option.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
            option.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
            userAgent = generate_user_agent(navigator='chrome',os='win', device_type='desktop')
            
            print(userAgent)
            option.add_argument(f'user-agent={userAgent}')
            
            # service = Service(ChromeDriverManager().install())
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=option)
        except Exception as e:
            print("크롬 연결실패",e)

        # driver.implicitly_wait(10) # seconds
        driver.get(blackUrl)
        self.driver = driver
        wait = WebDriverWait(driver, 25)
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
        input_ms = datetime.now()
        key = ''

        while True:
            input_ms, key, code = self.getSignal(driver, input_ms)
            if code == 0 :
                continue

            if code < 60  :
                element = driver.find_element(By.TAG_NAME, 'body')
                driver.execute_script("arguments[0].innerHTML = '<h1 style=\"color: white; margin: auto;\">게더타운으로 이동합니다</h1>';",element)
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
        sleep(1)

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

            if tryNum > 20:
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
        input_ms = datetime.now()
        key = ''

        while True:
            input_ms, key, code = self.getSignal(key, input_ms)
            if code == 0 :
                continue

            # key = keyboard.read_key()
            # print(key)
            if(key == 'start'):
                try:
                    element = driver.find_element(By.CLASS_NAME, 'css-5mqzab')
                    element.click()
                    print("Start gather Request")
                    break
                except:
                    print(Exception)
            elif(code == 13):           # 좌
                self.btnIndex[self.btnCategory] -= 1
                if self.btnIndex[self.btnCategory] < 0:
                    self.btnIndex[self.btnCategory] = itemsCnt-1
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, False)
            elif(code == 14):           # 우
                self.btnIndex[self.btnCategory] += 1
                if self.btnIndex[self.btnCategory] == itemsCnt:
                    self.btnIndex[self.btnCategory] = 0
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, False)
            elif(code == 12):           # 하
                self.btnCategory += 1
                if self.btnCategory > 3:
                    self.btnCategory = 3
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, True)
            elif(code == 11):           # 상
                self.btnCategory -= 1
                if self.btnCategory < 0:
                    self.btnCategory = 0
                allItems, itemsCnt = self.moveCustom(allItems, itemsCnt, True)
            sleep(0.1)

        sleep(0.1)
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
        ghost_ms = 0
        arrow_ms = 0
        key = ''
        before_key = ''
        before_code = 0
        start_ms = input_ms
        now_ms = input_ms
        inGame = False
        self.gameMode = False
        insert_ms = 50 / 1000
        isMoved = False
        Searching = False
        needSearch = False
        exitBtn = ''

        while True:
            if not self.gameMode:
                input_ms, key, code = self.getSignal(key, input_ms)
                if ghost_ms != 0:
                    duration = (datetime.now() - ghost_ms).total_seconds() * 1000 
                    if duration> 500:
                        print("Ghost 종료",duration)
                        ActionChains(driver).key_up('g').perform()
                        ghost_ms = 0
                if arrow_ms != 0:
                    duration = (datetime.now() - arrow_ms).total_seconds() * 1000 
                    if duration> 150:
                        ActionChains(driver).key_up(before_key).perform()
                        print("키보드",KEYMAP_STR[str(before_code)],"키 뗌",int(duration),"ms")
                        arrow_ms = 0

                if code == 0 :
                    continue

                # key = keyboard.read_key()
                # print(key)
                if code < 20:
                    if before_key != key and before_key != '':
                        print("키보드",KEYMAP_STR[str(before_code)],"키 뗌")
                        ActionChains(driver).key_up(before_key).perform()

                    print("키보드",KEYMAP_STR[str(code)],"키 누름")
                    ActionChains(driver).key_down(key).perform()
                    before_key = key
                    before_code = code
                    arrow_ms = datetime.now()
                elif code < 30:
                    print("음소거")
                    pyautogui.FAILSAFE = False
                    pyautogui.hotkey('alt', 'shift', 'm')            
                elif code < 40:
                    isMoved = True
                    if key == 'g':
                        print("Ghost 시작")
                        ActionChains(driver).key_down(key).perform()
                        ghost_ms = datetime.now()
                    else:    
                        ActionChains(driver).key_down(key).pause(0.05).key_up(key).perform()
                        if key == 'x' and not Searching:
                            print("닫기 버튼 검색",code)
                            Searching = True
                            try:
                                sleep(0.1)
                                btnList = driver.find_elements(By.TAG_NAME,'button')
                                print("Btn 검색",len(btnList))
                                if len(btnList) > 14:

                                    print("iframe 검색")
                                    iframeList = driver.find_elements(By.TAG_NAME,'iframe')
                                    print("iframe",len(iframeList),"개")
                                    if(len(iframeList) > 0):
                                        # exitBtn = driver.find_element(By.CLASS_NAME,'css-fib3fn')
                                        if self.goGame(iframeList):
                                            self.goBlack()
                                            print("goBlack")
                                            break
                            except Exception as e:
                                print("닫기버튼 없음",e)
                            Searching = False
                elif code == 60:
                    self.goBlack()
                    print("goBlack")
                    break

                # if code > 40 and not Searching and needSearch:
                #     print("닫기 버튼 검색",code)
                #     Searching = True
                #     try:
                #         btnList = driver.find_elements(By.TAG_NAME,'button')
                #         print("Btn 검색",len(btnList))
                #         if len(btnList) > 14:
                #             print("iframe 검색")
                #             iframeList = driver.find_elements(By.TAG_NAME,'iframe')
                #             print("iframe",len(iframeList),"개")
                #             if(len(iframeList) > 0):
                #                 exitBtn = driver.find_element(By.CLASS_NAME,'css-fib3fn')
                #                 if self.goGame(iframeList, exitBtn):
                #                     self.goBlack()
                #                     print("goBlack")
                #                     break
                #     except Exception as e:
                #         print("닫기버튼 없음",e)
                #     Searching = False
                #     needSearch = False

                

            # sleep(insert_ms)

    def moveCustom(self, allItems, itemsCnt, search):
        driver = self.driver
        wait = WebDriverWait(driver, 25)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-1xytt4v')))


        if search or itemsCnt == 0:
            print("커스텀 목록 분석",search)
            sample_button = driver.find_elements(By.CSS_SELECTOR, '.css-ix8tkr')[0]
            categoryDiv = sample_button.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
            # print("카테고리 div 확인",categoryDiv)
            buttonList = categoryDiv.find_elements(By.TAG_NAME,'button')
            # print("카테고리 하위 button : ",len(buttonList))

            colorBtn = categoryDiv.find_element(By.XPATH, '..')
            colorDiv = colorBtn.find_elements(By.CLASS_NAME,'Layout')
            # print("colorDiv",len(colorDiv))
            colorList = colorDiv[3].find_elements(By.TAG_NAME,'button')
            # print("colorList : ",len(colorList),"idx:",self.btnIndex[0])
            
            itemsDiv = driver.find_element(By.CLASS_NAME, 'css-1xytt4v')
            itemList = itemsDiv.find_elements(By.TAG_NAME,'button')
            # print("itemList : ",len(itemList))
            
            first = buttonList[:4]
            second = buttonList[4:]
            colors = colorList
            items = itemList

            allItems = [first, second, colors, items]

        if not search:
            if self.btnCategory == 0:
                if self.btnIndex[self.btnCategory] == 0:
                    self.btnIndex = [self.btnIndex[0],0,2,0]
                else:
                    self.btnIndex = [self.btnIndex[0],0,0,0]
            elif self.btnCategory == 1:
                self.btnIndex = [self.btnIndex[0],self.btnIndex[1],0,0]

        
        print("커스텀 커서 이동",
                    # self.btnCategory,self.btnIndex[self.btnCategory]+1,"/",itemsCnt,
                    search,self.btnIndex)
        
        if itemsCnt > 0:
            selectedItem = allItems[self.btnCategory][self.btnIndex[self.btnCategory]]
            driver.execute_script("arguments[0].setAttribute('style', 'background:white')", selectedItem)
            sleep(0.1)
            driver.execute_script("arguments[0].setAttribute('style', 'background:')", selectedItem)
            selectedItem.click()

        itemsCnt = len(allItems[self.btnCategory])

        return allItems, itemsCnt


    def goGame(self, iframeList):
        driver = self.driver
        self.gameMode = True
        input_ms = datetime.now()
        arrow_ms = 0
        key = ''
        before_key = ''
        before_code = 0
        start_ms = 0
        now_ms = input_ms
        inGame = False
        insert_ms = 50 / 1000
        exitBtn = ''


        print("게임모드에 진입")
        sleep(1)


        for i, iframe in enumerate(iframeList):
            gameUrl = iframe.get_attribute('src').split('/')[-1]
            # gamdId = iframe.get_attribute('id')
            print("iframe url",gameUrl)
            if gameUrl in GAME_URL:
                print(gameUrl, "스위칭")
                driver.switch_to.frame(iframe)
                sleep(2)
                gamePage = driver.find_elements(By.TAG_NAME,'span')
                print("게임 클릭",len(gamePage))
                gamePage[0].click()
                driver.execute_script("arguments[0].setAttribute('style', 'display:none')", gamePage[0])
                # iframe.click()

                print("키 입력 대기")
                start_ms = datetime.now()
                input_ms = datetime.now()

                while True:
                    input_ms, key, code = self.getSignal(key, input_ms, 200)
                    # key = keyboard.read_key()
                    # print(key)
                    if arrow_ms != 0:
                        duration = (datetime.now() - arrow_ms).total_seconds() * 1000 
                        if duration> 100:
                            ActionChains(driver).key_up(before_key).perform()
                            print("키보드",KEYMAP_STR[str(before_code)],"키 뗌",int(duration),"ms")
                            arrow_ms = 0

                    if code == 0 :
                        continue

                    if(key == 'z') or key =='x' or code == 60:
                        duration = (datetime.now() - start_ms).total_seconds() * 1000 
                        print("exit btn click? ",int(duration),'ms')
                        if duration < 500:
                            continue

                        try:
                            driver.switch_to.default_content()
                            sleep(0.1)
                            btnList = driver.find_elements(By.TAG_NAME,'button')
                            print("Btn 검색",len(btnList))
                            for btn in btnList:
                                className= btn.get_attribute('class')
                                print(className)
                                if className == 'css-fib3fn' or className == 'css-m9qqc0':
                                    print("Find ExitBtn!!")
                                    exitBtn = btn

                            exitBtn.click()
                            self.gameMode = False
                            print("ifame 복귀")
                            if code == 60:
                                return True
                            break
                        except Exception as e:
                            print(e)
                    elif code < 20:
                        if before_key != key and before_key != '':
                            print("키보드",KEYMAP_STR[str(before_code)],"키 뗌")
                            ActionChains(driver).key_up(before_key).perform()

                        print("키보드",KEYMAP_STR[str(code)],"키 누름")
                        ActionChains(driver).key_down(key).perform()
                        before_key = key
                        before_code = code
                        arrow_ms = datetime.now()
                    elif code < 30:
                        print("음소거 ON/OFF")
                        pyautogui.FAILSAFE = False
                        pyautogui.hotkey('alt', 'shift', 'm') 
                    elif code > 40 :
                        if (key == 'start'):
                            print("게임 시작")
                            ActionChains(driver).key_down('1').perform()
                            sleep(0.05)
                            ActionChains(driver).key_up('1').perform()
                        elif (key == 'select'):
                            print("코인 삽입")
                            ActionChains(driver).key_down('5').pause(0.05).key_up('5').perform()
                        else:
                            ActionChains(driver).key_down(key).pause(0.05).key_up(key).perform()

        return False
        # gamearea << 게임 영역
        # css-fib3fn <<< 게임 종료 버튼


    def getSignal(self, before_key, then, delay = 500):
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
                print(KEYMAP_STR[code],"(",code,")",int(duration),"ms")

                if key != 'ERROR' :
                    if (before_key == key and duration > delay) or before_key != key :
                        # ActionChains(driver).key_down(key).pause(0.05).key_up(key).perform()
                        output_ms = datetime.now()
                        return output_ms, key, int(code)
                    else:
                        return output_ms, key, 0

        return output_ms, 'ERROR', 0
    
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