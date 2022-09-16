from __future__ import annotations
import GoldyBot

MODULE_NAME = "EXTENSION"

class Extension(object):
    """
    The base class for a Goldy Bot extension.

    ---------------
    ### ***``Example:``***

    This is how you set up an extension in a GoldyBot module. 😍

    ```python
    class YourExtension(GoldyBot.Extension):
        def __init__(self, package_module=None):
            super().__init__(self, package_module_name=package_module)

        def loader(self):

            @GoldyBot.command()
            async def uwu(self:YourExtension, ctx):
                await ctx.send(f'Hi, {ctx.author.mention}! UwU!')

    def load():
        YourExtension(package_module_name=__name__)
        pass
    ```
    """

    def __init__(self, class_object, package_module_name:str=None):
        """Tells Goldy Bot to Load this class as an extension."""
        self.class_object:object = class_object
        self.module_name_ = package_module_name
        self.ignored_extensions_list = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON)).read("ignored_extensions")
        
        try:
            if not self.code_name in self.ignored_extensions_list:
                # Cache it.
                #------------
                try:
                    if self.module.is_internal_module:
                        GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extensions"][f"{self.code_name}"] = {}
                        GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extensions"][f"{self.code_name}"]["commands"] = []
                        GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extensions"][f"{self.code_name}"]["object"] = self
                    else:
                        GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extensions"][f"{self.code_name}"] = {}
                        GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extensions"][f"{self.code_name}"]["commands"] = []
                        GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extensions"][f"{self.code_name}"]["object"] = self
                except AttributeError:
                    GoldyBot.logging.log("error", f"""[{MODULE_NAME}] Did you specify the module name when loading this extension. Looks like the module '{self.module_name}' did not get loaded by Goldy Bot. 
                    Perhaps this is a package module and you forgot to specify the module name when loading this extension.\n""")
                    
                    GoldyBot.Goldy().stop(f"I think you forgot to specify the module name when loading the '{self.code_name}' extension.")

                GoldyBot.logging.log(f"[{self.code_name}] Loading my commands...")
                self.loader() # Load commands.

            else:
                GoldyBot.logging.log("info", f"[{class_object.__class__.__name__}] Not loading commands as this extension is ignored.")

        except TypeError as e:
            what_is_incorrect = None

            if self.ignored_extensions_list == None: what_is_incorrect = "ignored_extensions"

            raise GoldyBot.errors.ConfigIsIncorrect(e, what_is_incorrect)

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
        """Returns the name of the module this extension is being called from. This is much faster than grabbing the name with ``module().name``."""
        if self.module_name_ == None:
            return self.class_object.__module__
        else:
            return self.module_name_

    @property
    def module(self) -> GoldyBot.modules.Module:
        return GoldyBot.cache.FindModules().find_object_by_module_name(self.module_name)

    def loader(self):
        """The extension's command loader. This is what Goldy Bot uses to load your commands in an extension."""
        pass

    def get_object(self):
        """Returns the actual class object of the extension."""
        return self.class_object