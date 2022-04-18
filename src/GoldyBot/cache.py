from nextcord.ext import commands

import GoldyBot

MODULE_NAME = "CACHE"

main_cache_dict = {
    "client" : None,

    "database" : None,

    "modules" : {

    },

    "internal_modules" : {
        "goldy" : {
            "extenstions" : {
                "core" : {
                    
                }
            }
        }
    },

    "guilds" : {

    }
}

class FindGuilds():
    """A class dedicated to finding guilds from cache."""
    def __init__(self):
        self.goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

    def find_object_by_id(self, guild_id):
        """Searches cache and returns guild object of found guild."""
        guild_code_name = self.goldy_config.read("allowed_guilds")[f"{guild_id}"]
        guild_object:GoldyBot.utility.guilds.guild.Guild = main_cache_dict["guilds"][f"{guild_code_name}"]["object"]
        return guild_object

    def find_object_by_code_name(self, guild_code_name:str):
        """This is faster than finding the guild by id."""
        guild_object:GoldyBot.utility.guilds.guild.Guild = main_cache_dict["guilds"][f"{guild_code_name}"]["object"]
        return guild_object

class FindModules():
    """A class dedicated to finding loaded Goldy Bot modules from cache."""
    def __init__(self):
        self.goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

    def find_object_by_module_name(self, module_name:str):
        """A fast way to grab the class object of a module from Goldy Bot cache."""
        GoldyBot.logging.log(f"[{MODULE_NAME}] Finding module by name...")
        try:
            module_object:GoldyBot.modules.Module = main_cache_dict["modules"][f"{module_name}"]["object"]
            GoldyBot.logging.log(f"[{MODULE_NAME}] Found the module '{module_name}'!")
            return module_object
        except KeyError:
            try:
                module_object:GoldyBot.modules.Module = main_cache_dict["internal_modules"][f"{module_name}"]["object"]
                GoldyBot.logging.log(f"[{MODULE_NAME}] Found the module '{module_name}'!")
                return module_object
            except KeyError:
                GoldyBot.logging.log("error", f"[{MODULE_NAME}] Failed to find the module '{module_name}'.")
                return None