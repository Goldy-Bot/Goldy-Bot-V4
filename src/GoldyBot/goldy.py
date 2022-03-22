import os
import sys
import threading
from multiprocessing import Process
import GoldyBot

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