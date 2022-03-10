from os import stat_result
import nextcord
import settings

from .. import goldy_utility
from .. import goldy_func
from cogs import shop

from . import msg

try:
    import config.config as config
except ModuleNotFoundError as e:
    pass

bot_name = settings.bot_name

class profile():
    class icon():
        @staticmethod
        async def get(ctx): #Get's memeber's profile pic.
            try:
                return ctx.author.avatar.url
            except AttributeError as e:
                return msg.images.no_pfp.logo_1

class roles():
    @staticmethod
    async def get(ctx): #Returns list of ids for the roles the member has in that guild. (Doesn't return role object.)
        roles_list = []
        for role in ctx.author.roles:
            roles_list.append(role.id)

        goldy_func.print_and_log(None, f"[{bot_name.upper()}] Grabbed role ids from the member '{ctx.author.name}'")
        return roles_list

    @staticmethod
    async def give(ctx, role_id): #Find and give member role by id. (Returns 'role' object too.)
        role = nextcord.utils.get(ctx.guild.roles, id=role_id)
        await ctx.author.add_roles(role)

        goldy_func.print_and_log(None, f"[{bot_name.upper()}] Gave '{ctx.author.name}' the role '{role.name}'.")
        return True, role

    @staticmethod
    async def take(ctx, role_id): #Find and takes role away from member by id. (Returns 'role' object too.)
        role = nextcord.utils.get(ctx.guild.roles, id=role_id)
        await ctx.author.remove_roles(role)

        goldy_func.print_and_log(None, f"[{bot_name.upper()}] Took the role '{role.name}' from '{ctx.author.name}'.")
        return True, role

class items():
    @staticmethod
    async def get(member_data): #Get member's item list and colours list in a tuple. Returns 'None' if member has no items list.
        try: items_list = member_data.items
        except AttributeError: items_list = None

        try: colours_list = member_data.colours
        except AttributeError: colours_list = None

        return items_list, colours_list
    
class networth():
    @staticmethod
    async def get(ctx, member_data): #Calculates and returns member's networth.
        networth = 0
        try:
            for item in member_data.items:
                item_data = await shop.items.find_one(ctx, item)

                try: networth += int(item_data.price)
                except AttributeError: pass
        except AttributeError:
            pass
        
        try:
            for colour in member_data.colours:
                item_data = await shop.items.find_one(ctx, colour)

                try: networth += int(item_data.price)
                except AttributeError: pass
        except AttributeError:
            pass

        goldy_func.print_and_log(None, f"[{bot_name.upper()}] Calculated net worth of '{ctx.author.name}'.")
        return networth

class checks():
    @staticmethod
    async def in_vc(ctx):
        voice_state = ctx.author.voice
        if voice_state == None: return False
        else: return True