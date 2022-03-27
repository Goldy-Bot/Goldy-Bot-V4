import GoldyBot

class Extenstion(object):
    """The base class for a Goldy Bot extenstion."""

    def __init__(self, class_object):
        """Tells Goldy Bot to Load this class as an extenstion."""
        self.class_object = class_object

        GoldyBot.cache.main_cache_dict["extenstions"][f"{class_object.__class__.__name__}"] = self

        GoldyBot.logging.log(f"[{class_object.__class__.__name__}] Loading my commands...")
        self.loader() # Load commands.

    def loader(self):
        """The extenstion's command loader. This is what Goldy Bot uses to load your commands in here."""
        pass

    def get_object(self):
        """Retutns the actual class object of the extenstion."""
        return self.class_object