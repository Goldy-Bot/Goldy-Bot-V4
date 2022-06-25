import datetime
import GoldyBot

async def change(game_name:str, status:GoldyBot.nextcord.Status=None):
    """Commands Goldy Bot to change presence."""
    client:GoldyBot.nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

    game = GoldyBot.nextcord.Game(game_name)

    if status == None:
        actual_status = client.status
    else:
        actual_status = status

    await client.change_presence(status=actual_status, activity=game)