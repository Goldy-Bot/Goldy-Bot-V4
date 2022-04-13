import os
import GoldyBot
import importlib.util

MODULE_NAME = "MODULES"

class Module(object):
    """Goldy Bot class to easily interface with modules."""
    def __init__(self, path_to_module:str=None, module_file_name:str=None):
        self.path_to_module = path_to_module
        self.module_file_name = module_file_name

        self.ignored_modules_list = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON)).read("ignored_modules")

        if self.path_to_module == None:
            if self.module_file_name == None:
                GoldyBot.logging.log("error", "Module() must have either arguments 'path_to_module' or 'module_file_name' passed in.")
            else:
                # Find where module is located.
                #----------------------------------
                if self.module_file_name in os.listdir(GoldyBot.paths.INTERNAL_COGS_V4):
                    self.path_to_module = f"{GoldyBot.paths.INTERNAL_COGS_V4}/{self.module_file_name}"

                if self.module_file_name in os.listdir(GoldyBot.paths.MODULES):
                    self.path_to_module = f"{GoldyBot.paths.MODULES}/{self.module_file_name}"

                if not self.path_to_module == None:
                    GoldyBot.logging.log(f"[{MODULE_NAME}] The module '{self.module_file_name}' was found in '{self.path_to_module}'.")
                else:
                    GoldyBot.logging.log("warn", f"[{MODULE_NAME}] The module '{self.module_file_name}' was not found!")
        
        else:
            # Assume 'path_to_module' was used.
            self.module_file_name = path_to_module.split("/")[-1]


        # Checks if it's a single module or a package module. (More Info Here: )
        #-------------------------------------------------------------------------
        #TODO: Add support for loading folder modules with "__init__.py".


    def load(self):
        """Commands Goldy Bot to load this module."""
        
        if not self.module_file_name[:-3] in self.ignored_modules_list:
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

                GoldyBot.logging.log(f"💚 [{MODULE_NAME}] Loaded the internal module '{self.module_file_name}'!")
            except AttributeError:
                GoldyBot.logging.log("error", f"❤️ [{MODULE_NAME}] The internal module '{self.module_file_name[:-3]}' failed to load because it did not contain the 'load()' function.")

        else:
            GoldyBot.logging.log("info", f"💙 [{MODULE_NAME}] The internal module '{self.module_file_name[:-3]}' is not being loaded as it was ignored.")