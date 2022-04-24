from __future__ import annotations
import GoldyBot

MODULE_NAME = "EXTENSTION"

class Extenstion(object):
    """The base class for a Goldy Bot extenstion."""

    def __init__(self, class_object, package_module_name:str=None):
        """Tells Goldy Bot to Load this class as an extenstion."""
        self.class_object:object = class_object
        self.module_name_ = package_module_name
        self.ignored_extenstions_list = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON)).read("ignored_extenstions")
        
        if not self.code_name in self.ignored_extenstions_list:
            # Cache it.
            #------------
            try:
                if self.module.is_internal_module:
                    GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extenstions"][f"{self.code_name}"] = {}
                    GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extenstions"][f"{self.code_name}"]["commands"] = []
                    GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extenstions"][f"{self.code_name}"]["object"] = self
                else:
                    GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extenstions"][f"{self.code_name}"] = {}
                    GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extenstions"][f"{self.code_name}"]["commands"] = []
                    GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extenstions"][f"{self.code_name}"]["object"] = self
            except AttributeError:
                GoldyBot.logging.log("error", f"""[{MODULE_NAME}] Did you specify the module name when loading this extenstion. Looks like the module '{self.module_name}' did not get loaded by Goldy Bot. 
                Perhaps this is a package module and you forgot to specify the module name when loading this extenstion.\n""")
                
                GoldyBot.Goldy().stop(f"I think you forgot to specify the module name when loading the '{self.code_name}' extenstion.")

            GoldyBot.logging.log(f"[{self.code_name}] Loading my commands...")
            self.loader() # Load commands.

        else:
            GoldyBot.logging.log("info", f"[{class_object.__class__.__name__}] Not loading commands as this extenstion is ignored.")

        # Setting all variable shortcuts.
        #-----------------------------------
        self.client:GoldyBot.nextcord.Client = GoldyBot.cache.main_cache_dict["client"]
        self.database:GoldyBot.database.Database = GoldyBot.cache.main_cache_dict["database"]

        self.FindGuilds = GoldyBot.cache.FindGuilds()

        self.msg = GoldyBot.utility.msgs

    @property
    def code_name(self):
        return self.class_object.__class__.__name__

    @property
    def module_name(self):
        """Returns the name of the module this extenstion is being called from. This is much faster than grabing the name with ``module().name``."""
        if self.module_name_ == None:
            return self.class_object.__module__
        else:
            return self.module_name_

    @property
    def module(self) -> GoldyBot.modules.Module:
        return GoldyBot.cache.FindModules().find_object_by_module_name(self.module_name)

    def loader(self):
        """The extenstion's command loader. This is what Goldy Bot uses to load your commands in an extenstion."""
        pass

    def get_object(self):
        """Retutns the actual class object of the extenstion."""
        return self.class_object