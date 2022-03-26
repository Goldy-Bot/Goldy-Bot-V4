from nextcord.ext import commands
from nextcord import Interaction

import GoldyBot

MODULE_NAME = "COMMANDS"

def command(command_name:str=None, command_usage:str=None, help_des:str=None):
    """Add a command to Goldy Bot with this decorator."""

    def inner(func, command_name=None, command_usage=None, help_des=None):
        func:function = func
        
        goldy_command = GoldyBot.utility.goldy.command.Command(func)

        print(goldy_command.extenstion)

        if command_name == None: command_name = goldy_command.code_name

        if help_des == None: help_des = goldy_command.get_help_des()

        #  Add command to nextcord.
        #============================
        # Grab client object from cache.
        client:commands.Bot = GoldyBot.cache.main_cache_dict["client"]
        
        # Get command's arguments.
        params = goldy_command.params

        is_in_extenstion = goldy_command.in_extenstion
        class_ = goldy_command.extenstion

        if not params[0] == "ctx": # Check if command has 'ctx' as first argument.
            GoldyBot.logging.log("warn", f"Failed to load the command '{command_name}', it must contain 'ctx' as it's first argument!")
            return None

        # Add command.
        if is_in_extenstion == True:
            @client.command(name=command_name, help_message=help_des)
            async def command_(ctx=params[0], *params):
                await func(class_, ctx, *params)
        else:
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

        if is_in_extenstion == True:
            exec(f"""
@client.slash_command(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params}):
    ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
    await func(class_, ctx{slash_command_params})

        """, {"func":func, "client":client, "command_name":command_name, "help_des":help_des, 
        "Interaction": Interaction, "GoldyBot": GoldyBot, "class_":class_})

        else:
            exec(f"""
@client.slash_command(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params}):
    ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
    await func(ctx{slash_command_params})

        """, {"func":func, "client":client, "command_name":command_name, "help_des":help_des, 
        "Interaction": Interaction, "GoldyBot": GoldyBot})

        GoldyBot.logging.log(f"[{MODULE_NAME}] The Command '{command_name}' has been loaded.")

    return inner