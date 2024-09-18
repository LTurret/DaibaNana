import logging

from asyncio import run
from os import getenv, listdir, path, sep

from discord import Game, Intents, Object, Status
from discord.ext.commands import when_mentioned, Bot
from dotenv import load_dotenv


# System symbol
root: str = path.dirname(path.realpath(__file__))

# Service configuration
intents: Intents = Intents.default()
intents.message_content = True
Nana: Bot = Bot(command_prefix=when_mentioned, intents=intents)
Nana.remove_command("help")


@Nana.event
async def on_ready():
    await Nana.change_presence(status=Status.online, activity=Game("スタァライト"))
    await Nana.tree.sync(guild=Object(id=1221555155716145262))
    logging.info("バナナイス！")


async def main():
    async with Nana:
        for filename in listdir(f"{root}{sep}cogs"):
            if filename.endswith(".py"):
                await Nana.load_extension(f"cogs.{filename[:-3]}")

        await Nana.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.CRITICAL)
    logging.basicConfig(
        filename="service.log",
        encoding="utf-8",
        filemode="a",
        level=logging.INFO,
        format="%(levelname)-5s %(asctime)s %(message)s ",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run(main())
