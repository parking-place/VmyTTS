from tkinter import *

from VmyTTSGlobal import VmyTTSSingleton
from VmyTTSSpeakers import SPEAKERS



def new_window_settings():
    global SPEAKERS
    speakers = SPEAKERS
    # speakers 를 리스트로 변환
    speakers = list(speakers.items())

    settings = {
        "speaker": "nara",
        "volume": "0",
        "speed": "0",
        "pitch": "0",
        "emotion": "0",
        "emotion-strength" : "0",
        "alpha": "0",
    }

    # json 파일 불러오기 (UTF-8)
    
    settings = VmyTTSSingleton.getInstance().get_settings()

    print(settings)
            

    setlevel = Toplevel()

    # TK 창 이름 설정
    setlevel.title("목소리 설정")


    # speaker 설정 (체크박스, 스크롤바, 이름만 출력, 한줄에 5개씩 출력)
    speakerLabel = Label(setlevel, text="목소리 설정")
    speakerLabel.pack()
    speakerVar = StringVar()
    speakerVar.set(settings["speaker"])

    # 라디오 버튼 클릭시 설정 저장
    def radio_click():
        settings = VmyTTSSingleton.getInstance().get_settings()
        settings["speaker"] = speakerVar.get()
        print(settings["speaker"])
        VmyTTSSingleton.getInstance().set_settings(settings)
    
    # 6개가 한줄인 칸을 만들어서 speakers 리스트를 출력
    # 체크되어있는 칸은 배경색을 회색으로 설정
    speakerFrame = Frame(setlevel)
    speakerFrame.pack()
    for i, (key, value) in enumerate(speakers):
        name = value['name']
        infos = value['info']
        gender = value['gender']
        # infos 는 ,로 구분된 문자열로 변환(원본은 딕셔너리)
        infos = ", ".join([f"{v}" for k, v in infos.items()])
        text = f"{name} : {gender} : {infos}"
        # gender가 남성일 경우 짙은 파란색, 여성일 경우 짙은 빨간색
        fg_color = "#0000BB" if gender == "남성" else "#BB0000"
        # 체크되어있는 칸은 배경색을 회색으로 설정
        if key == settings["speaker"]:
            # bg_color = "#c7c7c7"
            bg_color = "#ffffff"
        else:
            bg_color = "#ffffff"
        
        speakerRadio = Radiobutton(speakerFrame,
                                text=text,
                                variable=speakerVar,
                                value=key,
                                fg=fg_color,
                                bg=bg_color,
                                indicatoron=0,
                                width=25,
                                command=radio_click
                                )
        speakerRadio.grid(row=i//5, column=i%5)
        



    # 저장 버튼 함수
    def save_settings_and_close():
        settings["speaker"] = speakerVar.get()
        print(settings["speaker"])
        VmyTTSSingleton.getInstance().set_settings(settings)
        setlevel.destroy()

    # 저장 버튼
    saveButton = Button(setlevel, text="닫기", command=save_settings_and_close)
    saveButton.pack()

    setlevel.mainloop()