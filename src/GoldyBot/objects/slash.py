import asyncio
from typing import Any
import nextcord

Interaction = nextcord.Interaction
MISSING: Any = nextcord.utils.MISSING

loop = asyncio.get_event_loop()

class InteractionToCtx():
    """This Goldy Bot class is used to convert interactions to ctx."""
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    @property
    def guild(self) -> Interaction.guild:
        return self.interaction.guild

    @property
    def author(self):
        return self.interaction.user

    @property
    def channel(self):
        return self.interaction.channel

    async def send(self, text:str=None, **kwargs):
        if not text == None:
            await self.interaction.send(text)
        else:
            await self.interaction.send(**kwargs)
        
        return Message(self.interaction)

    async def send_modal(self, modal:nextcord.ui.Modal):
        """Sends modal."""
        await self.interaction.response.send_modal(modal)

        return Message(self.interaction)

class Message():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def delete(self, delay=None):
        await self.interaction.delete_original_message(delay=delay)

    async def edit(self, **args):
        #TODO: #29 Don't forget to add text to this.
        await self.interaction.edit_original_message(**args)