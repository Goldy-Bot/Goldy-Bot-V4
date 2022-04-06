from types import SimpleNamespace
import nextcord
from nextcord import guild
from nextcord.ext import commands
import asyncio
import datetime
import traceback
import os
import json

from ...GoldyBotV3 import settings
from ...GoldyBotV3.src import goldy_utility, goldy_func, goldy_cache, goldy_error
from ...GoldyBotV3.src.utility import cmds, members
from ...GoldyBotV3.src.utility import msg
try:
    import config.config as config
except ModuleNotFoundError as e:
    pass

from . import database, economy

from .shop_cog import embeds, items

cog_name = "shop".upper()

class shop(commands.Cog, name="🛒Shop"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 3

    #NEW shop command!
    @commands.command(aliases=[], usage="!shop {page}")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def shop(self, ctx, page_choice:int=None):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            items_data = await items.find(ctx)
            server_info = goldy_utility.servers.get(ctx.guild.id)

            #Grab all commands.
            commands_context = ""
            for command in items_data[0].commands.list:
                #Picking the item data.
                name = (items_data[1]["commands"][command]["names"]["display_name"])
                price = (items_data[1]["commands"][command]["price"])

                #Check if member has item.
                if await database.database.member.checks.has_item(ctx, command): possession_status = "✅"
                else: possession_status = "❌"

                commands_context += f"**• {name} (CMD): **{server_info.config.money_emoji}``{price}`` **{possession_status}**\n"

            #Grab all roles.
            roles_context = ""
            for role in items_data[0].roles.list:
                #Picking the item data.
                rank_mention = (nextcord.utils.get(ctx.guild.roles, id=items_data[1]["roles"][role]["id"])).mention
                price = (items_data[1]["roles"][role]["price"])

                #Check if member has item.
                if await database.database.member.checks.has_item(ctx, role): possession_status = "✅"
                else: possession_status = "❌"

                roles_context += f"**• {rank_mention} (RANK): **{server_info.config.money_emoji}``{price}`` **{possession_status}**\n"

            #Grab all colours.
            colours_context = ""
            for colour in items_data[0].colours.list:
                #Picking the item data.
                colour_mention = (nextcord.utils.get(ctx.guild.roles, id=items_data[1]["colours"][colour]["id"])).mention
                price = (items_data[1]["colours"][colour]["price"])

                #Check if member has item.
                if await database.database.member.checks.has_item(ctx, colour, type="colour"): possession_status = "✅"
                else: possession_status = "❌"

                colours_context += f"**• {colour_mention} (COLOUR): **{server_info.config.money_emoji}``{price}`` **{possession_status}**\n"

            BUTTONS = ["◀️", "▶️"]
            shop_embed_dict = {}
            page_count = 1
            shop_bt_current_page = 1
            (a, b, c) = len(items_data[0].commands.list), len(items_data[0].roles.list), len(items_data[0].colours.list)
            shop_embed_dict[1] = {}
            shop_embed_dict[1]["embed_obj"] = await embeds.shop.create(ctx, self.client, commands_context, roles_context, colours_context, 1)

            #Create pages accoring to the amount of items.
            while a > 5*page_count or b > 5*page_count or c > 5*page_count:
                page_count += 1
                new_embed = await embeds.shop.create(ctx, self.client, commands_context, roles_context, colours_context, page_count)
                shop_embed_dict[page_count] = {}
                shop_embed_dict[page_count]["embed_obj"] = new_embed

            shop_embed_dict["max_pages"] = page_count

            #Apply footer to all pages.
            for page in shop_embed_dict:
                if not page == "max_pages":
                    embed = shop_embed_dict[int(page)]["embed_obj"]
                    max_pages = shop_embed_dict["max_pages"]
                    embed.set_footer(text=f"[PAGE {page}/{max_pages}] " + msg.footer.type_2)
            
            #Start of Command
            if not page_choice == None:
                try:
                    message = await ctx.send(embed=shop_embed_dict[page_choice]["embed_obj"])
                    bt_current_page = page_choice
                except KeyError:
                    await ctx.send(msg.shop.page_out_of_range.format(ctx.author.mention))
            else:
                message = await ctx.send(embed=shop_embed_dict[1]["embed_obj"])

            #Add reactions.
            for button in BUTTONS:
                await message.add_reaction(button)

            #Wait for user inputs.
            while True:
                try:
                    reaction, user = await goldy_cache.client.wait_for('reaction_add', timeout=360)
                    if not user == goldy_cache.client.user: #Ignores reactions from itself.
                        if reaction.message == message:
                            if reaction.emoji == BUTTONS[0]: #Backwards button.
                                if not shop_bt_current_page <= 1: #Stops page num from going under 1.
                                    shop_bt_current_page -= 1
                                    await embeds.shop.change(message, page=shop_bt_current_page, shop_embed_dict=shop_embed_dict)
                                    await message.remove_reaction(reaction.emoji, user)
                                else:
                                    await message.remove_reaction(reaction.emoji, user)

                            if reaction.emoji == BUTTONS[1]: #Forwards button.
                                if not shop_bt_current_page >= page_count:
                                    shop_bt_current_page += 1 #Stops page num from going over max amount.
                                    await embeds.shop.change(message, page=shop_bt_current_page, shop_embed_dict=shop_embed_dict)
                                    await message.remove_reaction(reaction.emoji, user)
                                else:
                                    await message.remove_reaction(reaction.emoji, user)

                except asyncio.TimeoutError:
                    #Clear reactions first.
                    for button in BUTTONS:
                        await message.clear_reaction(button)

                    break #Stop loop

    @shop.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error); return
        if isinstance(error, (commands.BadArgument, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!shop {page}")); return
        else:
            await goldy_error.log(ctx, self.client, error, "shop.shop")



    #Buy Command
    @commands.command(description="For buying items from the shop.")
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    async def buy(self, ctx, *, item=None): #Work in progress.
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            if not item == None:
                items_data = await items.find_one(ctx, item)

                if not items_data == False:
                    #Buy item
                    await items.buy(ctx, self.client, items_data)

                if items_data == False:
                    await ctx.send((msg.buy.failed.no_exist).format(ctx.author.mention))

            if item == None:
                await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!buy {item}"))

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        else:
            await goldy_error.log(ctx, self.client, error, "shop.buy")



    #Sell Command
    @commands.command(description="For selling items you own.")
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    async def sell(self, ctx, *, item=None):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            if not item == None:
                items_data = await items.find_one(ctx, item)

                if not items_data == False:
                    #Sell item
                    await items.sell(ctx, self.client, items_data)

                if items_data == False:
                    await ctx.send((msg.sell.failed.no_exist).format(ctx.author.mention))

            if item == None:
                await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!sell {item}"))

    @sell.error
    async def sell_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        else:
            await goldy_error.log(ctx, self.client, error, "shop.sell")



    #Inventory Command
    @commands.command(aliases=["inv", "items"], usage="!inv {page}")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def inventory(self, ctx, page_choice:int=None):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            member_data = await database.database.member.pull(ctx)
            items_list = await members.items.get(member_data)
            net_worth = await members.networth.get(ctx, member_data)
            money_emoji = await goldy_utility.servers.money_emoji.get(ctx)
            
            items_context = "**❗ __Commands & 🏷️Ranks__**\n"
            for item in items_list[0]:
                item_data = await items.find_one(ctx, item)

                if not item_data == False:
                    name = await items.get_name(ctx, item_data)
                    item_type = (await items.checks.item_type(item_data)).upper()

                    if item_type.lower() == "role":
                        items_context += f"**• {name} ⁃** {money_emoji}``{item_data.price}``\n"
                    else:
                        items_context += f"**•** ``{name}`` **⁃** {money_emoji}``{item_data.price}`` \n"

            items_context += "\n**🍭 __Colours__ **\n"
            for item in items_list[1]:
                item_data = await items.find_one(ctx, item)

                if not item_data == False:
                    name = await items.get_name(ctx, item_data)

                    items_context += f"**• {name} ⁃** {money_emoji}``{item_data.price}`` \n"

            BUTTONS = ["◀️", "▶️"]
            inventory_embed_dict = {}
            page_count = 1
            inventory_bt_current_page = 1
            inventory_embed_dict[1] = {}
            inventory_embed_dict[1]["embed_obj"] = await embeds.inventory.create(ctx, self.client, items_context, 1, net_worth, money_emoji)

            #Create pages accoring to the amount of items.
            while len(items_context.splitlines()) > 8*page_count:
                page_count += 1
                new_embed = await embeds.inventory.create(ctx, self.client, items_context, page_count, net_worth, money_emoji)
                inventory_embed_dict[page_count] = {}
                inventory_embed_dict[page_count]["embed_obj"] = new_embed

            inventory_embed_dict["max_pages"] = page_count

            #Apply footer to all pages.
            for page in inventory_embed_dict:
                if not page == "max_pages":
                    embed = inventory_embed_dict[int(page)]["embed_obj"]
                    max_pages = inventory_embed_dict["max_pages"]
                    embed.set_footer(text=f"[PAGE {page}/{max_pages}] " + msg.footer.type_2)
            
            #Start of Command
            if not page_choice == None:
                try:
                    message = await ctx.send(embed=inventory_embed_dict[page_choice]["embed_obj"])
                    bt_current_page = page_choice
                except KeyError:
                    await ctx.send(msg.shop.page_out_of_range.format(ctx.author.mention))
            else:
                message = await ctx.send(embed=inventory_embed_dict[1]["embed_obj"])

            #Add reactions.
            for button in BUTTONS:
                await message.add_reaction(button)

            #Wait for user inputs.
            while True:
                try:
                    reaction, user = await goldy_cache.client.wait_for('reaction_add', timeout=360)
                    if not user == goldy_cache.client.user: #Ignores reactions from itself.
                        if user == ctx.author: #Only change page if author is reacting.
                            if reaction.message == message:
                                if reaction.emoji == BUTTONS[0]: #Backwards button.
                                    if not inventory_bt_current_page <= 1: #Stops page num from going under 1.
                                        inventory_bt_current_page -= 1
                                        await embeds.inventory.change(message, page=inventory_bt_current_page, inventory_embed_dict=inventory_embed_dict)
                                        await message.remove_reaction(reaction.emoji, user)
                                    else:
                                        await message.remove_reaction(reaction.emoji, user)

                                if reaction.emoji == BUTTONS[1]: #Forwards button.
                                    if not inventory_bt_current_page >= page_count:
                                        inventory_bt_current_page += 1 #Stops page num from going over max amount.
                                        await embeds.inventory.change(message, page=inventory_bt_current_page, inventory_embed_dict=inventory_embed_dict)
                                        await message.remove_reaction(reaction.emoji, user)
                                    else:
                                        await message.remove_reaction(reaction.emoji, user)

                except asyncio.TimeoutError:
                    #Clear reactions first.
                    for button in BUTTONS:
                        await message.clear_reaction(button)

                    break #Stop loop
            pass

    @inventory.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error); return
        if isinstance(error, (commands.BadArgument, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!inv {page}")); return
        else:
            await goldy_error.log(ctx, self.client, error, "shop.inventory")

def setup(client):
    client.add_cog(shop(client))