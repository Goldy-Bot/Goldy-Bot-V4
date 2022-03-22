from nextcord.ext import commands
from nextcord import Interaction

import GoldyBot

MODULE_NAME = "COMMANDS"

def command(func, command_name:str=None, command_usage:str=None, help_des:str=None):
    """Add a command to Goldy Bot with this decorator."""

    if command_name == None: command_name = func.__name__

    goldy_command = GoldyBot.utility.goldy.command.Command(command_name)

    if help_des == None: help_des = goldy_command.get_help_des()

    #  Add command to nextcord.
    #============================
    # Grab client object from cache.
    client:commands.Bot = GoldyBot.cache.main_cache_dict["client"]
    
    # Get command's arguments.
    params = list(func.__code__.co_varnames)

    if not params[0] == "ctx": # Check if command has 'ctx' as first argument.
        GoldyBot.logging.log("warn", f"Failed to load the command '{command_name}', it must contain 'ctx' as it's first argument!")

    else: # Add command.
        @client.command(name=command_name, help_message=help_des)
        async def command_(ctx=params[0], *params):
            await func(ctx, *params)

        # Add slash command

        """
        if len(params) >= 2:
            @client.slash_command(name=command_name, description=help_des, guild_ids=[863416692083916820])
            async def slash_command_(interaction:Interaction, params=None):
                params_list = params.split()
                ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
                await func(ctx, *params_list)
        else:
            @client.slash_command(name=command_name, description=help_des, guild_ids=[863416692083916820])
            async def slash_command_(interaction:Interaction):
                ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
                await func(ctx)
        """

        #TODO: MAKE SEPERATE COMMAND HANDLER FOR SLASH COMMANDS.

        GoldyBot.logging.log(f"[{MODULE_NAME}] The Command '{command_name}' has been loaded.")