import GoldyBot
from GoldyBot.logging import print_and_log

import time

class GoldyBotError(Exception):
    """The parent/master class of all the errors in Goldy Bot."""
    def __init__(self, error, no_traceback:bool=False):
        """Raise me! UwU OwO"""
        super().__init__(error)
        GoldyBot.logging.log("error", error, no_traceback)

# Commands
#-------------
class GuildNotRegistered(GoldyBotError):
    """Raised when a member executes a command from a guild that has not been registered."""
    pass

class CommandNotAllowedInGuild(GoldyBotError):
    """Raised when a command that isn't allowed in that guild executes."""
    pass

class MemberHasNoPermsForCommand(GoldyBotError):
    """Raised when a member without the proper roles tries to execute a command."""
    pass

# Roles
#-----------
class FailedToFindRole(GoldyBotError):
    """This exception is raised by ``GoldyBot.objects.Role`` when a role can't be found."""
    def __init__(self, option_used=None, option_value=None):
        error = "Failed to find role!"
        if not option_used == None:
            error = f"Failed to find role by the {option_used} '{option_value}'."

        super().__init__(error)

# Modules
#------------
class ModuleFailedToLoad(GoldyBotError):
    def __init__(self, error):
        super().__init__(error)

class ModuleNotFound(GoldyBotError):
    def __init__(self, error):
        super().__init__(error)

# Guilds
#---------

# Guild Config
class FailedToFindGuildRole(GoldyBotError):
    """Raised when a guild role can't be found by ``GoldyBot.objects.Role``."""
    def __init__(self, error):
        super().__init__(error, no_traceback=True)



# Config
#---------

# Config Incorrect
class ConfigIsIncorrect(GoldyBotError):
    def __init__(self, error, what_is_incorrect:str=None):
        """Error that is raised whenever a configuration file is incorrect or missing something."""
        super().__init__(error)
        print_and_log("info", "^ This usually means you misspelt something in the config or the layout of the config is incorrect. ^")

        if not what_is_incorrect == None:
            print_and_log("warn", f"We actually think you might of misspelt '{what_is_incorrect}'.")