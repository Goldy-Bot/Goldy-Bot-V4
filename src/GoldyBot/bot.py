import nextcord
from nextcord.ext import commands
import GoldyBot

TOKEN = GoldyBot.token.get()
intents = nextcord.Intents()

# Discord Bot
client = commands.Bot(command_prefix = "", help_command=GoldyBot.utility.nextcordpy.help_command.goldy_help_command(), 
case_insensitive=True, intents=intents.all())

# Caching client object.
GoldyBot.cache.main_cache_dict["client"] = client

@client.event
async def on_ready():
    GoldyBot.log("info_2", "[BOT READY]")

# Run Bot
client.run(TOKEN)