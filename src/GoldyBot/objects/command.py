import importlib
import GoldyBot

MODULE_NAME = "COMMAND"

class Command():
    def __init__(self, func):
        """Generates goldy bot command object with command function object."""
        self.func:function = func

        self.command_name = self.func.__name__
        self.params_ = list(self.func.__code__.co_varnames)
        
        self.in_extenstion_ = False

        if self.params[0] == "self":
            self.in_extenstion_ = True
            self.params_.pop(0)

    @property
    def code_name(self) -> str:
        """Returns code name of comamnd."""
        return self.command_name

    @property
    def params(self) -> list:
        """Returns list of function parameters."""
        return self.params_

    @property
    def extension_name(self) -> str:
        """Returns extension's code name."""
        if self.in_extenstion:
            # Command is in extenstion.
            return str(self.func).split(" ")[1].split(".")[0]
        else:
            # Command is not in any extenstion.
            return None

    @property
    def extenstion(self) -> GoldyBot.ext.extenstions.Extenstion:
        """Finds and returns the object of the command's extenstion."""
        if self.in_extenstion:
            return GoldyBot.cache.main_cache_dict["extenstions"][f"{self.extension_name}"] #TODO: Get extenstion object from cache.
        else:
            return None

    @property
    def in_extenstion(self) -> bool:
        """Returns true/false if the command is in a extenstion."""
        if self.in_extenstion_:
            return True
        else:
            return False

    def get_help_des(self) -> str:
        """Returns the command's help description."""
        try:
            return (importlib.import_module(f'.{self.command_name}', package="GoldyBot.utility.msgs")).help_des

        except ImportError:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not have a 'msg' module, so the help command will not display a help description for it.")
            return "None"

        except AttributeError:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not contain 'help_des' variable in it's 'msg' module, so the help command will not display a help description.")
            return "None"