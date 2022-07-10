import GoldyBot
import nextcord

def get_prefix(client, command:nextcord.Message):
    # Get the guild object from the cache.
    prefix = None
    
    guild:GoldyBot.utility.guilds.guild.Guild = GoldyBot.cache.FindGuilds().find_object_by_id(command.guild.id)

    if not guild == None:
        prefix = guild.config.prefix

    if prefix == None:
        return "!"
    else:
        return prefix