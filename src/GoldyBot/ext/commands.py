import nextcord
from nextcord.ext import commands
from nextcord import Interaction

import GoldyBot

MODULE_NAME = "COMMANDS"

def command(command_name:str=None, command_usage:str=None, help_des:str=None):
    """Add a command to Goldy Bot with this decorator."""

    def inner(func, command_name=None, command_usage=None, help_des=None):
        func:function = func
        
        goldy_command = GoldyBot.objects.command.Command(func)

        if command_name == None: command_name = goldy_command.code_name

        if help_des == None: help_des = goldy_command.get_help_des()

        #  Add command to nextcord.
        #============================
        # Grab client object from cache.
        client:commands.Bot = GoldyBot.cache.main_cache_dict["client"]
        
        # Get command's arguments.
        params = goldy_command.params

        # Create command usage embed.
        command_usage_args = f"!{command_name} "
        for param in params[1:]:
            command_usage_args += ("{" + param + "} ")

        command_usage_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandUsage.Embed.title, colour=GoldyBot.utility.goldy.colours.AKI_ORANGE)
        command_usage_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandUsage.Embed.thumbnail)

        # Preparing to add command.
        is_in_extenstion = goldy_command.in_extenstion
        class_ = goldy_command.extenstion

        if not params[0] == "ctx": # Check if command has 'ctx' as first argument.
            GoldyBot.logging.log("warn", f"Failed to load the command '{command_name}', it must contain 'ctx' as it's first argument!")
            return None

        # Add command.
        if is_in_extenstion == True: # Run in EXTENSTION!
            @client.command(name=command_name, help_message=help_des)
            async def command_(ctx=params[0], *params):
                command_usage_embed.description = GoldyBot.utility.msgs.bot.CommandUsage.Embed.des.format(ctx.author.mention, command_usage_args)

                #Run command.
                try:
                    await func(class_, ctx, *params)
                    GoldyBot.logging.log(f"[{MODULE_NAME}] The command '{goldy_command.code_name}' was executed.")
                except TypeError as e: # Arguments missing.
                    #TODO: #11 Goldy Bot thinks arguments are missing whenever a type error occurs within a command.
                    GoldyBot.logging.log("error", e)
                    await ctx.send(embed=command_usage_embed)
                except Exception as e:
                    GoldyBot.logging.log("error", e)
        else: # Run as NORMAL command!
            @client.command(name=command_name, help_message=help_des)
            async def command_(ctx=params[0], *params):
                command_usage_embed.description = GoldyBot.utility.msgs.bot.CommandUsage.Embed.des.format(ctx.author.mention, command_usage_args)

                # Run command.
                try: 
                    await func(ctx, *params)
                    GoldyBot.logging.log(f"[{MODULE_NAME}] The command '{goldy_command.code_name}' was executed.")
                except TypeError: # Arguments missing.
                    await ctx.send(embed=command_usage_embed)
                except Exception as e:
                    GoldyBot.logging.log("error", e)

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

        if is_in_extenstion == True: # Run in EXTENSTION!
            exec(f"""
@client.slash_command(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params}):
    ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
    try:
        await func(class_, ctx{slash_command_params})
        GoldyBot.logging.log(f"[{MODULE_NAME}] The command '{goldy_command.code_name}' was executed.")
    except Exception as e:
        GoldyBot.logging.log("error", e)

            """, {"func":func, "client":client, "command_name":command_name, "help_des":help_des, 
            "Interaction": Interaction, "GoldyBot": GoldyBot, "class_":class_})
            
        else: # Run as NORMAL command!
            exec(f"""
@client.slash_command(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params}):
    ctx = GoldyBot.utility.goldy.slash.InteractionToCtx(interaction)
    try:
        await func(ctx{slash_command_params})
        GoldyBot.logging.log(f"[{MODULE_NAME}] The command '{goldy_command.code_name}' was executed.")
    except Exception as e:
        GoldyBot.logging.log("error", e)

            """, {"func":func, "client":client, "command_name":command_name, "help_des":help_des, 
            "Interaction": Interaction, "GoldyBot": GoldyBot})

        GoldyBot.logging.log(f"🤍 [{MODULE_NAME}] The command '{command_name}' has been loaded.")

    return inner