import logging

from os import getenv
from typing import Optional

from discord import Guild, Message, Role, TextChannel
from discord.ext.commands import Bot, Cog
from dotenv import load_dotenv

load_dotenv()


class verification(Cog):
    def __init__(self, Nana):
        self.Nana: Bot = Nana
        self.CHANNEL: Optional[TextChannel] = None
        self.MESSAGE: Optional[Message] = None
        self.GUILD: Optional[Guild] = None
        self.ROLE: Optional[Role] = None
        logging.info(f"↳ Extension {__name__} loaded.")

    @Cog.listener()
    async def on_ready(self):
        self.CHANNEL = int(getenv("ROLE_CHANNEL"))
        self.MESSAGE = int(getenv("ROLE_MESSAGE"))
        self.GUILD = self.Nana.get_guild(int(getenv("ROLE_SERVEER")))
        self.ROLE = self.GUILD.get_role(int(getenv("ROLE")))

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = int(payload.channel_id)
        message = int(payload.message_id)
        emoji = payload.emoji.name

        if channel == self.CHANNEL and message == self.MESSAGE:
            if emoji == "🧁":
                await payload.member.add_roles(self.ROLE)
                logging.info("Verification tiggered, role added.")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = int(payload.channel_id)
        message = int(payload.message_id)
        emoji = payload.emoji.name

        if channel == self.CHANNEL and message == self.MESSAGE:
            if emoji == "🧁":
                member = await self.GUILD.fetch_member(payload.user_id)
                await member.remove_roles(self.ROLE)
                logging.info("Verification tiggered, role removed.")


async def setup(Nana):
    await Nana.add_cog(verification(Nana))
