import GoldyBot

class GoldyBotError(Exception):
    """The parent/master class of all the errors in Goldy Bot."""
    def __init__(self, error):
        GoldyBot.logging.log("error", error)
        super().__init__(error)

# Commands
#-------------
class GuildNotRegistered(GoldyBotError):
    """Raised when a member executes a command from a guild that has not been registered."""
    pass

class CommandNotAllowedInGuild(GoldyBotError):
    """Raised when a command that isn't allowed in that guild executes."""
    pass

class MemberHasNoPermsForCommand(GoldyBotError):
    """Raised when a member without the proper roles trys to execute a command."""
    pass

# Roles
#-----------
class FailedToFindRole(GoldyBotError):
    def __init__(self, option_used=None, option_value=None):
        if not option_used == None:
            if not option_value == None:
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

# Guild Config
class FailedToFindGuildRole(GoldyBotError):
    def __init__(self, error):
        super().__init__(error)