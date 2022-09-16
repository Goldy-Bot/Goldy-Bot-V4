import nextcord
import GoldyBot
import time

MODULE_NAME = "NEXTCORD COMMANDS"

def find_slash_command(command_name:str) -> nextcord.BaseApplicationCommand:
    """Goldy Bot function to find a slash command nextcord application object."""
    client:nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

    for slash_command in client.get_all_application_commands():
        if slash_command.name == command_name:
            GoldyBot.logging.log(f"[{MODULE_NAME}] The slash command '{command_name}' was found!")
            return slash_command

    GoldyBot.logging.log("warn", f"[{MODULE_NAME}] The slash command '{command_name}' was NOT found!")
    return None