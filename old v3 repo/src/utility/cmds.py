import datetime
from inspect import Attribute
import json
import nextcord
from cogs.halloween_cog.bats import embed
import settings

from .. import goldy_utility

from . import msg
from . import members

from cogs import shop

try:
    import config.config as config
except ModuleNotFoundError as e:
    pass

async def can_the_command_run(ctx, cog_name=None): #The function that get's ran in EVERY single command in goldy bot.

    try: #Is command being called from a discord guild.
        guild_id = ctx.guild.id
    except AttributeError as e:
        if ctx.author.id in settings.admin_users:
            return True #If author is admin allow.
        else:
            return False #Disables commands from being called in dm's.

    #Is the guild in servers.json.
    server_info = goldy_utility.servers.get(guild_id)

    if server_info == False:
        try:
            await ctx.send(msg.error.server_not_registered) #Sends this message --> 'This server is not registered. Contact the Developer: Dev Goldy/The Golden Pro (https://github.com/THEGOLDENPRO)'
        except AttributeError as e: #Added in V3.08
            pass #Silences attribute errors.
        
        return False

    #Does discord server allow the cog.
    cog_allowed = goldy_utility.servers.cogs.is_allowed(guild_id, cog_name, server_info=server_info)

    if not cog_allowed == None:
        if cog_allowed == False:
            try:
                if not cog_name in await goldy_utility.servers.hidden_cogs.get(ctx):
                    await ctx.send(msg.error.command_disabled_by_server) #Sends this message saying 'This command is disabled by the server.'
            except AttributeError as e:
                pass
            return False

        if cog_allowed == True:
            pass

    #Is bot in dev mode or production mode?
    if config.bot_mode == 'P':
        return True

    if config.bot_mode == 'D':
        if ctx.channel.id == server_info.channels.dev_channel:
            return True

    return False

class rank():
    @staticmethod
    async def can_the_command_run(ctx, code_names:list): #This function takes in a list of roles and only returns True if the member has any of those roles. (WARNING: Role has to be )
        member_roles_id_list = await members.roles.get(ctx)
        roles_list = []
        mention_ranks_list = ""
        count = 0

        server_info = goldy_utility.servers.get(ctx.guild.id)
        server_code_name = server_info.names.code_name

        #Guild items.json.
        f = open (f'./config/{server_code_name}/items.json', "r", encoding="utf8")
        guild_items_json = json.loads(f.read())

        for rank in code_names:
            try:
                item_data = guild_items_json["roles"][rank]
                roles_list.append(nextcord.utils.get(ctx.guild.roles, id=item_data["id"]))
                if item_data["id"] in member_roles_id_list:
                    return True
            except KeyError:
                try:
                    roles_list.append(nextcord.utils.get(ctx.guild.roles, id=rank)) #Assume string is id of role.
                except Exception:
                    pass

        for role in roles_list:
            count += 1
            if count == 1:
                mention_ranks_list += f"{role.mention}"
            else:
                mention_ranks_list += f", {role.mention}"
            
        embed = nextcord.Embed(title="**💛🚫 Rank Exclusive Command!**", description=msg.error.command_these_ranks_only.format(ctx.author.mention, mention_ranks_list))
        await ctx.send(embed=embed)
        return False, roles_list


class cooldown(): #Class that will house all the command cooldown functions.

    @staticmethod
    async def msg_send(ctx, error): #Sends cooldown message to author's dms.
        embed = nextcord.Embed(title="**❤️ Slow Down, please!**", description=msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))), color=settings.RED)
        embed.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/502e9c70122067.5b98d56c402af.gif")
        await ctx.author.send(embed=embed)