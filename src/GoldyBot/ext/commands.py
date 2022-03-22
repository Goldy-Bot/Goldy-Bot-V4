from nextcord.ext import commands
from nextcord import Interaction

import GoldyBot

MODULE_NAME = "COMMANDS"

def command(func, command_name:str=None, command_usage:str=None, help_des:str=None):
    """Add a command to Goldy Bot with this decorator."""
    func:function = func

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

    else: 
        # Add command.
        @client.command(name=command_name, help_message=help_des)
        async def command_(ctx=params[0], *params):
            await func(ctx, *params)

        # Add slash command
        params_amount = len(params[1:])
        slash_command_params = ""
        if params_amount >= 1:
            slash_command_params = ", "
            count = 0
            for param in params[1:]:
                count += 1
                if count >= params_amount:
                    slash_command_params += f"{param}"
                else:
                    slash_command_params += f"{param}, "

        exec(f"""
        
@client.slash_command(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params}):
    ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
    await func(ctx{slash_command_params})

""", {"func":func, "client":client, "command_name":command_name, "help_des":help_des, "Interaction": Interaction, "GoldyBot": GoldyBot})

        GoldyBot.logging.log(f"[{MODULE_NAME}] The Command '{command_name}' has been loaded.")