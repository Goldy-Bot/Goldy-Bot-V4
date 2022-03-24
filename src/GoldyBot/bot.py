import nextcord
from nextcord import Interaction
from nextcord.ext import commands

import GoldyBot

MODULE_NAME = "GOLDY"

TOKEN = GoldyBot.token.get()
intents = nextcord.Intents()

# Discord Bot
client = commands.Bot(command_prefix = "!", 
case_insensitive=True, intents=intents.all())

# Caching client object.
GoldyBot.cache.main_cache_dict["client"] = client

@client.event
async def on_ready():
    GoldyBot.log("info_2", f"[{MODULE_NAME}] [BOT READY]")

@GoldyBot.command
async def goldy(ctx, arg_1, arg_2, arg_3):
    await ctx.send(f"Hi I'm goldy! Args: {arg_1}")

class JeffTheKiller(GoldyBot.Extenstion):
    def __init__(self):
        super().__init__(self)
        
    @GoldyBot.command
    async def jeff(self, ctx):
        await ctx.send("jiff")
        pass
    

# Run Bot
client.run(TOKEN)