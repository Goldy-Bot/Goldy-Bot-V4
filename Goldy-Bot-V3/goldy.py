import nextcord
import os
from nextcord.ext import commands
from nextcord.ext import *
from nextcord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed
import settings
import asyncio
import sys

from src import goldy_func, goldy_utility, goldy_cache
from src.utility import cmds
from cogs.core import goldy_help_command

#Create config.py file in config folder before importing anything else.
import shutil
goldy_func.create_folder("./config")
if not "config.py" in os.listdir("./config"):
    shutil.copyfile('example_config.py', './config/config.py')

import config.config as config

cog_name = None
goldy_func.print_and_log("app_name", "💛 Goldy Bot " + config.bot_version)
goldy_func.print_and_log()

TOKEN = goldy_func.get_token()
intents = nextcord.Intents()

client = commands.Bot(command_prefix = goldy_utility.servers.prefix.get, help_command=goldy_help_command(), case_insensitive=True, intents=intents.all())
goldy_cache.client = client
os.chdir(os.getcwd())

@client.event
async def on_ready():

    if await goldy_utility.goldy.in_production_mode() == False:
        activity = nextcord.Game(name="IN MAINTENANCE", type=3)
        await client.change_presence(status=nextcord.Status.do_not_disturb, activity=activity)
    
    if await goldy_utility.goldy.in_production_mode() == True:
        activity = nextcord.Game(name=f"{settings.bot_name} | {config.v_short}", type=3)
        await client.change_presence(status=nextcord.Status.online, activity=activity)

    #Things to do during start up.
    await goldy_utility.servers.update()

    goldy_func.print_and_log("info_2", "[BOT READY]")
    goldy_func.print_and_log()

    #Antispam
    goldy_func.print_and_log(None, "Starting Spam Detection Loop...")
    while True:
        try:
            with open("anti_spam.txt", "r+") as file:
                file.truncate(0)

            if await goldy_utility.goldy.in_production_mode() == False: #Silences debug message for antispam if bot is in Production Mode
                goldy_func.print_and_log(None, "[CORE] Spam Detection: Cleared anti_spam.txt")

            await asyncio.sleep(6)

        except FileNotFoundError:
            f = open("anti_spam.txt", "x")
            goldy_func.print_and_log("info", "The file 'anti_spam.txt' did not exist so I created it.")
            goldy_func.print_and_log()

            with open("anti_spam.txt", "r+") as file:
                file.truncate(0)

            if await goldy_utility.goldy.in_production_mode() == False: #Silences debug message for antispam if bot is in Production Mode
                goldy_func.print_and_log(None, "[CORE] Spam Detection: Cleared anti_spam.txt")

            await asyncio.sleep(6)

#This executes only if the file is run as a script.
if __name__ == '__main__':
    #Command line commands.
    command = None
    try:
        command = sys.argv[1]
        try:
            arg = sys.argv[2]
        except IndexError as e:
            arg = None
            pass

        goldy_func.print_and_log("info_2", f":) We got your command line argument. >>> {command} {arg}")

        if command.lower() == "create":
            if arg.lower() == "cog":
                #Create example cog in cogs folder.
                try:
                    import shutil
                    shutil.copyfile('example_cog.py', 'cogs/your_cog.py')
                    goldy_func.print_and_log("info_2", "Cog 'your_cog' created in cogs folder.")

                except Exception as e:
                    goldy_func.print_and_log("error", f"Error Exception in cog creation if statement: ({e})")

        if command.lower() == "update":
            #Force Checks for new servers in servers.json.
            '''
            new_server_found = await servers.update()

            if new_server_found == False:
                goldy_func.print_and_log("warn", "No new servers were found.")
            '''

        raise SystemExit

    except IndexError as e:
        goldy_func.print_and_log("info", f"Couldn't grab command line argument, if you didn't pass an argument ignore this. {e}")
        goldy_func.print_and_log()

    #Goldy Starting Message
    goldy_func.print_and_log("warn", f"{settings.short_name} is starting up...")
    goldy_func.print_and_log()

    goldy_func.print_and_log(None, "Loading Cogs...")

    #Loading cogs here...
    try:
        #Load First cogs...
        for cog in config.load_first:
            if not cog in config.ignore_cogs: #Doesn't load ignored cogs.
                client.load_extension(f'cogs.{cog}')
                print ("💜  Force Loaded {}".format(cog + ".py"))

        #Normal cogs
        for filename in os.listdir('./cogs'):
            if not filename[:-3] in config.ignore_cogs: #Doesn't load ignored cogs.
                if filename.endswith('.py'):
                    try:
                        client.load_extension(f'cogs.{filename[:-3]}')
                        print ("💚  Loaded {}".format(filename))

                    except ExtensionAlreadyLoaded as e:
                        pass

                    except ExtensionFailed as e:
                        print ("🧡  '{}' was not loaded.".format(filename))
                        pass

        goldy_func.print_and_log()
        client.run(TOKEN)

    except FileNotFoundError:
        goldy_func.create_folder(".\\cogs") #Creating cog folder.
        goldy_func.print_and_log("warn", "There was no 'cogs' folder so I created one.")

        try:
            for filename in os.listdir('./cogs'):
                if not filename[:-3] in config.ignore_cogs: #Doesn't load ignored cogs.
                    if filename.endswith('.py'):
                        client.load_extension(f'cogs.{filename[:-3]}')
                        print ("💚  Loaded {}".format(filename))

            client.run(TOKEN)

        except Exception as e:
            goldy_func.print_and_log("error", f"Failed to start bot. {e}")

