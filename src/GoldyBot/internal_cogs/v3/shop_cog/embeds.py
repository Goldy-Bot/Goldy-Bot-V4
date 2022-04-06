import nextcord
import json
import os

from ....GoldyBotV3 import settings
from ....GoldyBotV3.src import goldy_error, goldy_utility, goldy_func
from ....GoldyBotV3.src.utility import msg

class shop():
    class image():
        @staticmethod
        async def update(): #Checks if "shop_images.json" is in config.
            json_file_name = "shop_images.json"

            if not json_file_name in os.listdir("config/"):
                #Create and write to level_up_msgs.json
                shop_images_file = open(f"config/{json_file_name}", "x")
                shop_images_file = open(f"config/{json_file_name}", "w")
                
                json.dump({"urls" : ["https://cdn.discordapp.com/attachments/436201641486581762/878059830600933416/8404015.gif"]}, shop_images_file) #Dumping the example layout in the json file.

        @staticmethod
        async def get(page:int): #Get's random simp image from "simp_images.json".
            json_file_name = "shop_images.json"

            try:
                f = open (f'config/{json_file_name}', "r", encoding="utf8")
                shop_images_normal = json.loads(f.read())

            except FileNotFoundError as e:
                goldy_func.print_and_log("warn", f"'{json_file_name}' was not found. Running update function and trying again. >>> {e}")
                await shop.embeded.image.update()

                f = open (f'config/{json_file_name}', "r", encoding="utf8")
                shop_images_normal = json.loads(f.read())
            
            image_num = page - 1
            max_images = len(shop_images_normal["urls"])
            try:
                return (shop_images_normal["urls"])[image_num]
            except IndexError:
                return (shop_images_normal["urls"])[max_images - 1]

    @staticmethod
    async def get_context(ctx, context, page): #Grabs the correct number of items to view in page. (Used to only grab a certain amount of items for the shop page)
        try:
            last_item = page * 5
            first_item = last_item - 5

            list_of_items = (context.splitlines()[first_item:last_item])
            context = ""
            for command in list_of_items:
                context += command + "\n"

            if context == "":
                return "***There's no more items on this page.***"

            return context

        except Exception as e:
            await goldy_error.log(ctx, f"Failed to grab items!!! {msg.error.contact_dev}\n" + e) #Fix this function thing...
            return "***Failed to grab items!!! Contact a Dev.***"

    @staticmethod
    async def change(msg_obj, page, shop_embed_dict): #Method that changes the shop command page.
        await msg_obj.edit(embed=shop_embed_dict[page]["embed_obj"])
        pass

    @staticmethod
    async def create(ctx, client, commands_context, roles_context, colours_context, page):
        embed=nextcord.Embed(title="**💛🛒 __Shop__**", description="Welcome to Goldy's shop.", color=settings.Aki_Pink)

        commands_context = await shop.get_context(ctx, commands_context, page)
        roles_context = await shop.get_context(ctx, roles_context, page)
        colours_context = await shop.get_context(ctx, colours_context, page)

        server_icon = await goldy_utility.servers.get_icon(ctx, client)
        server_name = await goldy_utility.servers.get_name(ctx)
        embed.set_author(name=f"{server_name} - {ctx.author.name}", url=settings.github_page, icon_url=server_icon)

        embed.add_field(name="__🏷️Ranks__", value=roles_context, inline=False)
        embed.add_field(name="__❗Commands__", value=commands_context, inline=False)
        embed.add_field(name="__🍭Colours__", value=colours_context, inline=False)

        embed.set_image(url=await shop.image.get(page))
        return embed

class inventory():
    @staticmethod
    async def get_context(ctx, context, page): #Grabs the correct number of items to view in page. (Used to only grab a certain amount of items for the shop page)
        try:
            last_item = page * 8
            first_item = last_item - 8

            list_of_items = (context.splitlines()[first_item:last_item])
            context = ""
            for command in list_of_items:
                context += command + "\n"

            if context == "":
                return "***There's no more items on this page.***"

            return context

        except Exception as e:
            await goldy_error.log(ctx, f"Failed to grab items!!! {msg.error.contact_dev}\n" + e)
            return "***Failed to grab items!!! Contact a Dev.***"

    @staticmethod
    async def change(msg_obj, page, inventory_embed_dict): #Method that changes the shop command page.
        await msg_obj.edit(embed=inventory_embed_dict[page]["embed_obj"])
        pass

    @staticmethod
    async def create(ctx, client, items_context, page, net_worth:int, money_emoji):
        context = f"**🚀 __{ctx.author.name}__ ⁃ *Net Worth: {money_emoji}``{net_worth}``***\n\n"
        context += await inventory.get_context(ctx, items_context, page)

        server_icon = await goldy_utility.servers.get_icon(ctx, client)
        server_name = await goldy_utility.servers.get_name(ctx)

        embed=nextcord.Embed(title="**💙📦 __Inventory__**", 
        description=f"Hi, here's what's in your inventory. \n(NOTICE: Only shows items available in discord server.) \n\n {context}", 
        color=settings.BLUE)

        embed.set_author(name=f"{server_name} - {ctx.author.name}", url=settings.github_page, icon_url=server_icon)
        embed.set_thumbnail(url="https://cdn2.scratch.mit.edu/get_image/user/61433373_60x60.gif")
        return embed