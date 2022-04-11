import GoldyBot
import nextcord
from nextcord.ext import commands

class Extenstion(object):
    """The base class for a Goldy Bot extenstion."""

    def __init__(self, class_object):
        """Tells Goldy Bot to Load this class as an extenstion."""
        self.class_object = class_object
        
        # Cache it.
        GoldyBot.cache.main_cache_dict["internal_extenstions"][f"{class_object.__class__.__name__}"] = {}
        GoldyBot.cache.main_cache_dict["internal_extenstions"][f"{class_object.__class__.__name__}"]["object"] = self

        GoldyBot.logging.log(f"[{class_object.__class__.__name__}] Loading my commands...")
        self.loader() # Load commands.

        # Setting all variable shortcuts.
        #-----------------------------------
        self.client:nextcord.Client = GoldyBot.cache.main_cache_dict["client"]
        self.database:GoldyBot.database.Database = GoldyBot.cache.main_cache_dict["database"]

        self.FindGuilds = GoldyBot.cache.FindGuilds()

    def loader(self):
        """The extenstion's command loader. This is what Goldy Bot uses to load your commands in here."""
        pass

    def get_object(self):
        """Retutns the actual class object of the extenstion."""
        return self.class_object