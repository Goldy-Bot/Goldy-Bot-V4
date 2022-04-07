import GoldyBot

class GuildConfig():
    """This class gives you access to all the configuration settings a Goldy Bot guild possess."""
    def __init__(self, guild_config:GoldyBot.config.Config):
        self.guild_config = guild_config

    @property
    def prefix(self) -> str:
        return self.guild_config.read("prefix")

    #TODO: Finish this!


