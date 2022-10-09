import GoldyBot
from typing import Callable, List

MODULE_NAME = __name__.upper()

def normal_form(title:str, items:List[GoldyBot.nextcord.ui.Item], callback:Callable, author:GoldyBot.Member, timeout=None, 
        warning=False, warning_msg="🛑 Are you sure!") -> GoldyBot.nextcord.ui.Modal:
    """
    Goldy Bot's normal form modal. (Only the command author can interact with interactions from this form!)
    """

    class NormalForm(GoldyBot.nextcord.ui.Modal):
        def __init__(self):
            super().__init__(title, timeout=timeout, auto_defer=True)

            for item in items:
                self.add_item(item)

        async def callback(self, interaction: GoldyBot.nextcord.Interaction) -> None:
            view = await GoldyBot.utility.views.confirm.yes_or_no(interaction)
            
            if warning:
                message = await interaction.send(warning_msg, view=view)
                await view.wait()
                await message.delete()
            else:
                view.value = True

            if view.value == True:
                if not callback == None:
                    await callback((lambda x: [item_.value for item_ in x])(items), interaction) # Execute callback

                    GoldyBot.logging.log(f"[{MODULE_NAME}] Normal form modal for '{author.name}' executed it's function '{callback.__name__}'!")
    
    return NormalForm()