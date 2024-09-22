import os
import sys
import urllib.request
from tkinter import *
import threading
import json
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import VmyTTSManual
import VmyTTSSetting
import pyglet

# 프로그램이 켜진 시간과 날짜를 기록(Asia/Seoul)
import datetime
now = datetime.datetime.now()

# ./chatlog 폴더 생성 (있으면 생성하지 않음)
if not os.path.exists("./chatlogs"):
    os.makedirs("./chatlogs")
# 텍스트 백업용 파일 생성
backup_file = f"./chatlogs/backup_{now.strftime('%Y%m%d_%H%M%S')}.txt"
with open(backup_file, "w", encoding="utf-8") as f:
    f.write("")


# .keys 파일 불러오기
keys_file = "keys.json"
with open(keys_file, "r", encoding="utf-8") as f:
    keys = json.load(f)

client_id = keys["client_id"]
client_secret = keys["client_secret"]

# tinkter 폰트 설정
font_size_log = ("맑은 고딕", 15, "bold")
font_size_label = ("맑은 고딕", 18, "bold")


url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
resultLabeltext = "\n\n\n\n\n\n\n\n\n\n"

settings = {
    "speaker": "nara",
    "volume": "0",
    "speed": "0",
    "pitch": "0",
    "emotion": "0",
    "emotion-strength" : "0",
    "alpha": "0",
    "info": "",
    "WinVolume": "50",
}

#설정파일 불러오기 함수(UTF-8)
def load_settings():
    settings_file = "config.json"
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
        
    try:
        # speaker.json 파일 불러오기
        speakers_file = "./speaker.json"
        with open(speakers_file, "r", encoding="utf-8") as f:
            speakers_info = json.load(f)
        # 현재 스피커의 정보를 가져오기
        speaker_infos = speakers_info[settings["speaker"]]
        # 정보를 이름|성별|언어 format으로 변환
        speaker_info = f"{speaker_infos['name']}"
        speaker_info += f"|{speaker_infos['gender']}"
        infos = speaker_infos['info']
        info_str = ""
        for info in infos:
            info_str += f"|{infos[info]}"
        speaker_info += info_str
        
        settings["info"] = speaker_info
    except:
        settings = {
            "speaker": "nara",
            "volume": "0",
            "speed": "0",
            "pitch": "0",
            "emotion": "0",
            "emotion-strength" : "0",
            "alpha": "0",
            "info": "",
            "WinVolume": "50",
        }
    
    return settings

settings = load_settings()

# # 출력
# print(speaker_info)

count = 0

root = Tk()

# TK 창 이름 설정
# Version 파일 불러오기(UTF-8 텍스트 파일)
version_file = "Version"
with open(version_file, "r", encoding="utf-8") as f:
    version = f.read()
    
root.title(f"버미육을 위한 TTS v.{version}")

def returnEntry(arg=None):
    result=mEntry.get()
    resultlabeltext = resultLabel.cget("text")
    #텍스트가 10줄 이상일 경우 맨 윗줄 삭제
    if resultlabeltext.count("\n") >= 10:
        resultlabeltext = resultlabeltext[resultlabeltext.index("\n")+1:]
    #result 를 resultlabeltext 맨 아래에 추가
    resultLabel.config(text=resultlabeltext + "\n" + result)
    #label_you_said를 result로 변경
    label_you_said.config(text= f'{result}')
    
    #백업용 파일에 "현재시간: result" 추가
    now = datetime.datetime.now()
    with open(backup_file, "a", encoding="utf-8") as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')}: {result}\n")
    
    mEntry.delete(0, END)

    print("makeMp3")
    thread = threading.Thread(target=makeMp3, args=(result,))
    thread.daemon = True
    thread.start()
    
    
    print("done")

def makeMp3(text):
    # 카운트 0~5 반복
    global count
    count = count + 1
    if count > 6:
        count = 0
    filename = 'sample' + str(count) + '.mp3'

    encText = urllib.parse.quote(text)
    # data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
    data = f"speaker={settings['speaker']}&volume={settings['volume']}&speed={settings['speed']}&pitch={settings['pitch']}&format=mp3&text=" + encText
    print(data)
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
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
        
def saveSettings():
    global settings
    # 설정 저장(UTF-8)
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(settings, f)
        print("저장 완료")
        
# X버튼으로 종료시 설정 저장
def on_closing():
    saveSettings()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 정보 최신화 함수
def refresh_info():
    global settings
    settings = load_settings()
    speakerButton.config(text=f'목소리: {settings["info"]}')
    root.after(500, refresh_info)

#result
resultLabel = Label(root, text=resultLabeltext)
resultLabel.pack(fill=X)

#구분선
gubunline = ""
for i in range(0, 500):
    gubunline += "-"

#텍스트 (중앙 정렬, 글자 크기 5)
emptylabel_1 = Label(root, text=gubunline, font=("Helvetica", 3))
emptylabel_1.pack()
#텍스트 (중앙 정렬, 글자 크기 20, 볼드체)
label_you_said = Label(root, text="너가 직전에 말한 내용", font=("맑은 고딕", 15, "bold"))
label_you_said.pack()
#텍스트 (중앙 정렬, 글자 크기 5)
emptylabel_2 = Label(root, text=gubunline, font=("Helvetica", 3))
emptylabel_2.pack()

#사용자 입력(폰트 크기 10 맑은 고딕)
mEntry = Entry(root, width=80, font=("맑은 고딕", 13))
mEntry.focus()
mEntry.bind("<Return>", returnEntry)
mEntry.pack()

# mEntry = Entry(root, width=80)
# mEntry.focus()
# mEntry.bind("<Return>", returnEntry)
# mEntry.pack()

# # #버튼 클릭 - 함수 실행
# speakButton = Button(root, text="말하기(엔터도됨)", command=returnEntry)
# speakButton.pack()

# ./VmyTTSSetting.py 실행해주는 함수
def setting():
    # os.system('python VmyTTSSetting.py')
    VmyTTSSetting.new_window_settings()
    # 설정 다시 불러오기
    global settings
    settings = load_settings()
    # 설정 정보 업데이트
    speakerButton.config(text=f'목소리: {settings["info"]}')
    

# 새 창에서 스피커 설정 변경 버튼(우하단 정렬)
speakerButton = Button(root, text=f'목소리: {settings["info"]}', command=setting)
# speakerButton.pack(side=LEFT, anchor=SW)
speakerButton.pack()

# # 현재 설정 정보 출력(좌하단 정렬)
# infoLabel = Label(root, text=settings["info"])
# infoLabel.pack(side=LEFT, anchor=SW)


#윈도우 사이즈 변경 불가
# root.resizable(False, False)

# 설정 설명 새창에서 여는 함수
def newWindowManual():
    # os.system("python VmyTTSManual.py")
    VmyTTSManual.new_window_manual()
    
    
# 설정 설명 버튼(우하단 정렬)
manualButton = Button(root, text="옵션 설명", command=newWindowManual)
manualButton.pack(anchor=S)

    

# # 볼륨 조절 바(v_size = 0.30, 0.00~1.00)
# v_size_label = Label(root, text="볼륨 조절")
# v_size_label.pack()
# v_size_scale = Scale(root, from_=0.00, to=1.00, resolution=0.01, orient=HORIZONTAL, length=200, variable=v_size)
# v_size_scale.set(0.30)
# v_size_scale.pack()



# 감정 설정 체크박스(0중립, 1슬픔, 2기쁨, 3분노)
emotionLabel = Label(root, text="감정(일부 목소리만 적용)")
emotionLabel.pack()
emotionVar = IntVar()
emotionVar.set(int(settings["emotion"]))
emotionFrame = Frame(root)
emotionFrame.pack()
emotionRadios = []
for i, emotion in enumerate(["중립", "슬픔", "기쁨", "분노"]):
    emotionRadio = Radiobutton(emotionFrame, text=emotion, variable=emotionVar, value=i)
    emotionRadio.pack(side=LEFT)
    emotionRadios.append(emotionRadio)

# 감정 강도 설정(0약함, 1보통, 2강함)
emotionStrengthLabel = Label(root, text="감정 강도")
emotionStrengthLabel.pack()
emotionStrengthVar = IntVar()
emotionStrengthVar.set(int(settings["emotion-strength"]))
emotionStrengthFrame = Frame(root)
emotionStrengthFrame.pack()
emotionStrengthRadios = []
for i, emotionStrength in enumerate(["약함", "보통", "강함"]):
    emotionStrengthRadio = Radiobutton(emotionStrengthFrame, text=emotionStrength, variable=emotionStrengthVar, value=i)
    emotionStrengthRadio.pack(side=LEFT)
    emotionStrengthRadios.append(emotionStrengthRadio)
    
# 음색, 볼륨, 속도, 피치 바 설정
# -5~5 정수, 바위치가 바뀌면 설정 저장
# 1행으로 4개의 수직바를 배치
varFrame = Frame(root)
varFrame.pack()

# 음색 설정 (-5~5 정수)
alphaLabel = Label(varFrame, text="음\n색")
alphaLabel.pack(side=LEFT)
alphaVar = IntVar()
alphaVar.set(int(settings["alpha"]))
alphaScale = Scale(varFrame, from_=-5, to=5, orient=VERTICAL, variable=alphaVar)
alphaScale.pack(side=LEFT)

# 볼륨 설정 (-5~5 정수)
volumeLabel = Label(varFrame, text="볼\n륨")
volumeLabel.pack(side=LEFT)
volumeVar = IntVar()
volumeVar.set(int(settings["volume"]))
volumeScale = Scale(varFrame, from_=5, to=-5, orient=VERTICAL, variable=volumeVar)
volumeScale.pack(side=LEFT)

# 속도 설정 (-5~5 정수)
speedLabel = Label(varFrame, text="속\n도")
speedLabel.pack(side=LEFT)
speedVar = IntVar()
speedVar.set(int(settings["speed"]))
speedScale = Scale(varFrame, from_=-5, to=5, orient=VERTICAL, variable=speedVar)
speedScale.pack(side=LEFT)

# 피치 설정 (-5~5 정수)
pitchLabel = Label(varFrame, text="피\n치")
pitchLabel.pack(side=LEFT)
pitchVar = IntVar()
pitchVar.set(int(settings["pitch"]))
pitchScale = Scale(varFrame, from_=-5, to=5, orient=VERTICAL, variable=pitchVar)
pitchScale.pack(side=LEFT)

# 설정 적용 함수
def saveSettings_btn_func():
    global settings
    settings["volume"] = volumeVar.get()
    settings["speed"] = speedVar.get()
    settings["pitch"] = pitchVar.get()
    settings["emotion"] = emotionVar.get()
    settings["emotion-strength"] = emotionStrengthVar.get()
    settings["alpha"] = alphaVar.get()
    settings["WinVolume"] = WinVolumeScale.get()
    # print(settings)
    saveSettings()
    settings = load_settings()

# 설정 적용 버튼(하단 중앙 정렬)
saveButton = Button(root, text="설정 적용", command=saveSettings_btn_func)
saveButton.pack()


# 전체볼륨조절바 (0 ~ 100)
WinVolume = 50
WinVolume = int(settings["WinVolume"])

def setWinVolume(*args):
    global WinVolume
    WinVolume = WinVolumeScale.get()
    
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        # 현재 앱만 볼륨 조절
        if session.Process and session.Process.name() == "python.exe":
            volume.SetMasterVolume(WinVolume/100, None)
    
    # print(WinVolume)
    # os.system(f'nircmd.exe setsysvolume {WinVolume}')

# 전체볼륨조절바 (0 ~ 100)
WinVolumeLabel = Label(root, text="전체 볼륨 조절")
WinVolumeLabel.pack()
WinVolumeScale = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=200, command=setWinVolume)
WinVolumeScale.set(WinVolume)
WinVolumeScale.pack()





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

# refresh_info 함수 0.5초마다 실행
root.after(500, refresh_info)

#기본 루프
root.mainloop()