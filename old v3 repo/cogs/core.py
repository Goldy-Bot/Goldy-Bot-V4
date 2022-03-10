import datetime
import nextcord
from nextcord.errors import HTTPException
from nextcord.ext import commands
import json
import time
import asyncio

from nextcord.ext.commands.core import command
from nextcord.ext.commands.help import HelpCommand
from cogs.database import database

from src.goldy_func import *
from src.goldy_utility import *
import src.utility.msg as msg
import src.goldy_cache as goldy_cache

from cogs import shop, economy, rank_system

cog_name = "core"

class goldy_help_command(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    class embed():
        @staticmethod
        async def create(help_type, description=None, thumbnail_url=None, page_num=None):
            if description == None:
                description = msg.help.embed.des

            embed = nextcord.Embed(title=(msg.help.embed.title).format(help_type), description=description, color=settings.WHITE)
            if not thumbnail_url == None:
                embed.set_thumbnail(url=thumbnail_url)
            if not page_num == None:
                embed.set_footer(text=msg.footer.type_2 + f" [PAGE {page_num}]")
            return embed

        class page():
            @staticmethod
            async def change(msg_obj, page, help_embed_dict): #Method that changes the help command page.
                await msg_obj.edit(embed=help_embed_dict[page]["embed_obj"])
                pass

    async def send_bot_help(self, mapping):
        bot_icon = goldy_cache.client.user.display_avatar.url
        BUTTONS = ["◀️", "▶️"]
        help_embed_dict = {}
        extenstion_count = 0
        page_count = 1
        embed = await goldy_help_command.embed.create("Overview", thumbnail_url=bot_icon, page_num=page_count)
        help_embed_dict[page_count] = {}
        help_embed_dict[page_count]["embed_obj"] = embed
        value = False

        for cog in mapping:
            if not cog == None:
                if extenstion_count >= config.max_extenstions*page_count:
                    page_count += 1
                    new_embed = await goldy_help_command.embed.create("Overview", thumbnail_url=bot_icon, page_num=page_count)

                    help_embed_dict[page_count] = {}
                    help_embed_dict[page_count]["embed_obj"] = new_embed

                help_embed_dict[page_count]["embed_context"] = ""

                if servers.cogs.is_allowed(self.get_destination().guild.id, cog.cog_name):
                    if cog.cog_name == "core":
                        value = False
                    else:
                        value = True

                    if value:
                        for command in mapping[cog]:
                            help_embed_dict[page_count]["embed_context"] += f"**•** ``!{command.name}``\n"

                        if not help_embed_dict[page_count]["embed_context"] == "":
                            index = cog.help_command_index
                            #Add to embed.
                            if not index == None:
                                help_embed_dict[page_count]["embed_obj"].insert_field_at(index=index, name=f"__{(cog.qualified_name)}__", value=str(help_embed_dict[page_count]["embed_context"]))
                            else:
                                help_embed_dict[page_count]["embed_obj"].add_field(name=f"__{(cog.qualified_name)}__", value=str(help_embed_dict[page_count]["embed_context"]))

                            extenstion_count += 1
        
        message = await self.get_destination().send(embed=help_embed_dict[1]["embed_obj"])
        
        #Add reactions.
        for button in BUTTONS:
            await message.add_reaction(button)

        #Wait for user inputs.
        current_page = 1
        while True:
            try:
                reaction, user = await goldy_cache.client.wait_for('reaction_add', timeout=720)
                if not user == goldy_cache.client.user: #Ignores reactions from itself.
                    if reaction.message == message:
                        if reaction.emoji == BUTTONS[0]: #Backwards button.
                            if not current_page <= 1: #Stops page num from going under 1.
                                current_page -= 1
                                await goldy_help_command.embed.page.change(message, page=current_page, help_embed_dict=help_embed_dict)
                                await message.remove_reaction(reaction.emoji, user)
                            else:
                                await message.remove_reaction(reaction.emoji, user)

                        if reaction.emoji == BUTTONS[1]: #Forwards button.
                            if not current_page >= page_count:
                                current_page += 1 #Stops page num from going over max amount.
                                await goldy_help_command.embed.page.change(message, page=current_page, help_embed_dict=help_embed_dict)
                                await message.remove_reaction(reaction.emoji, user)
                            else:
                                await message.remove_reaction(reaction.emoji, user)

            except asyncio.TimeoutError:
                #Clear reactions first.
                for button in BUTTONS:
                    await message.clear_reaction(button)

                break #Stop loop


    async def send_cog_help(self, cog):
        embed = await goldy_help_command.embed.create(cog.qualified_name, 
        description="*Here's all the commands this Extenstion/Cog offers.*", 
        thumbnail_url=msg.images.other.url_1)
        
        if not cog == None:
            if servers.cogs.is_allowed(self.get_destination().guild.id, cog.cog_name):
                embed_context = ""
                for command in cog.get_commands():
                    embed_context += f"**•** ``!{command.name}`` **- {command.description}** \n"

                #Cog/Extenstion Github Repo Link
                try:
                    if not cog.github_repo == None:
                        github = f"**[[GitHub]({cog.github_repo})]**"
                        embed_context += f"\n {github}"
                except AttributeError:
                    pass

                if not embed_context == "":
                    embed.add_field(name=f"__{cog.qualified_name}'s Commands__", value=str(embed_context))
                
                #Cog/Extenstion Version
                try:
                    if not cog.version == None:
                        embed.set_footer(text=f"❤️ Ext Version: V{cog.version}")
                except AttributeError:
                    pass

                await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        description = command.description
        if description == "":
            description = "None"

        usage = command.usage
        
        command_context = f"""\n
        **❗┃ Name: **``!{command.name}``
        **📋┃ Description: *{description}***
        **🧡┃ Usage: ``{usage}``**

        **💙 From: __{command.cog.qualified_name}__**
        """
        
        if servers.cogs.is_allowed(self.get_destination().guild.id, command.cog.cog_name):
            embed = await goldy_help_command.embed.create(f"__!{command.name}__", 
            description=command_context)

            await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        '''
        #Try and correct known command errors.
        import re
        command = re.search('"(.*)"', error).group(1)
        await self.send_command_help(await self.get_command_signature(command[1:len(command)]))
        '''
        await self.get_destination().send(msg.help.command_not_found)

class core(commands.Cog, name="🧠Core"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 2

    async def get_client(self):
        return self.client

    @commands.command(hidden=True)
    async def load(self, ctx, extension):
        if await can_the_command_run(ctx, cog_name) == True:
            if await core.admin.checks.is_admin(ctx):
                try:
                    self.client.load_extension(f'cogs.{extension}')
                    await ctx.send("**💚 Loaded ``{}`` **".format(extension))
                    print_and_log(None, "💚  Loaded {}".format(extension))

                except Exception as e:
                    await ctx.send("**❤️ Failed to load ``{}``. [{}]**".format(extension, e))

    @commands.command(hidden=True)
    async def reload(self, ctx, extension):
        if await can_the_command_run(ctx, cog_name) == True:
            if await core.admin.checks.is_admin(ctx):
                try:
                    self.client.unload_extension(f'cogs.{extension}')
                    self.client.load_extension(f'cogs.{extension}')
                    await ctx.send("**💙 Reloaded ``{}`` **".format(extension))
                    print_and_log("info", "💙 Reloaded {}".format(extension))

                except Exception as e:
                    await ctx.send("**❤️ Failed to reload ``{}``. [{}]**".format(extension, e))

    @commands.command(hidden=True)
    async def unload(self, ctx, extension):
        if await can_the_command_run(ctx, cog_name) == True:
            if await core.admin.checks.is_admin(ctx):
                try:
                    if not extension == "core":
                        self.client.unload_extension(f'cogs.{extension}')
                        await ctx.send("**💛 Unloaded ``{}`` **".format(extension))
                        print ("💛  Unloaded {} **".format(extension))

                    else:
                        await ctx.send("**❤️ The core can't be unloaded.**")

                except Exception as e:
                    await ctx.send("**❤️ Failed to unload ``{}``. [{}]**".format(extension, e))



    @commands.command(hidden=True)
    async def give(self, ctx, target_member:nextcord.Member=None, option=None, arg1=None): #Command that allows admins to give any item to a member no cost.
        if await can_the_command_run(ctx, cog_name) == True:

            async def help(admin):
                embed = nextcord.Embed(title="**💚__ADMIN COMMAND: ``!give``__**", description=msg.admin.give.help_context, color=settings.GREEN)
                await admin.send(embed=embed)
                await core.admin.embed.help_sent(ctx)

            if await core.admin.checks.is_admin(ctx):

                admin = ctx.author

                if not target_member == None: #Check if target member has been entered.
                    admin = ctx.author

                    temp_ctx = ctx #Temporary storing ctx.
                    target_member_ctx = ctx #Set overwriten ctx to it's own varible.
                    target_member_ctx.author = target_member #Overwriting ctx.author to create a ctx for the target member.
                    
                    ctx = temp_ctx #Set ctx back to normal.

                    if not option == None:
                        done = False
                        exec(goldy_cache.give_cmd_additional_options)

                        if option.lower() == "money": #Give money.
                            try:
                                arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
                            except ValueError as e:
                                await help(admin)
                                return False

                            new_bal = await economy.economy.member.add(target_member_ctx, self.client, arg1)
                            embed = await core.admin.embed.create(des=(msg.admin.give.main_layout).format(admin.mention, target_member.mention, f"💷``{arg1}``"))
                            await ctx.send(embed=embed)
                            done = True

                        if option.lower() == "exp": #Give exp.
                            try:
                                arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
                            except ValueError as e:
                                await help(admin)
                                return False

                            await rank_system.member.exp.add(target_member_ctx, arg1)
                            embed = await core.admin.embed.create(des=(msg.admin.give.main_layout).format(admin.mention, target_member.mention, f"``{arg1}`` exp"))
                            await ctx.send(embed=embed)
                            done = True

                        if option.lower() == "rank": #Give rank.
                            try:
                                arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
                            except ValueError as e:
                                await help(admin)
                                return False

                            await rank_system.member.rank.add(target_member_ctx, arg1)
                            embed = await core.admin.embed.create(des=(msg.admin.give.main_layout).format(admin.mention, target_member.mention, f"``{arg1}`` rank"))
                            await ctx.send(embed=embed)
                            done = True

                        if done == False: #Give Item
                            item_data = await shop.items.find_one(ctx, option)
                            if not item_data in [False, None]:
                                item_name = await shop.items.get_name(ctx, item_data)

                                #Make item price 0
                                item_data.price = 0 
                                #Buy item
                                await shop.items.buy(target_member_ctx, self.client, item_data)
                                embed = await core.admin.embed.create(des=(msg.admin.give.main_layout).format(admin.mention, target_member.mention, item_name))
                                await ctx.send(embed=embed)

                            else:
                                await ctx.send((msg.buy.failed.no_exist).format(admin.mention))
                else:
                    await help(admin)
                    return False

    @commands.command(hidden=True)
    async def take(self, ctx, target_member:nextcord.Member=None, option=None, arg1=None): #Command that allows admins to give any item to a member no cost.
        if await can_the_command_run(ctx, cog_name) == True:

            async def help(admin):
                embed = nextcord.Embed(title="**💚__ADMIN COMMAND: ``!take``__**", description=msg.admin.take.help_context, color=settings.GREEN)
                await admin.send(embed=embed)
                await core.admin.embed.help_sent(ctx)

            if await core.admin.checks.is_admin(ctx):

                admin = ctx.author

                if not target_member == None: #Check if target member has been entered.
                    

                    temp_ctx = ctx #Temporary storing ctx.
                    target_member_ctx = ctx #Set overwriten ctx to it's own varible.
                    target_member_ctx.author = target_member #Overwriting ctx.author to create a ctx for the target member.
                    
                    ctx = temp_ctx #Set ctx back to normal.

                    if not option == None:
                        done = False
                        exec(goldy_cache.take_cmd_additional_options)

                        if option.lower() == "money": #Take money.
                            try:
                                arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
                            except ValueError as e:
                                await help(admin)
                                return False

                            new_bal = await economy.economy.member.subtract(target_member_ctx, self.client, arg1)
                            embed = await core.admin.embed.create(des=(msg.admin.take.main_layout).format(admin.mention, f"💷``{arg1}``", target_member.mention))
                            await ctx.send(embed=embed)
                            done = True

                        if option.lower() == "exp": #Take exp.
                            try:
                                arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
                            except ValueError as e:
                                await help(admin)
                                return False

                            await rank_system.member.exp.subtract(target_member_ctx, arg1) #This is not working OwO!
                            embed = await core.admin.embed.create(des=(msg.admin.take.main_layout).format(admin.mention, f"``{arg1}`` exp", target_member.mention))
                            await ctx.send(embed=embed)
                            done = True
                        
                        '''
                        if option.lower() == "rank": #Take rank.
                            try:
                                arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
                            except ValueError as e:
                                await help(admin)
                                return False

                            await rank_system.member.rank.subtract(target_member_ctx, arg1)
                            await ctx.send((msg.admin.give.main_layout).format(admin.mention, target_member.mention, f"``{arg1}`` rank"))
                            done = True
                        '''

                        if done == False: #Take Item
                            item_data = await shop.items.find_one(ctx, option)
                            if not item_data == False:
                                item_name = await shop.items.get_name(ctx, item_data)

                                #Make item price 0
                                item_data.price = 0
                                #Buy item
                                await shop.items.sell(target_member_ctx, self.client, item_data)
                                embed = await core.admin.embed.create(des=(msg.admin.take.main_layout).format(admin.mention, item_name, target_member.mention))
                                await ctx.send(embed=embed)

                            else:
                                await ctx.send((msg.buy.failed.no_exist).format(admin.mention))
                else:
                    await help(admin)
                    return False

    @commands.command(aliases=["read-cache"], hidden=True)
    async def read_cache(self, ctx): #A Command that sends goldy bot's cache.
        if await can_the_command_run(ctx, cog_name) == True:

            if await core.admin.checks.is_admin(ctx):
                from src.goldy_cache import main_cache_object
                des = f"```{main_cache_object}```"

                if not len(des) > 2000:
                    embed = nextcord.Embed(title=msg.admin.read_cache.embed.title, 
                    description=des)
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(title=msg.admin.read_cache.error.too_big_embed.title, 
                    description=msg.admin.read_cache.error.too_big_embed.des)
                    await ctx.send(embed=embed)

    @read_cache.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.read_cache")

    class admin():

        class checks():
            @staticmethod
            async def is_admin(ctx):
                if ctx.author.id in settings.admin_users: #Checks if ctx.author is a admin.
                    return True
                else:
                    return False        
        
        class embed():
            @staticmethod
            async def create(des):
                embed = nextcord.Embed(title="**💚__ADMIN COMMAND__**", description=des)
                return embed

            @staticmethod
            async def help_sent(ctx):
                embed=nextcord.Embed(title="**__💛 Help Sent To Dm's__**", description=f"**{ctx.author.mention}, i've sent help to your dm's.**", color=settings.YELLOW)
                message = await ctx.send(embed=embed)
                await asyncio.sleep(2)
                await message.delete()
                await ctx.message.delete()
                
    @commands.command()
    async def test(self, ctx): #A command we use for testing. (Delete this command if you wish.)
        if await can_the_command_run(ctx, cog_name) == True:
            if await core.admin.checks.is_admin(ctx):
                await ctx.send("*done*")

    @test.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.test")
            

def setup(client):
    client.add_cog(core(client))