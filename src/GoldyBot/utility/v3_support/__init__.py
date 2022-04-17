"""
Importing this module in a v3 extenstion/cog adds v4 support.
"""

#  V3 backwards compatibility.
import GoldyBot

#  Overwrite commonly varibles
commands = GoldyBot
# Add 'commands' attributes.
setattr(commands, 'Cog', GoldyBot.Extenstion)

#  Overwrite fnuctions.
print_and_log = GoldyBot.logging.log

# Fake 'can_the_command_run()' function.
def can_the_command_run(ctx=None, cog_name=None):
    """FAKED for V4 support, don't use this in V4!"""
    return True # Always return true because 'can_the_command_run' is now checked in '@GoldyBot.command' for V4.

#  Overwrite Modules
msg = GoldyBot.utility.msgs
#TODO: Add the settings module with all it's v3 attributes.