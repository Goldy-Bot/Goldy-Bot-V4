import GoldyBot
from GoldyBot.errors import FailedToFindGuildRole

class GuildConfig():
    """This class gives you access to all the configuration settings a Goldy Bot guild possess."""
    def __init__(self, guild_config:GoldyBot.config.Config):
        self.guild_config = guild_config

    @property
    def prefix(self) -> str:
        return self.guild_config.read("prefix")

    def get_role(self, ctx, role_code_name):
        """Finds and returns a Goldy Bot role from the guild's config with given code name."""
        try:
            role_id = self.guild_config.read("roles")[f"{role_code_name}"]
            return GoldyBot.objects.role.Role(ctx, role_id=role_id)
        except KeyError:
            raise FailedToFindGuildRole

    #TODO: Finish this!
    #TODO: #24 Add logging to the guild config class.


