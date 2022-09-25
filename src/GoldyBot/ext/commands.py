from __future__ import annotations
import asyncio
from typing import Dict
import nextcord
from nextcord.ext import commands

import GoldyBot
from GoldyBot.errors import GuildNotRegistered, MemberHasNoPermsForCommand

MODULE_NAME = "COMMANDS"

def command(command_name:str=None, required_roles:list=[], help_des:str=None, hidden=False, slash_cmd_only=False, normal_cmd_only=False, slash_options:Dict[str, nextcord.SlashOption]={}):
    """
    Add a command to Goldy Bot with this decorator.
    
    ---------------
    ### ***``Example:``***

    This is how you create a command in GoldyBot. 😀

    ```python
    @GoldyBot.command()
    async def uwu(ctx):
        await ctx.send(f'Hi, {ctx.author.mention}! UwU!')
    ```
    """
    def decorate(func):
        def inner(func, command_name, required_roles, help_des, hidden, slash_cmd_only, normal_cmd_only, slash_options) -> GoldyBot.objects.command.Command:
            func:function = func
            
            goldy_command = GoldyBot.objects.command.Command(func, command_name=command_name, required_roles=required_roles, slash_options=slash_options, help_des=help_des, hidden=hidden)
            print(goldy_command.params)

            if command_name == None: command_name = goldy_command.code_name

            toggle_slash_cmd = True
            toggle_normal_cmd = True

            if slash_cmd_only == True: toggle_normal_cmd = False
            if normal_cmd_only == True: toggle_slash_cmd = False

            #  Add command to nextcord.
            #============================
            # Grab client object from cache.
            client:commands.Bot = GoldyBot.cache.main_cache_dict["client"]
            
            # Get command's arguments.
            params = goldy_command.params

            # Create command usage embed.
            command_usage_args = f"!{command_name}"
            for param in params[1:]:
                command_usage_args += (" {" + param + "}")

            command_usage_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandUsage.Embed.title)
            command_usage_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandUsage.Embed.thumbnail)

            no_perms_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.title)
            no_perms_embed.color = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.colour
            no_perms_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.thumbnail)

            guild_not_registered_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.title)
            guild_not_registered_embed.color = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.colour
            guild_not_registered_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.thumbnail)

            # Preparing to add command.
            # Checking if this command is in an extension.
            is_in_extension = goldy_command.in_extension
            class_ = goldy_command.extension

            if not params[0] == "ctx": # Check if command has 'ctx' as first argument.
                GoldyBot.logging.log("warn", f"Failed to load the command '{command_name}', it must contain 'ctx' as it's first argument!")
                return None

            # Add command.
            #----------------
            if toggle_normal_cmd:
                GoldyBot.logging.log(f"[{MODULE_NAME}] [{command_name.upper()}] Creating normal command...")
                if is_in_extension == True: # Run in EXTENSION!
                    @client.command(name=command_name, help_message=help_des)
                    async def command_(ctx=params[0], *params):
                        command_usage_embed.description = GoldyBot.utility.msgs.bot.CommandUsage.Embed.des.format(ctx.author.mention, command_usage_args)

                        #Run command.
                        try:
                            if goldy_command.allowed_to_run(ctx):
                                await func(class_, ctx, *params)
                                GoldyBot.logging.log(f"[{MODULE_NAME}] The command '{goldy_command.code_name}' was executed.")
                        except TypeError as e: 
                            if not goldy_command.any_args_missing(params): # Command Arguments are missing.
                                message = await ctx.send(embed=command_usage_embed)
                                await asyncio.sleep(15)
                                await message.delete()                    

                            else: # Then it's an actual error.
                                GoldyBot.logging.log("error", e)

                        except MemberHasNoPermsForCommand:
                            if hidden == False:
                                no_perms_embed.description = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.des.format(ctx.author.mention)
                                message = await ctx.send(embed=no_perms_embed)
                                await asyncio.sleep(15)
                                await message.delete()

                        except GuildNotRegistered:
                            if hidden == False:
                                guild_not_registered_embed.description = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.des.format(ctx.author.mention)
                                message = await ctx.send(embed=guild_not_registered_embed)
                                await asyncio.sleep(15)
                                await message.delete()
                                
                        except Exception as e:
                            GoldyBot.logging.log("error", e)

                else: # Run as NORMAL command!
                    @client.command(name=command_name, help_message=help_des)
                    async def command_(ctx=params[0], *params):
                        command_usage_embed.description = GoldyBot.utility.msgs.bot.CommandUsage.Embed.des.format(ctx.author.mention, command_usage_args)

                        # Run command.
                        try: 
                            if goldy_command.allowed_to_run(ctx):
                                await func(ctx, *params)
                                GoldyBot.logging.log(f"[{MODULE_NAME}] The command '{goldy_command.code_name}' was executed.")
                        except TypeError as e:

                            if not goldy_command.any_args_missing(params): # Command Arguments are missing.
                                message = await ctx.send(embed=command_usage_embed)
                                await asyncio.sleep(15)
                                await message.delete()

                            else: # Then it's an actual error.
                                GoldyBot.logging.log("error", e)

                        except MemberHasNoPermsForCommand:
                            if hidden == False:
                                message = await ctx.send(embed=no_perms_embed)
                                await asyncio.sleep(6)
                                await message.delete()

                        except GuildNotRegistered:
                            if hidden == False:
                                message = await ctx.send(embed=guild_not_registered_embed)
                                await asyncio.sleep(15)
                                await message.delete()

                        except Exception as e:
                            GoldyBot.logging.log("error", e)
                GoldyBot.logging.log(f"[{MODULE_NAME}] [{command_name.upper()}] Normal command created!")

            # Add slash command
            #--------------------
            if toggle_slash_cmd:
                GoldyBot.logging.log(f"[{MODULE_NAME}] [{command_name.upper()}] Creating slash command...")
                goldy_command.create_slash()
            GoldyBot.logging.log("info_3", f"[{MODULE_NAME}] Command '{command_name}' has been loaded.")

            return goldy_command

        return inner(func, command_name, required_roles, help_des, hidden, slash_cmd_only, normal_cmd_only, slash_options)

    return decorate