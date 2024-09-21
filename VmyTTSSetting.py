import os
import sys
from tkinter import *
import json


# speakers = [("nara", "나라 / 여성(한국어)"),
#             ("jinho", "진호 / 남성(한국어)"),
#             ("clara", "클라라 / 여성(영어)"),
#             ("matt", "매트 / 남성(영어)"),
#             ("yuri", "유리 / 여성(일본어)"),
#             ]

# speaker.json 파일 불러오기 UTF-8
speakers_file = "./speaker.json"
with open(speakers_file, "r", encoding="utf-8") as f:
    speakers = json.load(f)

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
settings_file = "config.json"
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)

# json 파일 저장 (UTF-8)
def save_settings():
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f)
        

root = Tk()

# TK 창 이름 설정
root.title("목소리 설정")


# speaker 설정 (체크박스, 스크롤바, 이름만 출력, 한줄에 5개씩 출력)
speakerLabel = Label(root, text="스피커")
speakerLabel.pack()
speakerVar = StringVar()
speakerVar.set(settings["speaker"])
# 한줄에 5개씩 정렬하기 위해 Frame 사용
# 각 행, 열 간격 정렬
# pack() 함수는 위젯을 화면에 배치하는 함수
# pack(side=LEFT) : 왼쪽으로 정렬
# pack(side=RIGHT) : 오른쪽으로 정렬
# pack(side=TOP) : 위쪽으로 정렬
# pack(side=BOTTOM) : 아래쪽으로 정렬
# pack(fill=X) : X축으로 채움
# pack(fill=Y) : Y축으로 채움
# pack(fill=BOTH) : X, Y축으로 채움
# pack(expand=True) : 화면 크기에 맞게 확장


# 6개가 한줄인 칸을 만들어서 speakers 리스트를 출력
# 체크되어있는 칸은 배경색을 투명도 50%의 검은색으로 설정
speakerFrame = Frame(root)
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
    # 체크되어있는 칸은 배경색을 투명도 50%의 검은색으로 설정
    if key == settings["speaker"]:
        bg_color = "#c7c7c7"
    else:
        bg_color = "#ffffff"
    
    speakerRadio = Radiobutton(speakerFrame,
                            text=text,
                            variable=speakerVar,
                            value=key,
                            fg=fg_color,
                            bg=bg_color,
                            )
    speakerRadio.grid(row=i//6, column=i%6)
    

# for i, (key, value) in enumerate(speakers):
    # name = value['name']
    # infos = value['info']
    # gender = value['gender']
    # # infos 는 ,로 구분된 문자열로 변환(원본은 딕셔너리)
    # infos = ", ".join([f"{v}" for k, v in infos.items()])
    # text = f"{name} : {gender} : {infos}"
    # speakerRadio = Radiobutton(root, text=text, variable=speakerVar, value=key)
    # speakerRadio.pack()



# 저장 버튼 함수
def save_settings_and_close():
    settings["speaker"] = speakerVar.get()

    save_settings()
    root.quit()

# 저장 버튼
saveButton = Button(root, text="저장", command=save_settings_and_close)
saveButton.pack()

root.mainloop()