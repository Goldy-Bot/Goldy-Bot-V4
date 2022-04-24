import importlib

from nextcord.ext import commands
import GoldyBot

MODULE_NAME = "COMMAND"

class Command():
    def __init__(self, func, command_name=None, required_roles=[]):
        """Generates goldy bot command object with command function object."""
        self.func:function = func

        if command_name == None:
            self.command_name = self.func.__name__
        else:
            self.command_name = command_name
        self.required_roles = required_roles
        self.params_ = list(self.func.__code__.co_varnames)
        self.params_amount_ = self.func.__code__.co_argcount
        
        self.in_extenstion_ = False

        if self.params[0] == "self":
            self.in_extenstion_ = True
            self.params_.pop(0)

        # Add command to extenstion in cache.
        if self.in_extenstion:
            if self.module.is_internal_module:
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.module_name}"]["extenstions"][f"{self.extension_name}"]["commands"].append(self)
            else:
                GoldyBot.cache.main_cache_dict["modules"][f"{self.module_name}"]["extenstions"][f"{self.extension_name}"]["commands"].append(self)
        else:
            GoldyBot.cache.main_cache_dict["internal_modules"]["goldy"]["extenstions"]["core"]["commands"].append(self)

    @property
    def code_name(self) -> str:
        """Returns code name of comamnd."""
        return self.command_name

    @property
    def params(self) -> list:
        """Returns list of function parameters."""
        if self.in_extenstion:
            return self.params_[0:self.params_amount_ - 1]
        else:
            return self.params_[0:self.params_amount_]

    @property
    def extension_name(self) -> str:
        """Returns extension's code name."""
        if self.in_extenstion:
            # Command is in extenstion.
            return str(self.func).split(" ")[1].split(".")[0]
        else:
            # Command is not in any extenstion.
            return None

    @property
    def extenstion(self) -> GoldyBot.ext.extenstions.Extenstion:
        """Finds and returns the object of the command's extenstion."""
        return GoldyBot.cache.FindExtenstions().find_object_by_extenstion_name(extenstion_name=self.extension_name)

    @property
    def in_extenstion(self) -> bool:
        """Returns true/false if the command is in a extenstion."""
        if self.in_extenstion_:
            return True
        else:
            return False

    @property
    def module_name(self) -> str:
        """Returns name of module the command is located in."""
        return self.extenstion.module_name

    @property
    def module(self) -> GoldyBot.modules.Module:
        return GoldyBot.cache.FindModules().find_object_by_module_name(module_name=self.module_name)

    def remove(self):
        """Removes command from nextcord."""
        client:commands.Bot = GoldyBot.cache.main_cache_dict["client"]
        client.remove_command(name=self.code_name)
        GoldyBot.logging.log("info_5", f"[{MODULE_NAME}] Removed the command '{self.code_name}'!")
        return True

    def any_args_missing(self, command_executers_args:tuple) -> bool:
        """Checks if the args given by the command executer matches what paramaters the command needs."""
        if len(command_executers_args) == len(self.params[1:]):
            return True
        else:
            return False

    def allowed_to_run(self, ctx):
        """Checks if the command is allowed to run with currect circumstances."""
        goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))
        
        # Check if guild is registered.
        #--------------------------------
        if str(ctx.guild.id) in goldy_config.read("allowed_guilds"):
            if not self.required_roles == []:
                # If the required roles contain 'bot_dev' and the bot dev is running the command allow the command to exacute.
                #----------------------------------------------------------------------------------------------------------------
                if "bot_dev" in self.required_roles:
                    if str(ctx.author.id) in GoldyBot.settings.BOT_DEVS:
                        return True
                    else:
                        return False # It will look like the command doesn't exist.

                # Check if member has any of the required roles.
                #----------------------------------------------------
                guild_code_name = GoldyBot.cache.FindGuilds(goldy_config).find_object_by_id(ctx.guild.id).code_name
                guild_config = GoldyBot.utility.guilds.config.GuildConfig(GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.CONFIG + f"/{guild_code_name}/config.json")))
                
                for role_code_name in self.required_roles:
                    role = guild_config.get_role(ctx, role_code_name)
                    if GoldyBot.objects.member.Member(ctx).has_role(role):
                        return True

                raise GoldyBot.errors.MemberHasNoPermsForCommand(f"The member '{ctx.author.name}' does not have the right permissions to use this command.")

            else:
                return True
                
        else:
            raise GoldyBot.errors.GuildNotRegistered(f"The guild '{ctx.guild.name}' has not been registered.")

    def get_help_des(self) -> str:
        """Returns the command's help description."""
        try:
            return (importlib.import_module(f'.{self.command_name}', package="GoldyBot.utility.msgs")).help_des

        except ImportError:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not have a 'msg' module, so the help command will not display a help description for it.")
            return "None"

        except AttributeError:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The command '{self.command_name}' does not contain 'help_des' variable in it's 'msg' module, so the help command will not display a help description.")
            return "None"