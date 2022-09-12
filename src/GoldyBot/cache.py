from __future__ import annotations

import GoldyBot
from nextcord.ext import commands

MODULE_NAME = "CACHE"

main_cache_dict = {
    "client" : None,

    "goldy_class" : None,

    "database" : None,

    "modules" : {

    },

    "internal_modules" : {
        "goldy" : {
            "extensions" : {
                "core" : {
                    "commands" : []
                }
            }
        }
    },

    "guilds" : {

    }
}

def database() -> GoldyBot.database.Database|None:
    """Returns current database."""
    return main_cache_dict["database"]

class FindGuilds():
    """A class dedicated to finding guilds from cache."""
    def __init__(self, goldy_config:GoldyBot.config.Config=None):
        if goldy_config == None:
            self.goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))
        else:
            self.goldy_config = goldy_config

    def find_object_by_id(self, guild_id):
        """Searches cache and returns guild object of found guild."""
        try:
            guild_code_name = self.goldy_config.read("allowed_guilds")[f"{guild_id}"]
            guild_object:GoldyBot.utility.guilds.guild.Guild = main_cache_dict["guilds"][f"{guild_code_name}"]["object"]
            #TODO: #23 Add return None if guild is not found.
            return guild_object
        except KeyError:
            return None

    def find_object_by_code_name(self, guild_code_name:str):
        """This is faster than finding the guild by id."""
        try:
            guild_object:GoldyBot.utility.guilds.guild.Guild = main_cache_dict["guilds"][f"{guild_code_name}"]["object"]
            #TODO: #23 Add return None if guild is not found.
            return guild_object
        except KeyError:
            return None

class FindModules():
    """A class dedicated to finding loaded Goldy Bot modules from cache."""
    def __init__(self):
        pass

    def find_object_by_module_name(self, module_name:str):
        """A fast way to grab the class object of a module from Goldy Bot cache."""
        GoldyBot.logging.log(f"[{MODULE_NAME}] Finding module '{module_name}' by name...")
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

class FindExtensions():
    """A class dedicated to finding loaded Goldy Bot extensions from cache."""
    def __init__(self):
        pass

    def find_object_by_extension_name(self, extension_name:str):
        """A fast way to grab the class object of a extension from Goldy Bot cache."""
        GoldyBot.logging.log(f"[{MODULE_NAME}] Finding extension '{extension_name}' by name...")
        for module in main_cache_dict["modules"]:
            try:
                extension_object:GoldyBot.ext.extensions.Extension = main_cache_dict["modules"][f"{module}"]["extensions"][f"{extension_name}"]["object"]
                GoldyBot.logging.log(f"[{MODULE_NAME}] Found the extension '{extension_name}'!")
                return extension_object
            except KeyError:
                pass

        for module in main_cache_dict["internal_modules"]:
            try:
                extension_object:GoldyBot.ext.extensions.Extension = main_cache_dict["internal_modules"][f"{module}"]["extensions"][f"{extension_name}"]["object"]
                GoldyBot.logging.log(f"[{MODULE_NAME}] Found the extension '{extension_name}'!")
                return extension_object
            except KeyError:
                pass

        GoldyBot.logging.log("error", f"[{MODULE_NAME}] Failed to find the extension '{extension_name}'.")
        return None