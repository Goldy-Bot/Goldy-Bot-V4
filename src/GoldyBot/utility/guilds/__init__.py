from typing import List
import nextcord
import GoldyBot
from . import config, guild

def get_guild_ids() -> List[int]:
    """Returns the id of all the guilds Goldy Bot is in."""
    client:nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

    guilds_ids = []

    for guild in client.guilds:
        guilds_ids.append(guild.id)

    return guilds_ids