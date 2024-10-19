from VmyTTSGlobal import VmyTTSSingleton
from chzzkpy.chat import ChatClient, ChatMessage

# 라이브에서 챗 읽어오기

uid = '' # 치지직 uid

#uid파일에서 읽어오기
with open('uid', 'r') as f:
    uid = f.read()

client = ChatClient(uid)


@client.event
async def on_chat(message: ChatMessage):
    if message.profile.nickname == "주차장P":
        # 메세지가 !로 시작하지 않을때만 출력
        if not message.content.startswith("!"):
            print(f"{message.profile.nickname}: {message.content}")
            # VmyTTSSingleton.getInstance().speak_livechat(message.content)


client.run()
