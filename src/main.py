from os import getenv
from os import listdir
from os import path
from os import sep
from os import system

from dotenv import load_dotenv
from interactions import listen
from interactions import Activity
from interactions import Client
from interactions import Intents

Nana = Client(delete_unused_application_cmds=True, intents=Intents.ALL, activity=Activity(name="スタァライト"))


@listen()
async def on_startup():
    # system("clear")
    print("バナナイス！")


root: str = rf"{path.dirname(path.realpath(__file__))}"

load_dotenv(f"{root}{sep}..{sep}.env")

for filename in listdir(f"{root}{sep}cogs"):
    if filename.endswith(".py"):
        print(f"Loading extension: {filename}")
        Nana.load_extension(f"cogs.{filename[:-3]}")

Nana.start(getenv("BOT_TOKEN"))
