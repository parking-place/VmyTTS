from tkinter import *

from VmyTTSGlobal import VmyTTSSingleton
from VmyTTSSpeakers import SPEAKERS
import VmyTTSManual

def new_window_settings():
    settings = VmyTTSSingleton.getInstance().get_settings()
    
    setlevel = Toplevel()
    
    # TK 창 이름 설정
    setlevel.title("목소리 상세 설정")
    
    # 설정 설명 새창에서 여는 함수
    def newWindowManual():
        # os.system("python VmyTTSManual.py")
        VmyTTSManual.new_window_manual()
        
        
    # 설정 설명 버튼(상단 정렬)
    manualButton = Button(setlevel, text="옵션 설명", command=newWindowManual)
    manualButton.pack()

        

    # # 볼륨 조절 바(v_size = 0.30, 0.00~1.00)
    # v_size_label = Label(setlevel, text="볼륨 조절")
    # v_size_label.pack()
    # v_size_scale = Scale(setlevel, from_=0.00, to=1.00, resolution=0.01, orient=HORIZONTAL, length=200, variable=v_size)
    # v_size_scale.set(0.30)
    # v_size_scale.pack()


    # 감정 설정 함수
    def emotionSettings_btn_func():
        settings['emotion'] = emotionVar.get()
        VmyTTSSingleton.getInstance().set_settings(settings)
    # 감정 설정 체크박스(0중립, 1슬픔, 2기쁨, 3분노)
    emotionLabel = Label(setlevel, text="감정(일부 목소리만 적용)")
    emotionLabel.pack()
    emotionVar = IntVar()
    emotionVar.set(int(settings["emotion"]))
    emotionFrame = Frame(setlevel)
    emotionFrame.pack()
    emotionRadios = []
    for i, emotion in enumerate(["중립", "슬픔", "기쁨", "분노"]):
        emotionRadio = Radiobutton(
            emotionFrame,
            text=emotion,
            variable=emotionVar,
            value=i,
            command=emotionSettings_btn_func
            )
        emotionRadio.pack(side=LEFT)
        emotionRadios.append(emotionRadio)

    # 감정 강도 설정 함수
    def strengthSettings_btn_func():
        settings['emotion-strength'] = emotionStrengthVar.get()
        VmyTTSSingleton.getInstance().set_settings(settings)
    # 감정 강도 설정(0약함, 1보통, 2강함)
    emotionStrengthLabel = Label(setlevel, text="감정 강도")
    emotionStrengthLabel.pack()
    emotionStrengthVar = IntVar()
    emotionStrengthVar.set(int(settings["emotion-strength"]))
    emotionStrengthFrame = Frame(setlevel)
    emotionStrengthFrame.pack()
    emotionStrengthRadios = []
    for i, emotionStrength in enumerate(["약함", "보통", "강함"]):
        emotionStrengthRadio = Radiobutton(
            emotionStrengthFrame, text=emotionStrength, variable=emotionStrengthVar, value=i,
            command=strengthSettings_btn_func
            )
        emotionStrengthRadio.pack(side=LEFT)
        emotionStrengthRadios.append(emotionStrengthRadio)
        
    # 음색, 볼륨, 속도, 피치 바 설정
    # -5~5 정수, 바위치가 바뀌면 설정 저장
    # 1행으로 4개의 수직바를 배치
    varFrame = Frame(setlevel)
    varFrame.pack()

    # 음색 설정 함수
    def alphaSettings_btn_func():
        settings["alpha"] = alphaVar.get()
        VmyTTSSingleton.getInstance().set_settings(settings)
    # 음색 설정 (-5~5 정수)
    alphaLabel = Label(varFrame, text="음\n색")
    alphaLabel.pack(side=LEFT)
    alphaVar = IntVar()
    alphaVar.set(int(settings["alpha"]))
    alphaScale = Scale(
        varFrame, from_=-5, to=5, orient=VERTICAL, variable=alphaVar,
        command=alphaSettings_btn_func
        )
    alphaScale.pack(side=LEFT)

    # 볼륨 설정 함수
    def volumeSettings_btn_func():
        settings["volume"] = volumeVar.get()
        VmyTTSSingleton.getInstance().set_settings(settings)
    # 볼륨 설정 (-5~5 정수)
    volumeLabel = Label(varFrame, text="볼\n륨")
    volumeLabel.pack(side=LEFT)
    volumeVar = IntVar()
    volumeVar.set(int(settings["volume"]))
    volumeScale = Scale(
        varFrame, from_=5, to=-5, orient=VERTICAL, variable=volumeVar,
        command=volumeSettings_btn_func
        )
    volumeScale.pack(side=LEFT)

    # 속도 설정 함수
    def speedSettings_btn_func():
        settings["speed"] = speedVar.get()
        VmyTTSSingleton.getInstance().set_settings(settings)
    # 속도 설정 (-5~5 정수)
    speedLabel = Label(varFrame, text="속\n도")
    speedLabel.pack(side=LEFT)
    speedVar = IntVar()
    speedVar.set(int(settings["speed"]))
    speedScale = Scale(
        varFrame, from_=-5, to=5, orient=VERTICAL, variable=speedVar,
        command=speedSettings_btn_func
        )
    speedScale.pack(side=LEFT)

    # 피치 설정 함수
    def pitchSettings_btn_func():
        settings["pitch"] = pitchVar.get()
        VmyTTSSingleton.getInstance().set_settings(settings)
    # 피치 설정 (-5~5 정수)
    pitchLabel = Label(varFrame, text="피\n치")
    pitchLabel.pack(side=LEFT)
    pitchVar = IntVar()
    pitchVar.set(int(settings["pitch"]))
    pitchScale = Scale(
        varFrame, from_=-5, to=5, orient=VERTICAL, variable=pitchVar,
        command=pitchSettings_btn_func
        )
    pitchScale.pack(side=LEFT)

    # 닫기 버튼 함수
    def closeWindow_btn_func():
        setlevel.destroy()
    # 닫기 버튼(하단 중앙 정렬)
    saveButton = Button(setlevel, text="닫기", command=closeWindow_btn_func)
    saveButton.pack()
    
    
    pass