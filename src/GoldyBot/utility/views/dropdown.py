
import collections
import GoldyBot
from typing import Callable, List

MODULE_NAME = "DROPDOWN"

async def dropdown(ctx:GoldyBot.InteractionToCtx, options:List[GoldyBot.nextcord.SelectOption], placeholder_msg="🎯 Pick an Option", warning=True, warning_msg="🛑 Are you sure!", callback:Callable=None):
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

            super().__init__(
                placeholder=placeholder_msg,
                min_values=1,
                max_values=1,
                options=options,
            )

        async def callback(self, interaction: GoldyBot.nextcord.Interaction):
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

                    GoldyBot.logging.log(f"[{MODULE_NAME}] Dropdown view for '{self.author.name}' executed it's function '{self.callback_.__name__}'!")

    class DropdownView(GoldyBot.nextcord.ui.View):
        def __init__(self, author:GoldyBot.Member, options:List[GoldyBot.nextcord.SelectOption], placeholder_msg:str, warning:bool, warning_msg:str, callback:Callable):
            super().__init__()

            self.add_item(Dropdown(author, options, placeholder_msg, warning, warning_msg, callback))

    return DropdownView(GoldyBot.Member(ctx), options, placeholder_msg, warning, warning_msg, callback)