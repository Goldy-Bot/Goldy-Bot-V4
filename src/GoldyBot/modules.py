from __future__ import annotations

import os
import sys
from typing import List
import importlib.util

import GoldyBot
from GoldyBot.errors import ModuleFailedToLoad, ModuleNotFound

MODULE_NAME = "MODULES"

sys.path.insert(1, GoldyBot.paths.MODULES)
sys.path.append(GoldyBot.paths.INTERNAL_MODULES_V4)

class Module(object):
    """Goldy Bot class to easily interface with modules."""
    def __init__(self, path_to_module:str=None, module_file_name:str=None):
        self.path_to_module = path_to_module
        self.module_file_name = module_file_name

        self.version_ = None
        self.author_ = None
        self.author_github_ = None
        self.open_source_link_ = None

        self.is_internal_module_ = False
        self.is_external_module_ = False
        self.is_package_module_ = False

        self.ignored_modules_list = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON)).read("ignored_modules")

        if self.path_to_module == None:
            if self.module_file_name == None:
                GoldyBot.logging.log("error", "Module() must have either arguments 'path_to_module' or 'module_file_name' passed in.")
            else:
                # Find where module is located.
                #----------------------------------
                if self.module_file_name in os.listdir(GoldyBot.paths.INTERNAL_COGS_V4):
                    self.path_to_module = f"{GoldyBot.paths.INTERNAL_COGS_V4}/{self.module_file_name}"
                    self.is_internal_module_ = True

                if self.module_file_name in os.listdir(GoldyBot.paths.MODULES):
                    self.path_to_module = f"{GoldyBot.paths.MODULES}/{self.module_file_name}"
                    self.is_external_module_ = True

                if not self.path_to_module == None:
                    GoldyBot.logging.log(f"[{MODULE_NAME}] The module '{self.module_file_name}' was found in '{self.path_to_module}'.")
                    
                    if os.path.isdir(self.path_to_module): # Checks if the module is a package module.
                        GoldyBot.logging.log("info", f"[{MODULE_NAME}] The module '{self.module_file_name}' was dectected as a package module.")
                        self.is_package_module_ = True

                else:
                    #GoldyBot.logging.log("warn", f"[{MODULE_NAME}] The module '{self.module_file_name}' was not found!")
                    raise ModuleNotFound(f"[{MODULE_NAME}] The module '{self.module_file_name}' was not found!")
        else:
            # Assume 'path_to_module' was used.
            self.module_file_name = path_to_module.split("/")[-1]

        # Cache module.
        #----------------
        if self.is_external_module_:
            if not self.name in GoldyBot.cache.main_cache_dict["modules"]:
                GoldyBot.cache.main_cache_dict["modules"][f"{self.name}"] = {}
                GoldyBot.cache.main_cache_dict["modules"][f"{self.name}"]["extensions"] = {}
                GoldyBot.cache.main_cache_dict["modules"][f"{self.name}"]["object"] = self
        else:
            if not self.name in GoldyBot.cache.main_cache_dict["internal_modules"]:
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.name}"] = {}
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.name}"]["extensions"] = {}
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.name}"]["object"] = self


    def load(self):
        """Commands Goldy Bot to load this module."""
        
        if not self.module_file_name[:-3] in self.ignored_modules_list:
            if self.is_package_module_:
                # Specify Package Module
                sys.path.append(self.path_to_module)

                spec_module = importlib.util.spec_from_file_location(self.module_file_name, self.path_to_module + "/__init__.py")
            else:
                # Specify Module
                spec_module = importlib.util.spec_from_file_location(self.module_file_name[:-3], self.path_to_module)

            # Get Module
            module_py = importlib.util.module_from_spec(spec_module)
            
            # Run Module
            spec_module.loader.exec_module(module_py)

            # Get load function from module.
            try:
                load_function = getattr(module_py, "load")
                load_function()

                GoldyBot.logging.log("info_4", f"[{MODULE_NAME}] Loaded the internal module '{self.module_file_name}'!")
            except AttributeError:
                raise ModuleFailedToLoad(f"[{MODULE_NAME}] The internal module '{self.name}' failed to load because it did not contain the 'load()' function.")

            # Find information variables in module.
            try: self.version_ = getattr(module_py, "VERSION")
            except AttributeError: self.version_ = None

            try: self.author_ = getattr(module_py, "AUTHOR")
            except AttributeError: self.author_ = None

            try: self.author_github_ = getattr(module_py, "AUTHOR_GITHUB")
            except AttributeError: self.author_github_ = None

            try: self.open_source_link_ = getattr(module_py, "OPEN_SOURCE_LINK")
            except AttributeError: self.open_source_link_ = None

        else:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The internal module '{self.name}' is not being loaded as it was ignored.")

    def reload(self) -> List[GoldyBot.objects.command.Command]:
        """Commands Goldy Bot to reload this module."""

        # Unload the module.
        #--------------------------
        self.unload()

        # Load the module again.
        #--------------------------
        GoldyBot.logging.log(f"[{MODULE_NAME}] Reloading module...")
        self.load()

        return self.commands

    def unload(self):
        """Commands Goldy Bot to unload this module with it's commands."""

        # Remove all commands in module.
        #---------------------------------
        GoldyBot.logging.log(f"[{MODULE_NAME}] Getting all module's commands...")
        commands_list = self.commands

        for command in commands_list:
            command.remove()
        
        GoldyBot.logging.log(f"[{MODULE_NAME}] Removed all commands!")

        GoldyBot.logging.log("info_5", f"[{MODULE_NAME}] Unloaded the module '{self.module_file_name}'!")

    @property
    def name(self):
        """Returns the name of the module."""
        if self.is_package_module_:
            return self.module_file_name
        else:
            return self.module_file_name[:-3]

    @property
    def version(self) -> float|None:
        """Returns the current version of the module if stated."""
        return self.version_

    @property
    def author(self) -> str|None:
        """Returns the name of the developer who created this module if stated. """
        return self.author_

    @property
    def author_github(self) -> str|None:
        """Returns a link to the authors github page if stated."""
        return self.author_github_

    @property
    def open_source_link(self) -> str|None:
        """Returns link to github repository for this module."""
        return self.open_source_link_

    github_repo = open_source_link
    """Alias of ``open_source_link``"""

    @property
    def commands(self):
        """List of commands in the module."""
        if self.is_internal_module: modules_list_name = "internal_modules"
        else: modules_list_name = "modules"

        commands:List[GoldyBot.objects.command.Command] = []

        # Finding all commands in this.
        #-----------------------
        GoldyBot.logging.log(f"[{MODULE_NAME}] Finding all commands in the module '{self.name}'...")
        for extension in GoldyBot.cache.main_cache_dict[modules_list_name][self.name]["extensions"]:
            for command in GoldyBot.cache.main_cache_dict[modules_list_name][self.name]["extensions"][extension]["commands"]:
                command:GoldyBot.objects.command.Command

                commands.append(command)

        return commands

    @property
    def is_internal_module(self):
        """Commands Goldy Bot to check whether this module is an internal module or an external one."""
        if self.is_internal_module_:
            return True
        else:
            return False