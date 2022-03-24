import GoldyBot

class Extenstion(object):
    """The base class for a Goldy Bot extenstion."""

    def __init__(self, class_object):
        self.class_object = class_object

        GoldyBot.cache.main_cache_dict["extenstions"][f"{class_object.__class__.__name__}"] = self
        print(GoldyBot.cache.main_cache_dict)

    def get_object(self):
        """Retutns the actual class object of the extenstion."""
        return self.class_object