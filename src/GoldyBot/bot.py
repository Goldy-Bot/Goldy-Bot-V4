import asyncio
import sys
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
import importlib.util

import GoldyBot

MODULE_NAME = "GOLDY CORE"

TOKEN = GoldyBot.token.get()
DATABASE_TOKEN = GoldyBot.token.get_database()
intents = nextcord.Intents()
loop = asyncio.get_event_loop()

# Discord Bot
client = commands.Bot(command_prefix = GoldyBot.utility.nextcordpy.prefix.get_prefix, 
case_insensitive=True, intents=intents.all())

# Caching client object.
GoldyBot.cache.main_cache_dict["client"] = client

# Initializing Stuff
database = GoldyBot.database.Database(DATABASE_TOKEN) # Initializing goldy bot database connection.

@client.event
async def on_ready():
    # Goldy Setup.
    await GoldyBot.Goldy().setup(client)

    GoldyBot.log("info_2", f"[{MODULE_NAME}] [BOT READY]")

@GoldyBot.command()
async def goldy(ctx, arg_1, arg_2, arg_3):
    await ctx.send(f"Hi I'm goldy! Args: {arg_1}")

@GoldyBot.command()
async def stop(ctx, reason="A user ran the !stop command."):
    GoldyBot.Goldy().stop(reason)

# Load internal extenstions.
#----------------------------
for extn in os.listdir(GoldyBot.paths.INTERNAL_COGS_V4):
    if extn.endswith('.py'):
        if not extn == "__init__.py":
            # Specify Module
            spec_module = importlib.util.spec_from_file_location(extn[:-3], f"{GoldyBot.paths.INTERNAL_COGS_V4}/{extn}")

            # Get Module
            module = importlib.util.module_from_spec(spec_module)
            
            # Run Module
            spec_module.loader.exec_module(module)

            GoldyBot.logging.log(f"💚 [{MODULE_NAME}] Loaded the internal extenstion '{extn}'!")

# Run Bot
try:
    client.run(TOKEN)
except Exception as e: # Error Handling
    GoldyBot.logging.log("error", e); GoldyBot.Goldy().stop(e)