import GoldyBot
import nextcord

def get_prefix(client, command:nextcord.Message):
    # Get the guild object from the cache.
    guild:GoldyBot.utility.guilds.guild.Guild = GoldyBot.cache.FindGuilds().find_object_by_id(command.guild.id)
    prefix = guild.config.prefix

    if prefix == None:
        return "!"
    else:
        return prefix