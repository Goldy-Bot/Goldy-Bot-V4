import os
import nextcord
import GoldyBot

GUILD_CONFIG_TEMPLATE_JSON_PATH = GoldyBot.paths.GOLDY_BOT + "/utility/guilds/guild_config_template.json"

class Guild():
    """Class that represents a discord guild in Goldy Bot."""
    def __init__(self, guild:nextcord.Guild):
        self.guild = guild
        self.config_file = None

        # Get code name.
        goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))
        self.code_name_ = goldy_config.read("guilds")[f"{self.id}"]

    def setup(self):
        """Setup's the given guild in Goldy Bot with a nextcord guild object."""
        # Generate config folder for guild of there isn't already.
        #-----------------------------------

        # Create guild config folder.
        GUILD_CONFIG_FOLDER_PATH = GoldyBot.files.File(GoldyBot.paths.CONFIG + f"/{self.code_name}").file_path

        # Create guild config file.
        self.config_file = GoldyBot.files.File(GUILD_CONFIG_FOLDER_PATH + "/config.json")

        # If the config is empty, write the guild config template to it.
        if self.config_file.read() == "":
            self.config_file.write(GoldyBot.files.File(GUILD_CONFIG_TEMPLATE_JSON_PATH).read())


        # Create a database collection for the guild if there isn't already.
        #--------------------------------------------------------------------

        # Do ya thing. #TODO: Create database collection.
        pass

    @property
    def id(self):
        return self.guild.id

    @property
    def code_name(self):
        return self.code_name_

    @property
    def config(self) -> GoldyBot.utility.guilds.config.GuildConfig:
        """Returns guild's config class."""
        #TODO: If the config does not exist run guild setup.
        return GoldyBot.utility.guilds.config.GuildConfig(GoldyBot.config.Config())

    @property
    def does_exist(self) -> bool:
        """Commands Goldy Bot to check if the guild exist in config."""
        if self.code_name in os.listdir(GoldyBot.paths.CONFIG):
            return True
        else:
            return False