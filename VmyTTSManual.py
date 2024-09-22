from tkinter import *

def new_window_manual():
    # TK 창 생성
    menuallevel = Toplevel()

    # TK 창 이름 설정
    menuallevel.title("옵션 설명")

    # 음색 설명
    speakerLabel = Label(menuallevel, text="음색 설명")
    speakerLabel.pack()

    # 음색 설명 텍스트
    speakerText = """
    0보다 크면 높은 음색,
    0보다 작으면 낮은 음색
    """

    # 음색 설명 텍스트 출력
    speakerTextLabel = Label(menuallevel, text=speakerText)
    speakerTextLabel.pack()

    # 볼륨 설명
    volumeLabel = Label(menuallevel, text="볼륨 설명")
    volumeLabel.pack()

    # 볼륨 설명 텍스트
    volumeText = """
    -5면 0.5배 낮은 볼륨,
    5면 1.5배 더 큰 볼륨,
    0이면 정상 볼륨로 음성 합성
    """

    # 볼륨 설명 텍스트 출력
    volumeTextLabel = Label(menuallevel, text=volumeText)
    volumeTextLabel.pack()

    # 속도 설명
    speedLabel = Label(menuallevel, text="속도 설명")
    speedLabel.pack()

    # 속도 설명 텍스트
    speedText = """
    -5이면 2배 빠른 속도,
    5이면 0.5배 더 느린 속도,
    0이면 정상 속도로 음성 합성
    """

    # 속도 설명 텍스트 출력
    speedTextLabel = Label(menuallevel, text=speedText)
    speedTextLabel.pack()

    # 피치 설명
    pitchLabel = Label(menuallevel, text="피치 설명")
    pitchLabel.pack()

    # 피치 설명 텍스트
    pitchText = """
    -5이면 1.2배 높은 피치,
    5이면 0.8배 더 낮은 피치,
    0이면 정상 피치로 음성 합성
    """

    # 피치 설명 텍스트 출력
    pitchTextLabel = Label(menuallevel, text=pitchText)
    pitchTextLabel.pack()

    # 감정 설명
    emotionLabel = Label(menuallevel, text="감정 설명")
    emotionLabel.pack()

    # 감정 설명 텍스트
    emotionText = """
    지원 목소리
    아라, 아라(pro), 미경(pro), 다인(pro), 유나(pro)
    (단, 아라는 분노 미지원)
    """

    # 감정 설명 텍스트 출력
    emotionTextLabel = Label(menuallevel, text=emotionText)
    emotionTextLabel.pack()

    menuallevel.mainloop()