import asyncio
import nextcord

Interaction = nextcord.Interaction
MISSING = nextcord.utils.MISSING

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
        #TODO: #27 'interaction.message' is always none.
        return self.interaction.user

    async def send(self, text=None, embed=MISSING):
        await self.interaction.response.send_message(text, embed=embed)