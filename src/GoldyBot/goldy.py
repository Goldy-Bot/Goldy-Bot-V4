import os
import sys
import GoldyBot, devgoldyutils
import nextcord
import threading, _thread
import time

MODULE_NAME = "GOLDY"

class Goldy(object):
    """💛 Goldy herself. More precisely the main class to control the whole of the Bot."""
    def __init__(self):
        pass

    def start(self):
        """Awakens Goldy Bot! 👀💡⏰"""
        GoldyBot.log("warn", f"[{MODULE_NAME}] Goldy Bot is awakening...")

        file_setup() # Run file setup.
        
        # Fixes some werid as fu#k bug when stopping the bot.
        if GoldyBot.system.platform.system() == 'Windows':
            GoldyBot.asyncio.set_event_loop_policy(GoldyBot.asyncio.WindowsSelectorEventLoopPolicy())

        print("")
        input_thread = threading.Thread(target=input_loop)
        input_thread.setDaemon(True)
        input_thread.start()

        # Start V4
        from . import bot

    async def setup(self, client:nextcord.Client):
        """Notifies Goldy Bot that the client is ready and it can do it's setup."""

        #  Run setup on all allowed guilds.
        #------------------------------
        for guild in client.guilds:
            goldy_bot_guild = GoldyBot.utility.guilds.guild.Guild(guild) #TODO: Finish this.

            if goldy_bot_guild.is_allowed:
                await goldy_bot_guild.setup()

        #  Check if the config files have been edited for the guilds.
        not_edited_config_guilds = []
        for guild_ in GoldyBot.cache.main_cache_dict["guilds"]:
            guild:GoldyBot.utility.guilds.guild.Guild = GoldyBot.cache.main_cache_dict["guilds"][guild_]["object"]

            if not guild.has_config_been_edited:
                not_edited_config_guilds.append(guild.code_name)

        if not not_edited_config_guilds == []:
            self.stop(reason=f"Guild configs MUST be edited! These guilds have not had their config's edited: {not_edited_config_guilds}")

        GoldyBot.logging.log(f"[{MODULE_NAME}] Guilds Setup Done!")

    def stop(self, reason="Unknown"):
        """Safely shutdowns Goldy Bot and stops her from perfoming anymore actions, incase you know, things get weird. 😳"""

        GoldyBot.log("warn", f"[{MODULE_NAME}] Goldy is Shuting down...")
        GoldyBot.log("info", f"[{MODULE_NAME}] Here's the reason why I was requested to shutdown for >>> {reason}")
        sys.exit(reason)

def file_setup():
    """Makes sure all files and directoires are setup and ready to go."""
    GoldyBot.log(f"[{MODULE_NAME}] Setup is running...")

    # Directories
    for dir in GoldyBot.settings.directories_to_check:
        if os.path.exists(dir) == False: # If the directory doesn't exist create it.
            GoldyBot.files.File(dir)

    # Create goldy.json if it doesn't exist already.
    if not "goldy.json" in os.listdir(GoldyBot.paths.CONFIG):
        goldy_config = GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON).write(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON_TEMPLATE).read())

    GoldyBot.log("info_2", f"[{MODULE_NAME}] File Setup Done!")

def input_loop():
    console = devgoldyutils.Console()
    goldy = Goldy()

    time.sleep(6)

    try:
        while True:
            command = input("")

            if command.lower() == "stop":
                raise EOFError

            time.sleep(0.1)
            
    except EOFError:
        print("\n")
        _thread.interrupt_main()
        goldy.stop("Master commanded me to stop!")