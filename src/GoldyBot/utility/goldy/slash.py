import nextcord

Interaction = nextcord.Interaction
MISSING = nextcord.utils.MISSING

class InteractionToCtx():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    @property
    def guild(self) -> Interaction.guild:
        return self.interaction.guild

    @property
    def author(self):
        #TODO: Finish working on this.
        return self.interaction.message.author

    async def send(self, text=None, embed=MISSING):
        await self.interaction.response.send_message(text, embed=embed)