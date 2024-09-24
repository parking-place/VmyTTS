import os
import sys
import urllib.request
from tkinter import *
import threading
import json
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import VmyTTSManual
# import VmyTTSSetting
import VmyTTSGeneralSettings
import VmyTTSVoiceSettings
from VmyTTSGlobal import VmyTTSSingleton
from VmyTTSSpeakers import SPEAKERS
import pyglet
import datetime

COUNT = 0
BACKUP_FILE = ""
SETTINGS_FILE = "config.json"
KEYS_FILE = "keys.json"
CURRENT_TEXT = ""
CHATLOG = "\n\n\n\n\n\n\n\n\n\n"




def creat_chatlog():
    global BACKUP_FILE
    # 프로그램이 켜진 시간과 날짜를 기록(Asia/Seoul)
    now = datetime.datetime.now()
    # ./chatlog 폴더 생성 (있으면 생성하지 않음)
    if not os.path.exists("./chatlogs"):
        os.makedirs("./chatlogs")
    # 텍스트 백업용 파일 생성
    BACKUP_FILE = f"./chatlogs/backup_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        f.write("")
        
def get_keys():
    global KEYS_FILE
    with open(KEYS_FILE, "r", encoding="utf-8") as f:
        keys = json.load(f)
    
    CLIENT_AUTH = VmyTTSSingleton.getInstance().get_client_auth()
    
    CLIENT_AUTH["client_id"] = keys["client_id"]
    CLIENT_AUTH["client_secret"] = keys["client_secret"]
    
    VmyTTSSingleton.getInstance().set_client_auth(CLIENT_AUTH)
    
def load_setting():
    global SPEAKERS
    
    SETTINGS = VmyTTSSingleton.getInstance().get_settings()
    DEFAULT_SETTINGS = VmyTTSSingleton.getInstance().get_default_settings()
    
    # 스피커 정보를 가져오기
    try :
        speaker_infos = SPEAKERS[SETTINGS["speaker"]]
        # 정보를 이름|성별|언어 format으로 변환
        speaker_info = f"{speaker_infos['name']}"
        speaker_info += f"|{speaker_infos['gender']}"
        infos = speaker_infos['info']
        info_str = ""
        for info in infos:
            info_str += f"|{infos[info]}"
        speaker_info += info_str
        
        SETTINGS["info"] = speaker_info
    except Exception as e:
        print(e)
        print("Speaker 정보를 불러오는데 실패했습니다.")
        SETTINGS = DEFAULT_SETTINGS
    
    VmyTTSSingleton.getInstance().set_settings(SETTINGS)

def get_count():
    global COUNT
    # 카운트 0~5 반복
    COUNT += 1
    if COUNT > 5:
        COUNT = 0
    return COUNT

def save_chatlog(logline):
    global CHATLOG, BACKUP_FILE
    #백업용 파일에 "현재시간: result" 추가
    with open(BACKUP_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {logline}\n")

def makeMp3(text):
    CLIENT_AUTH = VmyTTSSingleton.getInstance().get_client_auth()
    SETTINGS = VmyTTSSingleton.getInstance().get_settings()
    URL = VmyTTSSingleton.getInstance().get_url()
    # mp3 파일 이름 설정
    #get_count()를 사용하면 0~5까지 반복
    filename = f"tts_{get_count()}.mp3"
    # text를 URL로 인코딩
    encText = urllib.parse.quote(text)
    # data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
    data = f"speaker={SETTINGS['speaker']}&volume={SETTINGS['volume']}&speed={SETTINGS['speed']}&pitch={SETTINGS['pitch']}&format=mp3&text=" + encText
    # print(data)
    # request 생성
    request = urllib.request.Request(URL)
    # 인증 정보 추가
    request.add_header("X-NCP-APIGW-API-KEY-ID",CLIENT_AUTH["client_id"])
    request.add_header("X-NCP-APIGW-API-KEY",CLIENT_AUTH["client_secret"])
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open(filename, 'wb') as f:
            f.write(response_body)
        speak(filename)
    else:
        print("Error Code:" + rescode)
        
def speak(filename):
    try:
        print("SoundPlay")
        # playsound.playsound(filename)
        song = pyglet.media.load(filename)
        song.play()
        # 재생이 끝나면 파일 삭제
        os.remove(filename)
    except:
        print("Error: ", sys.exc_info()[0])
        
def save_settings():
    VmyTTSSingleton.getInstance().save_settings()
    
    
def main_window():
    VERSION = VmyTTSSingleton.getInstance().get_version()
    SETTINGS = VmyTTSSingleton.getInstance().get_settings()
    
    # 사용자 입력 함수
    def returnEntry(arg=None):
        SETTINGS = VmyTTSSingleton.getInstance().get_settings()
        global CURRENT_TEXT, CHATLOG
        # 이전 CURRENT_TEXT를 CHATLOG에 추가
        chatLogLabel.config(text=CHATLOG + "\n" + CURRENT_TEXT)
        CURRENT_TEXT = mEntry.get()
        CHATLOG = chatLogLabel.cget("text")
        #텍스트가 10줄 이상일 경우 맨 윗줄 삭제
        if CHATLOG.count("\n") >= 10:
            CHATLOG = CHATLOG[CHATLOG.index("\n")+1:]
        # label_you_said를 업데이트
        currentLogLabel.config(text=CURRENT_TEXT)
        #백업용 파일에 "현재시간: result" 추가
        save_chatlog(CURRENT_TEXT)
        # 사용자 입력 초기화
        mEntry.delete(0, END)
        # 현재 설정 저장
        VmyTTSSingleton.getInstance().set_settings(SETTINGS)
        
        if SETTINGS["Mutemode"] == "False":
            # 음소거가 아닐 경우
            thread = threading.Thread(target=makeMp3, args=(CURRENT_TEXT,))
            thread.daemon = True
            thread.start()
    
    # 새창에서 목소리 설정 창을 띄우는 함수
    def new_window_voice_setting():
        # os.system('python VmyTTSSetting.py')
        VmyTTSVoiceSettings.new_window_settings()
        SETTINGS = VmyTTSSingleton.getInstance().get_settings()
        # 설정 정보 업데이트
        speakerButton.config(text=f'목소리: {SETTINGS["info"]}')
        root.after(500, refresh_info)
        
    # 새창에서 일반 설정 창을 띄우는 함수
    def new_window_general_setting():
        # os.system('python VmyTTSSetting.py')
        VmyTTSGeneralSettings.new_window_settings()
        
    # 전체 볼륨 조절 함수
    def setWinVolume(*args):
        SETTINGS = VmyTTSSingleton.getInstance().get_settings()
        SETTINGS["WinVolume"] = WinVolumeScale.get()
        
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            # 현재 앱만 볼륨 조절(python.exe, VmyTTS.exe)
            if session.Process and session.Process.name() == "python.exe":
                volume.SetMasterVolume(SETTINGS["WinVolume"]/100, None)
            if session.Process and session.Process.name() == "VmyTTS.exe":
                volume.SetMasterVolume(SETTINGS["WinVolume"]/100, None)
        
        VmyTTSSingleton.getInstance().set_settings(SETTINGS)
    
    # 음소거 체크박스 함수
    def setMute():
        SETTINGS = VmyTTSSingleton.getInstance().get_settings()
        if SETTINGS["Mutemode"] == "False":
            SETTINGS["Mutemode"] = "True"
        else:
            SETTINGS["Mutemode"] = "False"
        
        VmyTTSSingleton.getInstance().set_settings(SETTINGS)
    
    # 정보 최신화 함수
    def refresh_info():
        speakerButton.config(
            text=f'목소리: {VmyTTSSingleton.getInstance().get_settings()["info"]}'
            )
    
    # TK 창 생성
    root = Tk()
    # 창 이름 설정
    root.title(f"버미육을 위한 TTS v.{VERSION}")
    
    # ChatLog 생성
    chatLogLabel = Label(root, text=CHATLOG, font=("맑은 고딕", 10))
    chatLogLabel.pack(fill=X)
    
    # 구분선 생성
    gubunline = ""
    for i in range(0, 500):
        gubunline += "-"
    
    #텍스트 (중앙 정렬, 글자 크기 5)
    emptylabel_1 = Label(root, text=gubunline, font=("Helvetica", 3))
    emptylabel_1.pack()
    #텍스트 (중앙 정렬, 글자 크기 20, 볼드체)
    currentLogLabel = Label(root, text="너가 직전에 말한 내용", font=("맑은 고딕", 15, "bold"))
    currentLogLabel.pack()
    #텍스트 (중앙 정렬, 글자 크기 5)
    emptylabel_2 = Label(root, text=gubunline, font=("Helvetica", 3))
    emptylabel_2.pack()
    
    #사용자 입력(폰트 크기 10 맑은 고딕)
    mEntry = Entry(root, width=80, font=("맑은 고딕", 13))
    mEntry.focus()
    mEntry.bind("<Return>", returnEntry)
    mEntry.pack()
    
    # 새 창에서 목소리 설정 창을 띄우는 버튼과
    # 새 창에서 일반 설정 창을 띄우는 버튼
    # 한 프레임에서 좌우로 배치
    settingFrame = Frame(root)
    settingFrame.pack()
    # 목소리 설정 버튼
    speakerButton = Button(settingFrame, text=f'목소리: {SETTINGS["info"]}', command=new_window_voice_setting)
    speakerButton.pack(side=LEFT)
    # 일반 설정 버튼
    generalButton = Button(settingFrame, text="일반 설정", command=new_window_general_setting)
    generalButton.pack(side=RIGHT)
    
    # 음소거 체크박스, 전체볼륨조절바 (0 ~ 100)
    # 한 프레임으로 좌우로 배치
    volumeFrame = Frame(root)
    volumeFrame.pack()
    # 음소거 체크박스
    muteCheck = Checkbutton(volumeFrame, text="음소거", command=setMute)
    muteCheck.pack(side=LEFT)
    # 전체 볼륨 조절
    WinVolumeScale = Scale(volumeFrame, from_=0, to=100, orient=HORIZONTAL, length=200, command=setWinVolume)
    WinVolumeScale.set(int(SETTINGS["WinVolume"]))
    WinVolumeScale.pack(side=RIGHT)
    
    # by Parking_Place
    # 폰트 크기 7, 맑은 고딕, 우하단 정렬, 회색
    MadeMyLabel = Label(root, text="by @Parking_Place", font=("맑은 고딕", 8), fg="gray")
    MadeMyLabel.pack(anchor=SE)
    
    # 창 종료시 설정 저장
    def on_close():
        save_settings()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # 음성 초기화
    def init_playsound():
        # playsound.playsound('start0.mp3')
        try:
            song = pyglet.media.load('start0.mp3')
            song.play()
        except:
            print("Error: ", sys.exc_info()[0])
    thread = threading.Thread(target=init_playsound)
    thread.daemon = True
    thread.start()
    
    # refresh_info 함수 전달
    VmyTTSSingleton.getInstance().set_info_refreshing_func(refresh_info)
    
    #기본 루프
    root.mainloop()


def vmyTTS():
    
    # init
    creat_chatlog()
    VmyTTSSingleton.getInstance()
    
    # main window
    main_window()
    
    pass


if __name__ == "__main__":
    vmyTTS()