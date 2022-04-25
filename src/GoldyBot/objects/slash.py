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

    async def send(self, stickers=None, nonce=None, reference=None, mention_author=None, **args):
        await self.interaction.send(**args)
        
        return Message(self.interaction)


class Message():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def delete(self):
        await self.interaction.delete_original_message()

    async def edit(self, **args):
        #TODO: #29 Don't forget to add text to this.
        await self.interaction.edit_original_message(**args)