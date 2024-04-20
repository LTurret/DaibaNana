import json

from os import path
from os import sep
from os import getenv
from re import findall
from re import search

import google.generativeai as genai

from google.generativeai.generative_models import GenerativeModel
from google.generativeai.types.generation_types import GenerateContentResponse
from google.generativeai.generative_models import ChatSession
from interactions import client
from interactions import listen
from interactions import Extension
from interactions import Message
from interactions.api.events import MessageCreate


class generative(Extension):
    def __init__(self, Nana):
        self.Nana: client = Nana
        self.regex: str = r"<@1231204911988080730>(.+)"
        self.message: Message | None = None
        self.chat: ChatSession | None = None
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: MessageCreate):
        if findall(self.regex, event.message.content):
            self.message: Message = await event.message.channel.send("回應處理中！")
            genai.configure(api_key=getenv("GEMINI_TOKEN"))
            model: GenerativeModel = GenerativeModel("gemini-1.5-pro-latest")
            # model = genai.GenerativeModel('gemini-pro')

            root: str = rf"{path.dirname(path.realpath(__file__))}"
            history_log: str = rf"{root}{sep}..{sep}history.json"

            if not path.isfile(history_log):
                file: bytes = open(history_log, "w")
                file.write('{"history":[]}')
                file.close()
                print("已對話記錄檔建立！")

            with open(history_log, "r") as file:
                conversation: list[dict] = json.load(file)
                self.chat: ChatSession = model.start_chat(history=conversation["history"])

            # 對話初始化
            if not len(conversation["history"]):
                await self.message.edit(content="初始化中")
                self.chat = model.start_chat(history=[])
                response: GenerateContentResponse = self.chat.send_message(
                    "請搜尋一下「少女☆歌劇 レヴュースタァライト」並且詳細理解這些資料。接著，妳要模擬室就讀「聖翔音楽学園第99期生，學號15號」的「大場奈奈」。請注意，除了以上設定外您沒有其他設定，因此不要隨意增加設定。另外，妳的任何回答皆只能出現「正體-臺灣」、「英文」以及「日文」回應，在大多時候只選擇以「正體-臺灣」回應即可，且回應時絕對不要提及語言名稱與打破第四道牆！"
                )

            query: str = search(self.regex, event.message.content).group(1)
            response: GenerateContentResponse = self.chat.send_message(query)

            await self.message.edit(content=response.text)
            self.message = None

            # 儲存聊天紀錄
            conversation: list[dict] = []
            for message in self.chat.history:
                context: str = findall(r"\"(.+)\"", str(message.parts))[0]
                context: str = context.replace("\\n", "")
                session: dict = {"role": message.role, "parts": [{"text": context}]}
                conversation.append(session)

            with open(history_log, "w") as file:
                json.dump({"history": conversation}, file, ensure_ascii=False, indent=2)


def setup(Nana):
    generative(Nana)
