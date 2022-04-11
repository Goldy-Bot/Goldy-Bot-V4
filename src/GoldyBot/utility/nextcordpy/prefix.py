import GoldyBot
import nextcord

goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

def get_prefix(client, command:nextcord.Message):
    
    # Get the guild object from the cache.
    guild:GoldyBot.utility.guilds.guild.Guild = GoldyBot.cache.main_cache_dict["guilds"][goldy_config.read("guilds")[f"{command.guild.id}"]]["object"]
    
    # Get the guild prefix from it's config.
    return guild.config.prefix