import importlib
import GoldyBot

MODULE_NAME = "COMMAND"

class Command():
    def __init__(self, command_name:str):
        self.command_name = command_name

    def get_help_des(self) -> str:
        """Returns the command's help description."""
        try:
            return (importlib.import_module(f'.{self.command_name}', package="GoldyBot.utility.msgs")).help_des

        except ImportError:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not have a 'msg' module, so the help command will not display a help description for it.")
            return None

        except AttributeError:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not contain 'help_des' variable in it's 'msg' module, so the help command will not display a help description.")
            return None