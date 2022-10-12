from __future__ import annotations
import asyncio
import importlib
from typing import Dict, List
import nextcord
from nextcord.ext import commands

import GoldyBot

MODULE_NAME = "COMMAND"

MISSING = nextcord.utils.MISSING

# Embeds
#---------
class Embeds():
    def __init__(self):
        self.command_usage_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandUsage.Embed.title)
        self.command_usage_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandUsage.Embed.thumbnail)

        self.no_perms_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.title)
        self.no_perms_embed.color = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.colour
        self.no_perms_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.thumbnail)

        self.guild_not_registered_embed = GoldyBot.utility.goldy.embed.Embed(title=GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.title)
        self.guild_not_registered_embed.color = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.colour
        self.guild_not_registered_embed.set_thumbnail(url=GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.thumbnail)

class Command(Embeds):
    def __init__(self, func, command_object:nextcord.BaseApplicationCommand | commands.Command=None, command_name=None, 
        required_roles:list=[], slash_options:dict={}, help_des:str=None, hidden:bool=False, 
        parent_cmd:Command=None
    ):
        """Generates goldy bot command object with command function object."""
        self.func:function = func
        self.command = command_object
        """Nextcord command object."""

        if command_name == None:
            self.command_name = self.func.__name__
        else:
            self.command_name = command_name
        self.required_roles_ = required_roles
        self.slash_options_ = slash_options
        self.params_ = list(self.func.__code__.co_varnames)
        self.params_amount_ = self.func.__code__.co_argcount
        self.help_des_ = help_des
        self.is_hidden_ = hidden

        self.parent_cmd_ = parent_cmd
        
        self.in_extension_ = False

        if self.params[0] == "self":
            self.in_extension_ = True
            self.params_.pop(0)

        # Add command to extension in cache.
        if self.in_extension:
            if self.module.is_internal_module:
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extensions"][f"{self.extension_name}"]["commands"].append(self)
            else:
                GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extensions"][f"{self.extension_name}"]["commands"].append(self)
        else:
            GoldyBot.cache.main_cache_dict["internal_modules"]["goldy"]["extensions"]["core"]["commands"].append(self)

        super().__init__()

    @property
    def code_name(self) -> str:
        """Returns code name of command."""
        return self.command_name

    @property
    def params(self) -> list:
        """Returns list of function parameters."""
        if self.in_extension:
            return self.params_[0:self.params_amount_ - 1]
        else:
            return self.params_[0:self.params_amount_]

    @property
    def extension_name(self) -> str | None:
        """Returns extension's code name."""
        if self.in_extension:
            # Command is in extension.
            return str(self.func).split(" ")[1].split(".")[0]
        else:
            # Command is not in any extension.
            return None

    @property
    def extension(self) -> GoldyBot.ext.extensions.Extension | None:
        """Finds and returns the object of the command's extension."""
        if self.in_extension:
            return GoldyBot.cache.FindExtensions().find_object_by_extension_name(extension_name=self.extension_name)
        else:
            None

    @property
    def in_extension(self) -> bool:
        """Returns true/false if the command is in a extension."""
        if self.in_extension_:
            return True
        else:
            return False

    @property
    def module_name(self) -> str:
        """Returns name of module the command is located in."""
        return self.extension.module_name

    @property
    def module(self) -> GoldyBot.modules.Module:
        return GoldyBot.cache.FindModules().find_object_by_module_name(module_name=self.module_name)

    @property
    def is_hidden(self):
        """Is the command hidden."""
        return self.is_hidden_

    @property
    def parent_cmd(self) -> Command|None:
        """Returns the command object of the parent command if command has parent."""
        return self.parent_cmd_

    @property
    def is_child(self):
        """Returns if command is child or not."""
        if self.parent_cmd == None:
            return False
        else:
            return True

    def mention(self) -> str:
        """Returns mention of slash command, if registered as a slash command."""
        #TODO: Perhaps have this return codeblock if this command is not a slash command.
        try:
            if self.is_child == False:
                return f"</{self.code_name}:{self.command.command_ids[0]}>"
            else:
                return f"</{self.parent_cmd.code_name} {self.code_name}:{self.command.command_ids[0]}>"
        except (TypeError, AttributeError):
            GoldyBot.log("warn", f"[{MODULE_NAME}] Tried to mention slash command '{self.code_name}' but could not find it's command id so I'm returning the mention without it.")
            
            if self.is_child == False: return f"</{self.code_name}:0>"
            else: return f"</{self.parent_cmd.code_name} {self.code_name}:0>"

    def create_slash(self) -> nextcord.BaseApplicationCommand:
        """Creates slash command."""

        GoldyBot.logging.log(f"[{MODULE_NAME}] [{self.command_name.upper()}] Creating slash command...")
        slash_command_params = self.slash_commands_params_generator()

        return_data = {}

        #  Make slash command only visible to admins if it is hidden.
        default_member_permissions = None
        if self.is_hidden: default_member_permissions = nextcord.Permissions(permissions=8)
        

        if self.in_extension == True: # Run in EXTENSION!
            exec(f"""
@client.slash_command(name=command_name, description=help_des, guild_ids=guilds_allowed_in, default_member_permissions=default_member_permissions)
async def slash_command_(interaction: Interaction{slash_command_params[0]}):
    ctx = GoldyBot.objects.slash.InteractionToCtx(interaction)
    try:
        if self.allowed_to_run(ctx):
            await func(class_, ctx{slash_command_params[1]})
            GoldyBot.logging.log(f"[{MODULE_NAME}] The slash command '{self.code_name}' was executed.")

    except GoldyBot.errors.MemberHasNoPermsForCommand:
        if hidden == False:
            no_perms_embed.description = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=no_perms_embed)
            await asyncio.sleep(6)
            await message.delete()

    except GoldyBot.errors.GuildNotRegistered:
        if hidden == False:
            guild_not_registered_embed.description = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=guild_not_registered_embed)
            await asyncio.sleep(15)
            message.delete()

    except Exception as e:
        GoldyBot.logging.log("error", e)
            """, 
            
            {"func":self.func, "client":GoldyBot.cache.main_cache_dict["client"], "command_name":self.command_name, "help_des":self.get_help_des(), "self":self,
            "Interaction": GoldyBot.nextcord.Interaction, "GoldyBot": GoldyBot, "asyncio":asyncio, "nextcord":nextcord, "class_":self.extension, "no_perms_embed":self.no_perms_embed, 
            "guild_not_registered_embed":self.guild_not_registered_embed, "hidden":self.is_hidden, "guilds_allowed_in":self.guilds_allowed_in, 
            "default_member_permissions":default_member_permissions}, return_data)
            
        else: # Run as NORMAL command!
            exec(f"""
@client.slash_command(name=command_name, description=help_des, guild_ids=guilds_allowed_in, default_member_permissions=default_member_permissions)
async def slash_command_(interaction: Interaction{slash_command_params[0]}):
    ctx = GoldyBot.objects.slash.InteractionToCtx(interaction)
    try:
        if self.allowed_to_run(ctx):
            await func(ctx{slash_command_params[1]})
            GoldyBot.logging.log(f"[{MODULE_NAME}] The slash command '{self.code_name}' was executed.")

    except GoldyBot.errors.MemberHasNoPermsForCommand:
        if hidden == False:
            no_perms_embed.description = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=no_perms_embed)
            await asyncio.sleep(15)
            await message.delete()

    except GoldyBot.errors.GuildNotRegistered:
        if hidden == False:
            guild_not_registered_embed.description = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=guild_not_registered_embed)
            await asyncio.sleep(15)
            await message.delete()

    except Exception as e:
        GoldyBot.logging.log("error", e)
            """, 
            
            {"func":self.func, "client":GoldyBot.cache.main_cache_dict["client"], "command_name":self.command_name, "help_des":self.get_help_des(), "self":self,
            "Interaction": GoldyBot.nextcord.Interaction, "GoldyBot": GoldyBot, "asyncio":asyncio, "nextcord":nextcord, "no_perms_embed":self.no_perms_embed, 
            "guild_not_registered_embed":self.guild_not_registered_embed, "hidden":self.is_hidden, "guilds_allowed_in":self.guilds_allowed_in, 
            "default_member_permissions":default_member_permissions}, return_data)

        GoldyBot.logging.log(f"[{MODULE_NAME}] [{self.command_name.upper()}] Slash command created!")

        self.command = return_data["slash_command_"]
        return return_data["slash_command_"]

    def remove(self):
        """Removes command from nextcord."""
        command_application_object = self.command

        # Remove command from extension in cache.
        if self.in_extension:
            if self.module.is_internal_module:
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extensions"][f"{self.extension_name}"]["commands"].remove(self)
            else:
                GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extensions"][f"{self.extension_name}"]["commands"].remove(self)
        else:
            GoldyBot.cache.main_cache_dict["internal_modules"]["goldy"]["extensions"]["core"]["commands"].remove(self)

        # Remove from nextcord.
        client = GoldyBot.cache.client()
        client.remove_command(name=self.code_name)

        for guild_id in self.guilds_allowed_in:
            print(command_application_object.command_ids) #TODO: Problem here!
            GoldyBot.async_loop.run_until_complete(client.delete_application_commands(command_application_object, guild_id=guild_id))
            
            GoldyBot.cache.main_cache_dict["client"] = client

        GoldyBot.logging.log("info_5", f"[{MODULE_NAME}] Removed the command '{self.code_name}'!")
        return True

    def any_args_missing(self, command_executers_args:tuple) -> bool:
        """Checks if the args given by the command executer matches what parameters the command needs."""
        if len(command_executers_args) == len(self.params[1:]):
            return True
        else:
            return False

    def slash_commands_params_generator(self):
        """Generates a string of params for slash commands. This is more of an in-house thing."""
        params_amount = len(self.params[1:])
        slash_command_params = ""
        slash_command_args = ""

        if params_amount >= 1:
            slash_command_params = ", "
            slash_command_args = ", "
            count = 0
            for param in self.params[1:]:
                count += 1

                try:
                    # String
                    if isinstance(self.slash_options_[param.lower()], str):
                        default_value = f"='{self.slash_options_[param.lower()]}'"

                    # Slash Option
                    if isinstance(self.slash_options_[param.lower()], nextcord.SlashOption):
                        slash_option:nextcord.SlashOption = self.slash_options_[param.lower()]

                        if isinstance(slash_option.name, str):
                            name = f"'{slash_option.name}'"
                        else:
                            name = None

                        if isinstance(slash_option.description, str):
                            description = f"'{slash_option.description}'"
                        else:
                            description = None

                        if isinstance(slash_option.required, nextcord.utils._MissingSentinel):
                            required = None
                        else:
                            required = slash_option.required

                        if isinstance(slash_option.choices, nextcord.utils._MissingSentinel):
                            choices = None
                        else:
                            choices = slash_option.choices

                        """
                        if isinstance(slash_option.min_value, nextcord.utils._MissingSentinel):
                            min_value = None
                        else:
                            min_value = slash_option.min_value
                            
                        if isinstance(slash_option.max_value, nextcord.utils._MissingSentinel):
                            max_value = None
                        else:
                            max_value = slash_option.max_value
                        """

                        if isinstance(slash_option.autocomplete, nextcord.utils._MissingSentinel):
                            autocomplete = None
                        else:
                            autocomplete = slash_option.autocomplete

                        if isinstance(slash_option.default, str):
                            default = f"'{slash_option.default}'"
                        else:
                            default = None
                        
                        default_value = f"""=nextcord.SlashOption(name={name}, description={description}, required={required}, 
                        choices={choices}, autocomplete={autocomplete}, default={default}, verify={slash_option._verify})"""
                    
                    else:
                        default_value = f"={self.slash_options_[param.lower()]}"

                except KeyError:
                    default_value = ""

                if count >= params_amount:
                    slash_command_params += f"{param}{default_value}"
                    slash_command_args += f"{param}"
                else:
                    slash_command_params += f"{param}{default_value}, "
                    slash_command_args += f"{param}, "

        return (slash_command_params, slash_command_args)

    def update_command_object(self, command_object:commands.Command):
        """Adds/updates this command object to the class."""
        self.command = command_object

    def sub_command(self, command_name:str=None, required_roles:list=[], help_des:str=None, slash_options:Dict[str, nextcord.SlashOption]={}, also_run_parent_CMD:bool=True):
        """Create a lovely sub command from this slash command. 😀 (Only works with slash commands.)"""

        def decorate(func):
            def inner(func, command_name, required_roles, help_des, slash_options):
                parent_command = self.command

                return_data = {}

                goldy_sub_command = Command(func, command_name=command_name, required_roles=required_roles, slash_options=slash_options, help_des=help_des, parent_cmd=self)
                slash_command_params = goldy_sub_command.slash_commands_params_generator()
                parent_slash_command_params = self.slash_commands_params_generator()

                if self.in_extension == True: # Run in EXTENSION!
                    exec(f"""
@parent_command.subcommand(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params[0]}):
    ctx = GoldyBot.objects.slash.InteractionToCtx(interaction)
    try:
        if self.allowed_to_run(ctx):
            continue_onto_subcommand = None
            if also_run_parent_CMD == True: continue_onto_subcommand = await goldy_parent_command.func(class_, ctx{parent_slash_command_params[1]})
            if not continue_onto_subcommand == False:
                await func(class_, ctx{slash_command_params[1]})
                GoldyBot.logging.log(f"[{MODULE_NAME}] The slash subcommand '{goldy_sub_command.code_name}' was executed.")
            else:
                GoldyBot.logging.log(f"[{MODULE_NAME}] The slash subcommand '{goldy_sub_command.code_name}' never executed because parent command returned 'False'.")

    except GoldyBot.errors.MemberHasNoPermsForCommand:
        if hidden == False:
            no_perms_embed.description = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=no_perms_embed)
            await asyncio.sleep(6)
            await message.delete()

    except GoldyBot.errors.GuildNotRegistered:
        if hidden == False:
            guild_not_registered_embed.description = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=guild_not_registered_embed)
            await asyncio.sleep(15)
            message.delete()

    except Exception as e:
        GoldyBot.logging.log("error", e)
                    """, 
                                                                        # Lambda expression: Returns nc_co
                    {"func":goldy_sub_command.func, "parent_command": parent_command, "command_name":goldy_sub_command.command_name, "help_des":goldy_sub_command.get_help_des(), 
                    "self":goldy_sub_command, "Interaction": GoldyBot.nextcord.Interaction, "GoldyBot": GoldyBot, "asyncio":asyncio, "nextcord":nextcord, 
                    "class_":goldy_sub_command.extension, "no_perms_embed":self.no_perms_embed, "guild_not_registered_embed":self.guild_not_registered_embed, 
                    "hidden":goldy_sub_command.is_hidden, "also_run_parent_CMD":also_run_parent_CMD, "goldy_parent_command": self}, return_data)
                    
                else: # Run as NORMAL command!
                    exec(f"""
@parent_command.subcommand(name=command_name, description=help_des)
async def slash_command_(interaction: Interaction{slash_command_params[0]}):
    ctx = GoldyBot.objects.slash.InteractionToCtx(interaction)
    try:
        if self.allowed_to_run(ctx):
            if also_run_parent_CMD == True: await goldy_parent_command.func(ctx{parent_slash_command_params[1]})
            await func(ctx{slash_command_params[1]})
            GoldyBot.logging.log(f"[{MODULE_NAME}] The slash command '{goldy_sub_command.code_name}' was executed.")

    except GoldyBot.errors.MemberHasNoPermsForCommand:
        if hidden == False:
            no_perms_embed.description = GoldyBot.utility.msgs.bot.CommandNoPerms.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=no_perms_embed)
            await asyncio.sleep(15)
            await message.delete()

    except GoldyBot.errors.GuildNotRegistered:
        if hidden == False:
            guild_not_registered_embed.description = GoldyBot.utility.msgs.bot.CommandGuildNotRegistered.Embed.des.format(ctx.author.mention)
            message = await ctx.send(embed=guild_not_registered_embed)
            await asyncio.sleep(15)
            await message.delete()

    except Exception as e:
        GoldyBot.logging.log("error", e)
                    """, 
                    
                    {"func":goldy_sub_command.func, "parent_command": parent_command, "command_name":goldy_sub_command.command_name, "help_des":goldy_sub_command.get_help_des(), 
                    "self":goldy_sub_command, "Interaction": GoldyBot.nextcord.Interaction, "GoldyBot": GoldyBot, "asyncio":asyncio, "nextcord":nextcord, 
                    "no_perms_embed":self.no_perms_embed, "guild_not_registered_embed":self.guild_not_registered_embed, "hidden":goldy_sub_command.is_hidden, 
                    "also_run_parent_CMD":also_run_parent_CMD, "goldy_parent_command": self}, return_data)

                goldy_sub_command.update_command_object(return_data["slash_command_"])

                GoldyBot.logging.log("info_5", f"[{MODULE_NAME}] Sub Command '{goldy_sub_command.command_name}' of '{parent_command.name}' has been loaded.")
                return goldy_sub_command

            return inner(func, command_name, required_roles, help_des, slash_options)

        return decorate

    def allowed_to_run(self, ctx):
        """Checks if the command is allowed to run with current circumstances."""
        goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))
        
        # Check if guild is registered.
        #--------------------------------
        if str(ctx.guild.id) in goldy_config.read("allowed_guilds"):
            guild_code_name = GoldyBot.cache.FindGuilds(goldy_config).find_object_by_id(ctx.guild.id).code_name
            guild_config = GoldyBot.utility.guilds.config.GuildConfig(GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.CONFIG + f"/{guild_code_name}/config.json")))
            
            if guild_config.is_extension_allowed(self.extension_name):

                if not self.required_roles_ == []:
                    # If the required roles contain 'bot_dev' and the bot dev is running the command allow the command to execute.
                    #----------------------------------------------------------------------------------------------------------------
                    if "bot_dev" in self.required_roles_:
                        if str(ctx.author.id) in GoldyBot.settings.BOT_DEVS:
                            return True

                    # If the required roles contain 'bot_admin' and a bot admin is running the command allow the command to execute. (NEW)
                    #----------------------------------------------------------------------------------------------------------------
                    if "bot_admin" in self.required_roles_:
                        if str(ctx.author.id) in goldy_config.read("admin_users"):
                            return True

                    # Check if member has any of the required roles.
                    #----------------------------------------------------
                    for role_code_name in self.required_roles_:
                        if not role_code_name in ["bot_dev", "bot_admin"]:
                            role = guild_config.get_role(ctx, role_code_name)
                            if GoldyBot.objects.member.Member(ctx).has_role(role):
                                return True

                    raise GoldyBot.errors.MemberHasNoPermsForCommand(f"The member '{ctx.author.name}' does not have the right permissions to use this command.")

                else:
                    return True
                
        else:
            raise GoldyBot.errors.GuildNotRegistered(f"The guild '{ctx.guild.name}' has not been registered.")

    @property
    def guilds_allowed_in(self) -> List[int]:
        """Returns the ids of the guilds this command is allowed to function in."""
        goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))
        allowed_guilds = goldy_config.read("allowed_guilds")

        guilds_command_is_allowed_in:List[int] = []

        for guild_id in allowed_guilds:
            try:
                guild_config = GoldyBot.utility.guilds.config.GuildConfig(GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.CONFIG + f"/{allowed_guilds[guild_id]}/config.json")))
                
                if guild_config.is_extension_allowed(self.extension_name):
                    guilds_command_is_allowed_in.append(int(guild_id))
            except FileNotFoundError:
                pass
            
        if guilds_command_is_allowed_in == []: guilds_command_is_allowed_in = [123]

        print(guilds_command_is_allowed_in)

        return guilds_command_is_allowed_in

    def get_help_des(self) -> str:
        """Returns the command's help description."""
        if self.help_des_ == None:
            try:
                return (importlib.import_module(f'.{self.command_name}', package="GoldyBot.utility.msgs")).help_des

            except ImportError:
                GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not have a 'msg' module, so the help command will not display a help description for it.")
                return "None"

            except AttributeError:
                GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not contain 'help_des' variable in it's 'msg' module, so the help command will not display a help description.")
                return "None"
        else:
            return self.help_des_