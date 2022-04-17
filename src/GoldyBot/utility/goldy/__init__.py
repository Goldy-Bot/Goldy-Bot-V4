from . import slash, colours, embed

import GoldyBot

def get_pfp():
    """Returns the profile picture of Goldy Bot."""
    client:GoldyBot.nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

    pfp_url = client.user.display_avatar.url

    if pfp_url == None:
        return "https://htmlcolors.com/color-image/2f3136.png" # Blank Image
    else:
        return pfp_url