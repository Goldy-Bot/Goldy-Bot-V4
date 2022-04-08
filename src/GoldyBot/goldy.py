import os
import sys
import GoldyBot
import nextcord

MODULE_NAME = "GOLDY"

class Goldy(object):
    """💛 Goldy herself. More precisely the main class to control the whole of the Bot."""
    def __init__(self):
        pass

    def start(self):
        """Awakens Goldy Bot! 👀💡⏰"""
        GoldyBot.log("warn", f"[{MODULE_NAME}] Goldy Bot is awakening...")

        setup() # Run setup.
        
        # Start V4
        from . import bot

    def ready(self, client:nextcord.Client):
        """Notifies Goldy Bot that the client is ready."""

        Database:GoldyBot.database.Database = GoldyBot.cache.main_cache_dict["database"]

        #  Update database collections.
        #------------------------------
        # Create a database collection for new guilds.
        database_collections = Database.list_collection_names()
        for guild in client.guilds:
            GoldyBot.utility.guilds.guild.Guild(guild) #TODO: Finish this.

            #TODO: Create a system to configure each discord guild.
            #TODO: Check if guild is in database collections by getting it's goldy bot code name.
            pass

    def stop(self, reason="Unknown"):
        """Safely shutdowns Goldy Bot and stops her from perfoming anymore actions, incase you know, things get weird. 😳"""

        GoldyBot.log("warn", f"[{MODULE_NAME}] Goldy is Shuting down...")
        GoldyBot.log("info", f"[{MODULE_NAME}] Here's the reason I was requested to shutdown for >>> {reason}")
        sys.exit()

def setup():
    """Makes sure all files and directoires are setup and ready to go."""
    GoldyBot.log(f"[{MODULE_NAME}] Setup is running...")

    # Directories
    for dir in GoldyBot.settings.directories_to_check:
        if os.path.exists(dir) == False: # If the directory doesn't exist create it.
            GoldyBot.files.File(dir)

    GoldyBot.log("info_2", f"[{MODULE_NAME}] Done!")