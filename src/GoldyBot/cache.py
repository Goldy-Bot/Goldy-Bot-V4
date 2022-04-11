from nextcord.ext import commands

import GoldyBot

main_cache_dict = {
    "client" : None,

    "database" : None,

    "extenstions": {
        
    },

    "internal_extenstions": {
        
    },

    "guilds" : {

    }
}

class FindGuilds():
    """A class dedicated to finding guilds from cache."""
    def __init__(self):
        self.goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

    def find_object_by_id(self, guild_id):
        """Searches cache and returns guild object of found guild."""
        guild_code_name = self.goldy_config.read("guilds")[f"{guild_id}"]
        guild_object:GoldyBot.utility.guilds.guild.Guild = main_cache_dict["guilds"][f"{guild_code_name}"]["object"]
        return guild_object