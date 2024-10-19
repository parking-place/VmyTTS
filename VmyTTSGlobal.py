import json
from VmyTTSSpeakers import SPEAKERS

VERSION = "0.3.1 a"

URL = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

CLIENT_AUTH = {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
}

SETTINGS = {
    "speaker": "nara",
    "volume": "0",
    "speed": "0",
    "pitch": "0",
    "emotion": "0",
    "emotion-strength" : "0",
    "alpha": "0",
    "info": "",
    "WinVolume": "50",
    "Mutemode": False,
    "shortcut-abled": True,
}

DEFAULT_SETTINGS = {
    "speaker": "nara",
    "volume": "0",
    "speed": "0",
    "pitch": "0",
    "emotion": "0",
    "emotion-strength" : "0",
    "alpha": "0",
    "info": "",
    "WinVolume": "50",
    "Mutemode": False,
    "shortcut-abled": True,
}

DEDEFAULT_SHORTCUTS = {
    "ㅋ" : "키",
    "ㄹㅇ": "리얼",
    "ㅇㅈ" : "인정",
    "ㄱㅅ" : "감사",
    "ㅈㅅ" : "죄송",
    "ㅂㅇ" : "바이",
    "ㄱㅊ" : "갠찬",
    "ㅎㅇ" : "하이",
    "ㅇㅎ" : "아하",
    "ㅂㅂ" : "바이바이",
    "ㄱㄱ" : "고고",
    "ㅅㄱ" : "수고",
    "ㅇㄷ?" : "어디?",
    "ㅁㅇㅁㅇ" : "모야모야",
    "ㅁㅇ?" : "머임?",
}

class VmyTTSSingleton:
    __instance = None

    version = ''
    url= ''
    client_auth = {}
    settings = {}
    default_settings = {}
    info_refreshing_func = None
    shortcut  = {}
    defalut_shortcuts = {}
    shortcut_abled = True
    
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(VmyTTSSingleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
    
    @staticmethod
    def getInstance():
        if VmyTTSSingleton.__instance == None:
            VmyTTSSingleton()
        return VmyTTSSingleton.__instance

    def __init__(self):
        self.version = VERSION
        self.url = URL
        self.client_auth = CLIENT_AUTH
        self.settings = SETTINGS
        self.default_settings = DEFAULT_SETTINGS
        self.default_shortcuts = DEDEFAULT_SHORTCUTS
        self.shortcut_abled = True
        
        self.load_shortcuts()
        self.load_settings()
        self.load_keys()
    
    def set_info_refreshing_func(self, func):
        self.info_refreshing_func = func
    
    def get_version(self):
        return self.version
    
    def get_url(self):
        return self.url
    
    def get_client_auth(self):
        return self.client_auth
    
    def get_settings(self):
        return self.settings
    
    def get_default_settings(self):
        return self.default_settings
    
    def get_shortcuts(self):
        return self.shortcut
    
    def get_default_shortcuts(self):
        return self.default_shortcuts
    
    def set_shortcuts(self, shortcuts):
        self.shortcut = shortcuts
        self.save_shortcuts()
    
    def set_shortcut_abled(self, abled):
        self.shortcut_abled = abled

    def set_settings(self, settings):
        self.settings = settings
        
        # 스피커 정보를 가져오기
        try :
            speaker_infos = SPEAKERS[self.settings["speaker"]]
            # 정보를 이름|성별|언어 format으로 변환
            speaker_info = f"{speaker_infos['name']}"
            speaker_info += f"|{speaker_infos['gender']}"
            infos = speaker_infos['info']
            info_str = ""
            for info in infos:
                info_str += f"|{infos[info]}"
            speaker_info += info_str
            
            self.settings["info"] = speaker_info
        except Exception as e:
            print(e)
            print("Speaker 정보를 불러오는데 실패했습니다.")
            self.settings = self.default_settings
        
        self.save_settings()
        self.info_refreshing_func()
        
    def set_client_auth(self, client_auth):
        self.client_auth = client_auth
    
    def load_settings(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except:
            self.settings = self.default_settings
            self.save_settings()
        
        # 스피커 정보를 가져오기
        try :
            speaker_infos = SPEAKERS[self.settings["speaker"]]
            # 정보를 이름|성별|언어 format으로 변환
            speaker_info = f"{speaker_infos['name']}"
            speaker_info += f"|{speaker_infos['gender']}"
            infos = speaker_infos['info']
            info_str = ""
            for info in infos:
                info_str += f"|{infos[info]}"
            speaker_info += info_str
            
            self.settings["info"] = speaker_info
            self.save_settings()
        except Exception as e:
            print(e)
            print("Speaker 정보를 불러오는데 실패했습니다.")
            self.settings = self.default_settings
        
        # 불러온 세팅에 뮤트모드가 없을 경우 추가
        if "Mutemode" not in self.settings:
            self.settings["Mutemode"] = False
            self.save_settings()
        
        # 불러온 세팅에 단축어 사용여부가 없을 경우 추가
        if "shortcut-abled" not in self.settings:
            self.settings["shortcut-abled"] = True
            self.save_settings()
        
    def load_shortcuts(self):
        try:
            with open("shortcut.json", "r", encoding="utf-8") as f:
                self.shortcut = json.load(f)
        except:
            self.shortcut = self.default_shortcuts
            self.save_shortcuts()
    
    def save_shortcuts(self):
        with open("shortcut.json", "w", encoding="utf-8") as f:
            json.dump(self.shortcut, f)
    
    def save_settings(self):
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f)
    
    def load_keys(self):

        with open("keys.json", "r", encoding="utf-8") as f:
            keys = json.load(f)
        
        self.client_auth["client_id"] = keys["client_id"]
        self.client_auth["client_secret"] = keys["client_secret"]
    
    def replace_shortcut(self, text):
        for key, value in self.shortcut.items():
            text = text.replace(key, value)
        return text