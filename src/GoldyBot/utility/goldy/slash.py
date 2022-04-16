import nextcord

Interaction = nextcord.Interaction
MISSING = nextcord.utils.MISSING

class InteractionToCtx():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def send(self, text=None, embed=MISSING):
        #TODO: #13 Fix embed issue!
        await self.interaction.response.send_message(text, embed=embed)