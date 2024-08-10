from interactions import client
from interactions import slash_command
from interactions import Extension
from interactions import SlashContext


class voice(Extension):
    def __init__(self, Nana):
        self.Nana: client = Nana

    @slash_command(name="vc", description="奈奈陪你", scopes=[1221555155716145262, 943075990295416842])
    async def vc(self, ctx: SlashContext):
        await ctx.send("joined", ephemeral=True)
        await ctx.author.voice.channel.connect()


def setup(Nana):
    voice(Nana)
