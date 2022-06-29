import nextcord
import GoldyBot
import time

def find_slash_command(command_name:str):
    """Goldy Bot function to find a slash command nextcord application object."""
    client:nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

    for slash_command in client.get_application_commands(rollout=True):
        print(f"AHHH > {slash_command.name}")
        if slash_command.name == command_name:
            return slash_command

    return None