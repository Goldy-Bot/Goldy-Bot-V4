import json
from types import SimpleNamespace
import traceback
import nextcord

import settings
from src import goldy_utility, goldy_error, goldy_func
from src.utility import members, msg
from cogs import database, economy

module_name = "items"

class roles():
    class bundle:
        @staticmethod
        async def find(ctx, bundle_code_name): #Finds the role bundle data.
            try:
                server_info = goldy_utility.servers.get(ctx.guild.id)
                server_code_name = server_info.names.code_name

                code_name = bundle_code_name
                
                f = open (f'config/{server_code_name}/items.json', "r", encoding="utf8")
                bundles_json = json.loads(f.read())

                async def found_bundle(bundle_json):
                    bundle_json = json.dumps(bundle_json)
                    bundle_info = json.loads(bundle_json, object_hook=lambda d: SimpleNamespace(**d))
                    
                    return bundle_info #Returns the json but as python class so you can easily pick the data.

                #Find the bundles.
                for bundle in bundles_json["roles"]:
                    if bundle == code_name:
                        if str(bundle)[0] == "@":
                            bundle_json = bundles_json["roles"][code_name]
                            bundle_json["type"] = "role_bundle"
                            bundle_info = await found_bundle(bundle_json)
                            return bundle_info

                #If bundle not found.
                return False

            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())

    @staticmethod
    async def is_merging(ctx, item_data): #Checks if there's any role confilct going on.
        #Check if item has 'do_not_merge_with' object in config.
        try:
            #Find 'do_not_merge_with' object.
            try:
                merging = item_data.config.do_not_merge_with
            except AttributeError as e:
                return (False, None)

            #If 'do_not_merge_with' object exist find the role bundle.
            role_bundle_info = await roles.bundle.find(ctx, merging)

            #Check if member has any roles in list.
            for role_id in role_bundle_info.ids:
                role = nextcord.utils.get(ctx.guild.roles, id=role_id)

                if role in ctx.author.roles: #If member does, return True immediately.
                    return (True, role)

            #If member has none of the roles return False.
            return (False, None)

        except Exception as e:
            goldy_error.log(None, error=traceback.format_exc())

    @staticmethod
    async def give(ctx, item_data, item_data_is_role=False): #Give a member a role safely.
        if item_data_is_role == False:
            role = nextcord.utils.get(ctx.guild.roles, id=item_data.id)
        else:
            role = item_data

        has_role = None
        #Check if member has role.
        if role in ctx.author.roles:
            has_role = True
        else:
            has_role = False

        if has_role == True:
            return False
        if has_role == False:
            await ctx.author.add_roles(role)
            goldy_func.print_and_log(None, f"[{module_name.upper()}] Gave '{role.name}' to '{ctx.author.name}'.")
            return True

    @staticmethod
    async def take(ctx, item_data, item_data_is_role=False): #Remove a role from a member safely.
        if item_data_is_role == False:
            role = nextcord.utils.get(ctx.guild.roles, id=item_data.id)
        else:
            role = item_data

        has_role = None
        #Check if member has role.
        if role in ctx.author.roles:
            has_role = True
        else:
            has_role = False

        if has_role == True:
            await ctx.author.remove_roles(role)
            goldy_func.print_and_log(None, f"[{module_name.upper()}] Removed '{role.name}' from '{ctx.author.name}''.")
            return True
        if has_role == False:
            return False

class checks():
    @staticmethod
    async def item_type(item_data): #Tells you what type the item is, a command(cmd), a role or a colour. (ITEM TYPE IS USALLY GIVEN TO A ITEM IN THE "FIND_ONE" METHOD) (Used in buy function.)
        try: item_type = item_data.type 
        except AttributeError: return None
        return item_type

    @staticmethod
    async def is_sellable(item_data):  
        try:
            #Find sellable object
            try:
                sellable = item_data.config.sellable
            except AttributeError as e:
                sellable = None

            if sellable == None: #If not specified, it will default to True.
                return True
            else:
                return sellable

        except Exception as e:
            goldy_func.print_and_log("error", f"Exception in shop.items.checks.is_sellable method. {e}")

async def find(ctx): #Grabs data/info of all items. (Used in commands like the shop command.)
    server_info = goldy_utility.servers.get(ctx.guild.id)
    server_code_name = server_info.names.code_name
    
    async def run():
        #Guild items.json.
        f = open (f'./config/{server_code_name}/items.json', "r", encoding="utf8")
        guild_items_json_normal = json.loads(f.read())

        #Global items.json.
        f = open (f'./config/global/items.json', "r", encoding="utf8")
        global_items_json_normal = json.loads(f.read())

        #Combind items data.
        items_json_normal = await merge(guild_items_json_normal, global_items_json_normal)
        
        #Format data.
        items_json = json.dumps(items_json_normal)
        items_info_formatted = json.loads(items_json, object_hook=lambda d: SimpleNamespace(**d))
        
        return items_info_formatted, items_json_normal #Returns the json but as python class so you can easily pick the data.

    try:
        return await run()

    except FileNotFoundError as e:
        goldy_func.print_and_log("warn", f"'items.json' was not found. Running update function and trying again. >>> {e}")
        await goldy_utility.servers.update()
        return await run()

    except Exception as e:
        await goldy_error.log(None, error=traceback.format_exc())

async def find_one(ctx, code_name): #Grabs data/info of an item. (Used for getting info for a percific item only but is slower than find() if used to find multiple items.)
    server_info = goldy_utility.servers.get(ctx.guild.id)
    server_code_name = server_info.names.code_name

    code_name = code_name.lower()
    
    async def run():
        #Guild items.json.
        f = open (f'./config/{server_code_name}/items.json', "r", encoding="utf8")
        guild_items_json = json.loads(f.read())

        #Global items.json.
        f = open (f'./config/global/items.json', "r", encoding="utf8")
        global_items_json = json.loads(f.read())

        items_json = (guild_items_json, global_items_json)

        async def found_item(item_json):
            item_json = json.dumps(item_json)
            item_info = json.loads(item_json, object_hook=lambda d: SimpleNamespace(**d))
            
            return item_info #Returns the json but as python class so you can easily pick the data.
        
        #Find the guild items and global items.
        for i in range(len(items_json)):

            for command in items_json[i]["commands"]["list"]:
                if not (code_name[0]) == "!": #Allows function to still find the command even if there's no '!' at the start.
                    new_code_name = "!" + code_name
                else:
                    new_code_name = code_name

                if command == new_code_name:
                    item_json = items_json[i]["commands"][new_code_name]
                    item_json["type"] = "cmd"
                    item_info = await found_item(item_json)
                    return item_info
            
            try:
                for role in items_json[i]["roles"]["list"]:
                    if role == code_name:
                        item_json = items_json[i]["roles"][code_name]
                        item_json["type"] = "role"
                        item_info = await found_item(item_json)
                        return item_info
            except KeyError:
                pass

            for colour in items_json[i]["colours"]["list"]:
                if colour == code_name.replace(" ", "_"):
                    item_json = items_json[i]["colours"][code_name.replace(" ", "_")]
                    item_json["type"] = "colour"
                    item_info = await found_item(item_json)
                    return item_info

        #If item not found.
        return False

    try:
        return await run()

    except FileNotFoundError as e:
        goldy_func.print_and_log("warn", f"'items.json' was not found. Running update function and trying again. >>> {traceback.format_exc()}")
        await goldy_utility.servers.update()

        return await run()

    except Exception as e:
        await goldy_error.log(None, error=traceback.format_exc())

async def get_name(ctx, item_data): #Get's actually name of item.
    
    try:
        #Find display name
        try:
            display_name = item_data.display_name
        except AttributeError as e:
            display_name = None

        if display_name == None:
            #If the item is a role, change item name to role mention.
            if await checks.item_type(item_data) == "role":
                role_mention = (nextcord.utils.get(ctx.guild.roles, id=item_data.id)).mention
                item_name = role_mention
                return item_name
            if await checks.item_type(item_data) == "colour":
                role_mention = (nextcord.utils.get(ctx.guild.roles, id=item_data.id)).mention
                item_name = role_mention
                return item_name
            else:
                item_name = item_data.names.code_name
                return item_name

        if not display_name == None:
            return item_data.display_name

    except Exception as e:
        await goldy_error.log(None, error=traceback.format_exc())

async def get_code_name(item_data): #Get's code_name of item without hassle. (This is the recommended way!)
    try:
        if await checks.item_type(item_data) == "colour":
            return item_data.code_name
        else:
            return item_data.names.code_name

    except Exception as e:
        await goldy_error.log(None, error=traceback.format_exc())

async def get_embed(item_data): #Get's the item's image and msg for buy/sell embed.
    try:
        if await checks.item_type(item_data) == "colour":
            import cogs.colours_cog.msg as colours_msg; return colours_msg.buy.msg, colours_msg.buy.gif
        else:
            return item_data.embed.msg, item_data.embed.image

    except Exception as e:
        await goldy_error.log(None, error=traceback.format_exc())

async def merge(guild_items_json_normal, global_items_json_normal): #Merges global items with guild items.
    merged_items_json_normal = {}

    #Commands
    merged_items_json_normal["commands"] = await goldy_utility.goldy_methods.dict.merge(guild_items_json_normal["commands"], global_items_json_normal["commands"])
    merged_items_json_normal["commands"]["list"] = guild_items_json_normal["commands"]["list"] + global_items_json_normal["commands"]["list"] #Alter the list.
    
    #Roles
    merged_items_json_normal["roles"] = guild_items_json_normal["roles"]
    
    #Colours
    merged_items_json_normal["colours"] = await goldy_utility.goldy_methods.dict.merge(guild_items_json_normal["colours"], global_items_json_normal["colours"])
    merged_items_json_normal["colours"]["list"] = guild_items_json_normal["colours"]["list"] + global_items_json_normal["colours"]["list"] #Alter the list.

    return merged_items_json_normal

async def buy(ctx, client, item_data): #This buy function handels purchusing the item and sending Purchased embeded.
    item = await get_name(ctx, item_data)

    #Check if member has item.
    has_item = await database.database.member.checks.has_item(ctx, await get_code_name(item_data), type=await checks.item_type(item_data))
    if has_item == True:
        await ctx.send((msg.buy.failed.already_own).format(ctx.author.mention))
        return False

    #If the item is a role add the role, update member's prefix and check if it merges with any other roles.
    if await checks.item_type(item_data) == "role":
        is_it_merging = await roles.is_merging(ctx, item_data)
        if is_it_merging[0] == True:
            role_that_is_causing_it = is_it_merging[1]
            
            description_message = ((msg.buy.failed.role_conflict).format(ctx.author.mention, role_that_is_causing_it.mention, item))
            title_message = "❌ __PURCHASE FAILED!__"
            embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.RED)
            embed.set_footer(text=msg.footer.type_2)
            embed.set_thumbnail(url="https://c.tenor.com/t3Vqq1DiC0YAAAAM/obama-cool-kids-club.gif")
            await ctx.send(embed=embed)
            return False

        #Add role to member.
        await members.roles.give(ctx, item_data.id)
        #Update member's prefix.

    #Payment process.
    user_bal = await economy.economy.member.subtract(ctx, client, item_data.price)
    if user_bal == False: #Get's exacuted if member doesn't have enough money.
        await ctx.send((msg.buy.failed.no_money).format(ctx.author.mention))
        return False

    user_bal = '{:.2f}'.format(round(user_bal, 2))

    #Give user item.
    member_data = await database.database.member.pull(ctx) #Pull member data.

    #If the item is a colour, append to colours list instead of items list.
    if await checks.item_type(item_data) == "colour":
        member_colours = member_data.colours #Create copy of list.
        member_colours.append(await get_code_name(item_data)) #Append item to the list.
        member_data.colours = member_colours #Update the original list with modified list.

    else: #For all other items.
        member_items = member_data.items #Create copy of list.
        member_items.append(await get_code_name(item_data)) #Append item to the list.
        member_data.items = member_items #Update the original list with modified list.

    await database.database.member.push(ctx, member_data) #Push member data back to whatever hole it came from. 😏

    #Get money emoji.
    server_info = goldy_utility.servers.get(ctx.guild.id) #Getting server info.
    money_emoji = server_info.config.money_emoji #Grabbing emoji
    
    #Embeded message
    (embed_msg, embed_gif) = await get_embed(item_data)
    description_message = ((msg.buy.embed.item_context).format(ctx.author.mention, item, embed_msg, money_emoji, item_data.price, money_emoji, user_bal))
    title_message = "✅ __Purchase Complete!__"
    embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.GREEN)
    embed.set_footer(text=msg.footer.type_2)
    if not embed_gif in ["", None]: #yes ThIs iS tHe LAzY MEtHod
        embed.set_thumbnail(url=embed_gif)
    await ctx.send(embed=embed)

    #You horny?

    return True #Tells buy command purchase was complete and it can progress.

async def sell(ctx, client, item_data):
    item = await get_name(ctx, item_data) #Replace this with 'shop.item.get_name' when done with coding it OR ELSE BUYING ROLES WON'T WORK!

    #Check if member has item.
    has_item = await database.database.member.checks.has_item(ctx, await get_code_name(item_data), type=await checks.item_type(item_data))
    if has_item == False:
        await ctx.send((msg.sell.failed.do_not_have_item).format(ctx.author.mention))
        return False

    #Check if item is sellable.
    sellable = await checks.is_sellable(item_data)
    if sellable == False:
        await ctx.send((msg.sell.failed.not_sellable).format(ctx.author.mention))
        return False

    a = settings.sell_tax*0.01
    x = item_data.price*a #Applying Sell Tax
    amount = item_data.price - x

    #Payment process.
    user_bal = await economy.economy.member.add(ctx, client, amount)
    user_bal = '{:.2f}'.format(round(user_bal, 2))
    amount = '{:.2f}'.format(round(amount, 2))

    #Remove item from user.
    member_data = await database.database.member.pull(ctx) #Pull member data.
    
    #If the item is a colour, remove from colours list instead of items list.
    if await checks.item_type(item_data) == "colour":
        member_colours = member_data.colours #Create copy of list.
        try:
            member_colours.remove(await get_code_name(item_data)) #Remove item from the list.
        except ValueError as e:
            pass
        member_data.colours = member_colours #Update the original list with modified list.

    else:
        member_items = member_data.items #Create copy of list.
        try:
            member_items.remove(await get_code_name(item_data)) #Remove item from the list.
        except ValueError as e:
            pass
        member_data.items = member_items #Update the original list with modified list.

    await database.database.member.push(ctx, member_data) #Push member data back up.

    #If the item is a role update member's prefix and remove role from member.
    if await checks.item_type(item_data) == "role":
        #Remove role from member.
        await members.roles.take(ctx, item_data.id)

        #Update member's prefix.

    #Get money emoji.
    server_info = goldy_utility.servers.get(ctx.guild.id) #Getting server info.
    money_emoji = server_info.config.money_emoji #Grabbing emoji
    
    #Embeded message
    (embed_msg, embed_gif) = await get_embed(item_data)
    description_message = ((msg.sell.embed.main_context).format(ctx.author.mention, item, money_emoji, amount, money_emoji, user_bal, money_emoji, settings.sell_tax))
    title_message = "🤝 __ITEM SOLD!__"
    embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.YELLOW)
    embed.set_footer(text=msg.footer.type_2)
    if not embed_gif in ["", None]:
        embed.set_thumbnail(url=embed_gif)
    await ctx.send(embed=embed)

    #You still horny?

    return True #Tells buy command purchase was complete and it can progress.