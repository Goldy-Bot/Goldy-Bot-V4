import os
import nextcord
from nextcord.ext import commands

from .. import settings
from . import goldy_func, goldy_cache, goldy_utility
from .utility import msg

"""
Goldy Bot's error handler.
"""
MODULE_NAME = "Error Handler"

class checks():
    @staticmethod
    async def is_allowed(server_info): #Checks if discord guild allows error logging.
        try:
            is_allowed = server_info.config.allow_error_logging
        except AttributeError as e:
            return False

        return is_allowed

async def log(ctx=None, client=goldy_cache.client, error=None, command_name=None): #The default logging function. This handles reporting the error to the member and master.
    import traceback

    #Common Errors to ignore.
    if isinstance(error, (commands.errors.MemberNotFound, commands.errors.CommandOnCooldown)):
        goldy_func.print_and_log("warn", f"[{MODULE_NAME.upper()}] Error ignored! >>> {error}")
        return

    if not ctx == None:
        #Find guild info.
        server_info = goldy_utility.servers.get(ctx.guild.id)

        #First check if server allows error logging.
        if await checks.is_allowed(server_info) == True:
            #Get channel object.
            log_channel = await channel.get(ctx, server_info)
            
            #Get error tag role.
            tag = await role.get(ctx, server_info)

            if not log_channel == None:
                data_and_time = goldy_func.get_time_and_date("both")

                #Print error in console
                goldy_func.print_and_log("error", f"Command Error: {traceback.format_exc()} \n(Triggered by '{ctx.author}') \n(Occurred in command '{command_name}')")
                goldy_func.print_and_log()

                #Now send error to guilds log channel.
                embed = nextcord.Embed(description=f"**{tag.mention} {data_and_time} - __Triggered by {ctx.author.mention}__** ```{error} \n(Occurred in command '{command_name}') (FULL ERROR IN CONSOLE)``` **[🦘Jump To Message]({ctx.message.jump_url}) -** *__🧡Goldy Bot V3 Error Handler__*")
                await log_channel.send(embed=embed)

            if log_channel == None:
                goldy_func.print_and_log("info", f"'{server_info.names.code_name}' discord server has not specified an id for the error channel, so I'm ignoring and not sending the error in the channel.")

                data_and_time = goldy_func.get_time_and_date("both")

                #Print error in console
                goldy_func.print_and_log("error", f"Command Error: {traceback.format_exc()} \n(Triggered by {ctx.author}) \n(Occurred in command '{command_name}')")
                goldy_func.print_and_log()

            #Send error reported message to member.
            master_object = client.get_user(settings.MASTER)
            description_message = ((msg.error.command_exception).format(ctx.author.mention, master_object.mention))
            title_message = "❤️❌ __ERROR OCCURRED!__"
            embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.GREY)
            await ctx.send(embed=embed)

    else:
        #Print error in console
        goldy_func.print_and_log("error", f"{traceback.format_exc()} \n(Occurred in '{command_name}')")
        goldy_func.print_and_log()

class channel(): #Class for the logging channel

    class checks():
        @staticmethod
        async def is_available(server_info):
            try:
                error_channel = server_info.channels.error_channel
                if error_channel in ["", None]:
                    return False
                return True
            except AttributeError as e:
                return False

    @staticmethod
    async def get(ctx, server_info):
        if await channel.checks.is_available(server_info):
            error_channel_id = server_info.channels.error_channel
            error_channel = nextcord.utils.get(ctx.guild.channels, id=error_channel_id)
            return error_channel
        else:
            return None


class role(): #Class for the error role.

    class checks():
        @staticmethod
        async def is_available(server_info): #Checks if error role is available.
            try:
                error_role = server_info.roles.error_role
                if error_role in ["", None]:
                    return False
                return True
            except AttributeError as e:
                return False

    @staticmethod
    async def get(ctx, server_info): #Get error role for that guild. Returns role object.
        if await role.checks.is_available(server_info):
            error_role_id = server_info.roles.error_role
            error_role = nextcord.utils.get(ctx.guild.roles, id=error_role_id)
            return error_role
        else:
            return "ERROR" #Just returns string if no error role is found.
            
