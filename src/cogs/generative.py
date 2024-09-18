import json
import logging

from os import path, sep, getenv
from re import findall, search
from typing import Optional

import google.generativeai as genai

from discord import Object, Message
from discord.ext.commands import Bot, Cog
from google.generativeai.generative_models import ChatSession, GenerativeModel
from google.generativeai.types.generation_types import GenerateContentResponse


class generative(Cog):
    def __init__(self, Nana: Bot) -> None:
        self.Nana: Bot = Nana
        self.pattern: str = r"<@1231204911988080730>(.+)"
        self.message: Optional[Message] = None
        self.chat: Optional[ChatSession] = None
        logging.info(f"↳ Extension {__name__} loaded.")

    @Cog.listener()
    async def on_message(self, event: Message):
        if findall(self.pattern, event.message.content):
            async with event.channel.typing():
                self.message: Message = await event.message.channel.send("再生產中 <:douzo:1231308616129056778>", silent=True)

                root: str = rf"{path.dirname(path.realpath(__file__))}"

                # Security vulen.
                history_log: str = rf"{root}{sep}..{sep}history.json"

                # 對話初始化
                genai.configure(api_key=getenv("GEMINI_TOKEN"))
                model: GenerativeModel = GenerativeModel("gemini-1.5-pro-latest")

                if not path.isfile(history_log):
                    logging.info("對話紀錄檔未發現，初始化紀錄檔。")
                    file: bytes = open(history_log, "w")
                    file.write(r'{"history":[]}')
                    file.close()
                    logging.info("對話記錄檔建立！")

                with open(history_log, "r") as file:
                    conversation: list[dict] = json.load(file)
                    self.chat: ChatSession = model.start_chat(history=conversation["history"])

                if not len(conversation["history"]):
                    logging.info("對話記錄檔為空，人物設定初始化中。")
                    await self.message.edit(content="蕉蕉初始化中🍌✨")
                    self.chat = model.start_chat(history=[])
                    response: GenerateContentResponse = self.chat.send_message(
                        "請搜尋一下「少女☆歌劇 レヴュースタァライト」並且詳細理解這些資料。接著，妳要模擬室就讀「聖翔音楽学園第99期生，學號15號」的「大場奈奈」。請注意，除了以上設定外您沒有其他設定，因此不要隨意增加設定。另外，妳的任何回答皆只能出現「正體-臺灣」、「英文」以及「日文」回應，在大多時候只選擇以「正體-臺灣」回應即可，且回應時絕對不要提及語言名稱與打破第四道牆！"
                    )

                try:
                    query: str = search(self.pattern, event.message.content).group(1)
                    response: GenerateContentResponse = self.chat.send_message(query)
                    await self.message.edit(content=response.text)
                    self.message = None
                except:
                    await self.message.edit(content="抱歉，奈奈無法回答這個問題 <:nanacry:1231662593534591130>")

            # 儲存聊天紀錄
            conversation: list[dict] = []
            for message in self.chat.history:
                context: str = findall(r"\"(.+)\"", str(message.parts))[0]
                context: str = context.replace("\\n", "")
                session: dict = {"role": message.role, "parts": [{"text": context}]}
                conversation.append(session)

            with open(history_log, "w") as file:
                json.dump({"history": conversation}, file, ensure_ascii=False, indent=2)


async def setup(Nana):
    await Nana.add_cog(generative(Nana), guilds=[Object(id=1221555155716145262)])
