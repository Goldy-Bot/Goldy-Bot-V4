import nextcord
import GoldyBot

class Guild():
    """Class that represents a discord guild in Goldy Bot."""
    def __init__(self, guild:nextcord.Guild):
        self.guild = guild

    def setup(self):
        """Setup's the given guild in Goldy Bot with a nextcord guild object."""
        # Generate config folder for guild of there isn't already.
        #-----------------------------------

        # Do ya thing.


        # Create a database collection for the guild if there isn't already.
        #--------------------------------------------------------------------

        # Do ya thing.
        pass

    @property
    def id(self):
        return self.guild.id

    @property
    def config(self) -> GoldyBot.utility.guilds.config.GuildConfig:
        """Returns guild's config class."""
        pass

    @property
    def does_exist(self) -> bool:
        """Commands Goldy Bot to check if the guild exist in config."""
        #TODO: Go into every guild folder and check if the guild exist.
        pass