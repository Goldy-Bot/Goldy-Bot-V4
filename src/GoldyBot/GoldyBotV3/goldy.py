import nextcord
import os
from nextcord.ext import commands
from nextcord.ext import *
from nextcord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed
from . import settings
import asyncio
import sys

import GoldyBot # V4

from .src import goldy_func, goldy_utility, goldy_cache
from .src.utility import cmds
from ..internal_cogs.v3.core import goldy_help_command

MODULE_NAME = "GOLDY V3"
goldy_func.print_and_log("app_name", "💛 Goldy Bot " + GoldyBot.info.bot_version)
goldy_func.print_and_log()

TOKEN = GoldyBot.token.get()
intents = nextcord.Intents()

client = commands.Bot(command_prefix = goldy_utility.servers.prefix.get, help_command=goldy_help_command(), case_insensitive=True, intents=intents.all())
goldy_cache.client = client

config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

@client.event
async def on_ready():

    if await goldy_utility.goldy.in_production_mode() == False:
        activity = nextcord.Game(name="IN MAINTENANCE", type=3)
        await client.change_presence(status=nextcord.Status.do_not_disturb, activity=activity)
    
    if await goldy_utility.goldy.in_production_mode() == True:
        activity = nextcord.Game(name=f"{settings.bot_name} | {GoldyBot.info.v_short}", type=3)
        await client.change_presence(status=nextcord.Status.online, activity=activity)

    #Things to do during start up.
    await goldy_utility.servers.update()

    goldy_func.print_and_log("info_2", "[BOT READY]")
    goldy_func.print_and_log()

    #Antispam
    goldy_func.print_and_log(None, f"[{MODULE_NAME}] Starting Spam Detection Loop...")
    while True:
        try:
            with open("anti_spam.txt", "r+") as file:
                file.truncate(0)

            if await goldy_utility.goldy.in_production_mode() == False: #Silences debug message for antispam if bot is in Production Mode
                goldy_func.print_and_log(None, f"[{MODULE_NAME}] Spam Detection: Cleared anti_spam.txt")

            await asyncio.sleep(6)

        except FileNotFoundError:
            f = open("anti_spam.txt", "x")
            goldy_func.print_and_log("info", f"[{MODULE_NAME}] The file 'anti_spam.txt' did not exist so I created it.")
            goldy_func.print_and_log()

            with open("anti_spam.txt", "r+") as file:
                file.truncate(0)

            if await goldy_utility.goldy.in_production_mode() == False: #Silences debug message for antispam if bot is in Production Mode
                goldy_func.print_and_log(None, f"[{MODULE_NAME}] Spam Detection: Cleared anti_spam.txt")

            await asyncio.sleep(6)

def start():

    #Goldy Starting Message
    goldy_func.print_and_log("warn", f"[{MODULE_NAME}] {settings.short_name} is starting up...")
    goldy_func.print_and_log()

    goldy_func.print_and_log(None, f"[{MODULE_NAME}] Loading Cogs...")

    #Load First cogs...
    for cog in config.read("load_first"):
        if not cog in config.read("ignore_cogs"): #Doesn't load ignored cogs.
            client.load_extension(f'GoldyBot.internal_cogs.v3.{cog}')
            print (f"[{MODULE_NAME}] 💜  Force Loaded {cog}.py")

    #Normal cogs
    for filename in os.listdir('./GoldyBot/internal_cogs/v3'):
        if not filename[:-3] in config.read("ignore_cogs"): #Doesn't load ignored cogs.
            if filename.endswith('.py'):
                try:
                    client.load_extension(f'GoldyBot.internal_cogs.v3.{filename[:-3]}')
                    print (f"[{MODULE_NAME}] 💚  Loaded {filename}")

                except ExtensionAlreadyLoaded as e:
                    pass

                except ExtensionFailed as e:
                    print (f"[{MODULE_NAME}] 🧡  '{filename}' was not loaded.")
                    pass

    goldy_func.print_and_log()
    client.run(TOKEN)

