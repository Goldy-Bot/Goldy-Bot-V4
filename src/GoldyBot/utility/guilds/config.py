import GoldyBot
from GoldyBot.errors import FailedToFindGuildRole

class GuildConfig():
    """This class gives you access to all the configuration settings a Goldy Bot guild possess."""
    def __init__(self, guild_config:GoldyBot.config.Config):
        self.guild_config = guild_config

    @property
    def prefix(self) -> str:
        return self.guild_config.read("prefix")

    def is_extenstion_allowed(self, extenstion_name:str):

        if extenstion_name == None:
            return True

        if extenstion_name in ["Admin"]:
            return True

        config = self.guild_config.read("config")
        allowed_extenstions = config["allowed_extenstions"]
        disallowed_extenstions = config["disallowed_extenstions"]

        if extenstion_name in allowed_extenstions:
            return True

        if extenstion_name in disallowed_extenstions:
            return False

        if allowed_extenstions == ["."]:
            return True

        if disallowed_extenstions == ["."]:
            return False

        return True

    def get_role(self, ctx, role_code_name):
        """Finds and returns a Goldy Bot role from the guild's config with given code name."""
        try:
            role_id = self.guild_config.read("roles")[f"{role_code_name}"]
            return GoldyBot.objects.role.Role(ctx, role_id=role_id)
        except KeyError:
            raise FailedToFindGuildRole

    #TODO: Finish this!
    #TODO: #24 Add logging to the guild config class.


