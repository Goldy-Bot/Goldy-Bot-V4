import GoldyBot

class Extenstion(object):
    """The base class for a Goldy Bot extenstion."""

    def __init__(self, class_object):
        """Tells Goldy Bot to Load this class as an extenstion."""
        self.class_object = class_object
        self.ignored_extenstions_list = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON)).read("ignored_extenstions")
        
        if not self.code_name in self.ignored_extenstions_list:
            # Cache it.
            GoldyBot.cache.main_cache_dict["internal_extenstions"][f"{self.code_name}"] = {}
            GoldyBot.cache.main_cache_dict["internal_extenstions"][f"{self.code_name}"]["object"] = self

            GoldyBot.logging.log(f"[{self.code_name}] Loading my commands...")
            self._loader_() # Load commands.

        else:
            GoldyBot.logging.log("info", f"[{class_object.__class__.__name__}] Not loading commands as this extenstion is ignored.")

        # Setting all variable shortcuts.
        #-----------------------------------
        self.client:GoldyBot.nextcord.Client = GoldyBot.cache.main_cache_dict["client"]
        self.database:GoldyBot.database.Database = GoldyBot.cache.main_cache_dict["database"]

        self.FindGuilds = GoldyBot.cache.FindGuilds()

    @property
    def code_name(self):
        return self.class_object.__class__.__name__

    def _loader_(self):
        """The extenstion's command loader. This is what Goldy Bot uses to load your commands in an extenstion."""
        pass

    def get_object(self):
        """Retutns the actual class object of the extenstion."""
        return self.class_object