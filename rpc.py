"""
# YOUTUBE MUSIC DISCORD RPC
"""
import os
import shutil
import subprocess
import sys
import pypresence
import time
import threading
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

global Data
global CHROME_DIR_PATH
global RE_IS_YTM_IMG_URL
global RE_IMG_W_H

CHROME_DIR_PATH = r'{}'.format(os.getcwd()+'''\\chrome''') # 크롬 폴더 주소
RE_IS_YTM_IMG_URL = "https://lh3.googleusercontent.com"
RE_IMG_W_H = "=w[0-9]{1,4}-h[0-9]{1,4}(-l[0-9]{1,4}-rj)?"

class StateType:
    Running = 0
    PlzStop = 1
    Waiting = 2
    FixError = 8

class State:
    NOW_STATE = StateType.Waiting # 클래스 변수

Data = {
    "title" : "Idle🌙",
    "url" : "https://music.youtube.com/",
    "img" : "https://music.youtube.com/img/favicon_144.png",
    "small_img" : 'music_note_fill0_wght700_grad200_opsz48',
    "timeMax" : '0:01',
    "timeNow" : '0:01',
    "author" : "None",
    "isAlbum" : True,
    "album" : "None"
}

changeTimeDict = {
    0 : 1, # 초는 x1배
    1 : 60, # 분은 x60배
    2 : 3600, # 시간은 x3600배
    3 : 86400, # 일(日)은 x84600배
}

waiting_time = 0

def changeTime(time: str):
    """'12:34' 와 같은 형태를 754 (754초) 로 변환
    '12:23:59:59' (12일 23시간 59분 59초) -> 1123199 (1123199초)

    Args:
        time (str): 12:34 와 같은 문자형 시간

    Returns:
        _type_: _description_
    """
    t1 = time.split(":")
    result = 0
    for i in range(len(t1)):
        result += int(t1[-(i+1)]) * changeTimeDict[i]
    return result

def playPercent(nowTime, allTime) -> str:
    """재생바 생성

    Args:
        nowTime (_type_): _description_
        allTime (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        if nowTime == "0:01" and allTime == "0:01":
            return "!> ──────●●●────── <!"

        percent = (changeTime(nowTime) / changeTime(allTime)) * 100
        pp = int(percent / 6.5)
        if pp >= 1:
            pp = pp -1
        em = '●'
        listE = ['─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─', '─']
        listE[pp] = em
        for i in range(pp):
            listE[i] = "━"
        Text = ' '
        for i in listE:
            Text = f'{Text}{i}'
        percent = int(percent)
        Text = f'{nowTime} {Text} {allTime}'
        return Text
    except:
        return "!> ──────●●●────── <!"

def start_threading(func: any, name: str, args: tuple, daemon: bool = True) -> None:
    """
    - 간단하게 쓰레드를 시작합니다.
    |Name|Description|
    |:--:|:--:|
    |func|함수 이름|
    |name|실행할 쓰레드 이름|
    |args|함수 인자|
    |daemon|데몬 쓰레드 여부|
    * args(tuple)에 인자가 1개인 경우 마지막에 ,  ex) -> (1,)
    * 데몬쓰레드 : 메인 쓰레드가 종료되면 유지하지 않고 같이 종료되는 쓰레드.
    """
    if args is None:
        args = ( )
    thread = threading.Thread(target=func, name=name, args=args)
    thread.daemon = daemon
    thread.start()



def yt_music(*arg):
    try: # Start ChromeDriver
        options = Options()
        options.add_argument(f"user-data-dir={CHROME_DIR_PATH}")
        options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
        # options.add_argument("--start-maximized")  # 최대 크기로 시작
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://music.youtube.com")

        time.sleep(waiting_time)	# 암시적 대기 시간 3초 설정

    except ValueError as e: # 보통 파이썬 크롬 라이브러리 버전과 크롬 버전이 일치하지 않아서 발생해요.
        State.NOW_STATE = StateType.FixError
        print(f"\033[5m\033[1m\033[4m\033[3m\033[31mError : {e}\033[0m")
        print(f"\033[92mAutomatic repair is running. If not fixed, check the help below.")
        print(f"자동 복구가 실행 중 입니다. 만약 문제가 지속된다면 아래의 도움말을 참고해 주세요.\033[0m\n")

        print("\033[93mTry Updating Python Library and Chrome.\nAnd delete ./chrome diretory and ./__pycache__ diretory, then execute chrome.bat")
        print("Python 라이브러리와 Chrome을 업데이트해 보세요.\n그리고 ./chrome 폴더와 ./__pycache__폴더를 삭제한 다음, chrome.bat 을 실행하시고 다시 시작해 보세요.\033[0m\n")

        print("\033[92mAfter 10 seconds, all processes except for the Chrome update will be executed automatically. Press \033[93mCtrl + C\033[0m \033[93mto cancel\033[0m.")
        print("\033[92m10초뒤 크롬 업데이트를 제외한 과정이 자동으로 실행됩니다. \033[93m취소\033[92m하려면 \033[93mCtrl + C\033[0m를 누르세요.\033[0m\n")

        for i in range(1, 11):
            print(f"    Waiting... {i} s", end='\r')
            time.sleep(1)

        print("\nStart auto repair. Log in to YouTube Music in the open Chrome window and then close it.")
        print("자동 복구를 시작합니다. 이 과정에서 열린 크롬창은 유튜브 뮤직에 로그인 하고 닫아주시기 바랍니다.")

        print("\nDelect ./Chrome and ./__pycache__ Diretory")
        if os.path.isdir((chrome_dir := os.getcwd()+'''\\chrome''')): shutil.rmtree(chrome_dir)
        else: print("NotFoundChromeDir")

        if os.path.isdir((pycache_dir := os.getcwd()+'''\\__pycache__''')): shutil.rmtree(pycache_dir)
        else: print("NotFoundPycacheDir")

        print("\nUpdate Library")
        try: subprocess.Popen(['start', 'install_lib.bat'], shell=True)
        except Exception as e: print(f"Updating library is failed: {e}")

        print("\nStart chrome.bat")
        try: subprocess.Popen(['start', 'chrome.bat'], shell=True)
        except Exception as e: print(f"Starting chrome.bat is failed {e}")

        print("\nLog in to YouTube Music in the open Chrome window and then close it!")
        print("\033[91m꼭 이 과정에서 열린 크롬창에 유튜브 뮤직에 로그인\033[0m 하고 \033[91m닫아\033[0m주시기 바랍니다!")
        print("아니면 직접 chrome.bat 을 실행하여 로그인 하시기 바랍니다.")
        print("\033[92mThe program will end in 15 seconds and restart.\033[0m")

        print("이제 이 창은 닫아도 됩니다.")

        State.NOW_STATE = StateType.PlzStop
        sys.exit(1)

    except Exception as e:
        State.NOW_STATE = StateType.FixError
        print(e)
        print("알 수 없는 에러가 발생했습니다.")
        print("크롬이 켜진 상태라면 끄고 다시 시도해 보시기 바랍니다.")
        State.NOW_STATE = StateType.PlzStop
        sys.exit(1)

    else: # Crawler
        State.NOW_STATE = StateType.Running
        while True:
            print(); time.sleep(1)

            try:
                try: # Get Title
                    Data["title"] = f'{driver.find_element(By.XPATH, """//*[@id="layout"]/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string""").get_attribute("title")} '
                except:
                    Data["title"] = "Idle🌙"
                    Data['small_img'] = 'music_note_fill0_wght700_grad200_opsz48'

                try: # Get URL
                    Data["url"] = driver.find_element(By.XPATH, """/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-page/div/div[1]/ytmusic-player/div[2]/div/div/div[3]/div[2]/div/a""").get_attribute("href")
                    if "list" in Data["url"]:
                        Data["url"] = "https://music.youtube.com/watch?v=" + Data["url"].split("v=")[1]
                except:
                    Data["url"] = "https://music.youtube.com/"

                try: # Get Thumbnail URL
                    Data['img']: str = driver.find_element(By.XPATH, """//*[@id="layout"]/ytmusic-player-bar/div[2]/div[1]/img""").get_attribute("src")
                    if Data['img'].startswith(RE_IS_YTM_IMG_URL):
                        Data['img'] = Data['img'].replace(re.search(RE_IMG_W_H, Data['img']).group(), "=w544-h544-l90-rj")

                    if Data['img'] == '':
                        Data['img'] = "https://music.youtube.com/img/favicon_144.png"
                except:
                    Data['img'] = "https://music.youtube.com/img/favicon_144.png"

                try: # Get Time and State
                    time_data = driver.find_element(By.XPATH, """/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/tp-yt-paper-slider""").get_attribute("aria-valuetext")
                    time_data = time_data.split(" ")

                    before_time = Data['timeNow']

                    Data['timeMax'] = time_data[1]
                    Data['timeNow'] = time_data[3]
                    if Data['timeNow'] == "0:00":
                        Data['timeNow'] = '0:01'

                    if before_time == time_data[3]: Data['small_img'] = 'stop_fill0_wght700_grad200_opsz48'
                    else: Data['small_img'] = 'headphones_fill0_wght700_grad200_opsz48'
                except:
                    Data['timeMax'] = '0:01'
                    Data['timeNow'] = '0:01'
                    Data['small_img'] = 'question_mark_fill0_wght500_grad0_opsz48'

                try: # Get Author
                    Data['author'] = driver.find_element(By.XPATH, """//*[@id="layout"]/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[1]""").text
                except:
                    Data['author'] = "None"

                try: # Check it is Album (deprecated)
                    Data['album'] = driver.find_element(By.XPATH, """/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[2]""").text
                    Data['isAlbum'] = True
                except:
                    Data['album'] = "Music Video"
                    Data['isAlbum'] = False

                print(Data)

            except:
                pass






if __name__ == '__main__':
    print("Starting ChromeDirver...")
    start_threading(yt_music, "yt_music", (1,1), True)

    # time.sleep(waiting_time)
    while State.NOW_STATE == StateType.Waiting:
        time.sleep(0.1)

    print("Checking system...")
    while True:
        if State.NOW_STATE == StateType.FixError:
            time.sleep(0.1)

            if State.NOW_STATE == StateType.PlzStop:
                print("Exit code: 1")
                time.sleep(1)
                sys.exit(1)

        else: 
            break

    print("Starting RPC...")
    TIMESTAMP = time.time()
    client_id = 1135573479136170026 # don't touch
    try:
        RPC = pypresence.Presence(client_id)
        print("Connecting RPC...")
        RPC.connect()

    except pypresence.exceptions.DiscordNotFound:
        print("DiscordNotFound\nplease open discord windows application")

    except Exception as e:
        print(e)

    else:
        while True:
            RPC.update(
                details = f"{Data['title']}({Data['author']})",
                state = f"{playPercent(Data['timeNow'], Data['timeMax'])}",
                # start = start,
                buttons = [
                    {
                        "label": "YouTube Music에 연결하기",
                        "url": Data['url']
                    },
                    {
                        "label": "YouTube로 듣기",
                        "url": "https://www." + Data['url'].split("music.")[1]
                    }
                ],
                instance = True,
                large_image=Data['img'],
                large_text=f"{Data['title']} - {Data['author']}",
                small_image=Data['small_img'],
                start=TIMESTAMP
            )
            time.sleep(1)