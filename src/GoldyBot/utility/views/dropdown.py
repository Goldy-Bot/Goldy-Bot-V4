import GoldyBot
from typing import Callable, List

MODULE_NAME = "DROPDOWN"

async def dropdown(ctx:GoldyBot.InteractionToCtx, options:List[GoldyBot.nextcord.SelectOption], min_max_value:tuple=(1, 1) , placeholder_msg="🎯 Pick an Option", warning=True, warning_msg="🛑 Are you sure!", callback:Callable=None):
    """
    Goldy Bot's dropdown view. (Only the command author can interact with this!)
    """

    class Dropdown(GoldyBot.nextcord.ui.Select):
        def __init__(self, author:GoldyBot.Member, options:List[GoldyBot.nextcord.SelectOption], placeholder_msg:str, warning:bool, warning_msg:str, callback:Callable):
            self.author = author
            self.warning = warning
            self.warning_msg = warning_msg
            self.callback_ = callback

            self.options_values = {}

            # Embeds
            self.your_not_author_embed = GoldyBot.Embed(
                title="❌ Author Only!",
                description="***❌{}, this view can only be interacted by the command author.***",
                colour=GoldyBot.Colours.RED
            )

            super().__init__(
                placeholder=placeholder_msg,
                min_values=min_max_value[0],
                max_values=min_max_value[1],
                options=options,
            )

        async def callback(self, interaction: GoldyBot.nextcord.Interaction):
            if self.author.member.id == interaction.user.id: # Is this the author.
                view = await GoldyBot.utility.views.confirm.yes_or_no(interaction)
                
                if self.warning:
                    message = await interaction.send(self.warning_msg, view=view)
                    await view.wait()
                    await message.delete()
                else:
                    view.value = True

                if view.value == True:
                    if not self.callback_ == None:
                        await self.callback_(self.values) # Execute callback

                        await interaction.delete_original_message()

                        GoldyBot.logging.log(f"[{MODULE_NAME}] Dropdown view for '{self.author.name}' executed it's function '{self.callback_.__name__}'!")

            else:
                # View not for you message.
                embed_thumbnail = GoldyBot.File(GoldyBot.paths.ASSETS + "/angry_mirai_kuriyama.gif")

                your_not_author_embed = self.your_not_author_embed.copy()
                your_not_author_embed.description = self.your_not_author_embed.description.format(interaction.user.mention)
                your_not_author_embed.set_thumbnail("attachment://image.gif")

                message = await interaction.send(embed=your_not_author_embed, file=GoldyBot.nextcord.File(embed_thumbnail.file_path, filename="image.gif"))
                await message.delete(delay=6)

                #raise GoldyBot.errors.YourNotAuthor(f"[{MODULE_NAME}] '{interaction.user.name}' tried interacting with a command author only view.")

    class DropdownView(GoldyBot.nextcord.ui.View):
        def __init__(self, author:GoldyBot.Member, options:List[GoldyBot.nextcord.SelectOption], placeholder_msg:str, warning:bool, warning_msg:str, callback:Callable):
            super().__init__()

            self.add_item(Dropdown(author, options, placeholder_msg, warning, warning_msg, callback))

    return DropdownView(GoldyBot.Member(ctx), options, placeholder_msg, warning, warning_msg, callback)