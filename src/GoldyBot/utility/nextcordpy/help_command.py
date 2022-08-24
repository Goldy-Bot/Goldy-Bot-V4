import GoldyBot
import nextcord
from nextcord.ext import commands

"""

class goldy_help_command(commands.HelpCommand):
    def __init__(self):
        super().__init__()

        self.config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

    class embed():
        @staticmethod
        async def create(help_type, description=None, thumbnail_url=None, page_num=None):
            if description == None:
                description = GoldyBot.utility.msgs.help.Embed.des

            embed = nextcord.Embed(title=(GoldyBot.utility.msgs.help.Embed.title).format(help_type), description=description, color=settings.WHITE)
            if not thumbnail_url == None:
                embed.set_thumbnail(url=thumbnail_url)
            if not page_num == None:
                embed.set_footer(text=GoldyBot.utility.msgs.footer.type_2 + f" [PAGE {page_num}]")
            return embed

        class page():
            @staticmethod
            async def change(msg_obj, page, help_embed_dict): #Method that changes the help command page.
                await msg_obj.edit(embed=help_embed_dict[page]["embed_obj"])
                pass

    async def send_bot_help(self, mapping):
        bot_icon = GoldyBot.cache.main_cache_dict["client"].user.display_avatar.url
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
                if extenstion_count >= self.config.read("max_extenstions")*page_count:
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
        
        command_context = f"\n
        **❗┃ Name: **``!{command.name}``
        **📋┃ Description: *{description}***
        **🧡┃ Usage: ``{usage}``**

        **💙 From: __{command.cog.qualified_name}__**
        "
        
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
        await self.get_destination().send(GoldyBot.utility.msgs.help.command_not_found)

"""