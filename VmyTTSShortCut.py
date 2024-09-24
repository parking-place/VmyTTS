# 단축어 기능
from tkinter import *
import json
from VmyTTSGlobal import VmyTTSSingleton


def new_window_shortcut():
    
    # TK 창 생성
    shortcutlevel = Toplevel()
    
    # TK 창 이름 설정
    shortcutlevel.title("단축어 설정")
    
    # 단축어 설정
    # 프레임안에
    # 단축어 이름 : 단축어 내용 : 삭제 버튼
    
    # 밑에는 
    # 단축어 이름 : 단축어 내용 : 추가 버튼
    
    
    # 삭제 버튼
    def delete_shortcut(key):
        shortcut = VmyTTSSingleton.getInstance().get_shortcuts()
        del shortcut[key]
        VmyTTSSingleton.getInstance().set_shortcuts(shortcut)
        shortcutlevel.destroy()
        new_window_shortcut()
    
    # 추가 버튼
    def add_shortcut():
        key = key_entry.get()
        value = value_entry.get()
        # 키와 값이 모두 입력되어있을 때만 추가
        if key == "" or value == "":
            return
        # 키와 값의 좌우 공백 제거
        key = key.strip()
        value = value.strip()
        # 단축어 추가
        shortcut = VmyTTSSingleton.getInstance().get_shortcuts()
        shortcut[key] = value
        VmyTTSSingleton.getInstance().set_shortcuts(shortcut)
        shortcutlevel.destroy()
        new_window_shortcut()
    
    # 윈도우 새로고침
    def refresh():
        shortcutlevel.destroy()
        new_window_shortcut()
    
    # 단축어 갯수만큼 프레임 생성
    for i, (key, value) in enumerate(VmyTTSSingleton.getInstance().get_shortcuts().items()):
        frame = Frame(shortcutlevel)
        frame.pack()
        
        # 단축어 이름
        key_label = Label(frame, text=key)
        key_label.pack(side=LEFT)
        
        # -> 표시
        colon_label = Label(frame, text=" -> ")
        colon_label.pack(side=LEFT)
        
        # 단축어 내용
        value_label = Label(frame, text=value)
        value_label.pack(side=LEFT)
        
        # 삭제 버튼
        delete_button = Button(frame, text="삭제", command=lambda key=key: delete_shortcut(key))
        delete_button.pack(side=LEFT)
    
    # 추가 프레임 생성
    add_frame = Frame(shortcutlevel)
    add_frame.pack()
    
    # 단축어 이름 입력
    key_entry = Entry(add_frame)
    key_entry.pack(side=LEFT)
    
    # -> 표시
    colon_label = Label(add_frame, text=" -> ")
    colon_label.pack(side=LEFT)
    
    # 단축어 내용 입력
    value_entry = Entry(add_frame)
    value_entry.pack(side=LEFT)
    
    # 추가 버튼
    add_button = Button(add_frame, text="추가", command=add_shortcut)
    add_button.pack(side=LEFT)
    
    # 단축어 사용여부 함수
    def shortcut_check_func():
        settings = VmyTTSSingleton.getInstance().get_settings()
        settings["shortcut-abled"] = not settings["shortcut-abled"]
        VmyTTSSingleton.getInstance().set_settings(settings)
    
    # 단축어 사용여부 체크박스
    shortcut_check = Checkbutton(shortcutlevel, text="단축어 사용", command=shortcut_check_func)
    # 현재 단축어 사용여부 체크박스 상태로 설정
    if VmyTTSSingleton.getInstance().get_settings()["shortcut-abled"]:
        shortcut_check.select()
    else:
        shortcut_check.deselect()
    shortcut_check.pack(side=LEFT)
    
    # 닫기 버튼
    close_button = Button(shortcutlevel, text="닫기", command=shortcutlevel.destroy)
    close_button.pack()
    
    



