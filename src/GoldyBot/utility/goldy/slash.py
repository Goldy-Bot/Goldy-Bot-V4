from nextcord import Interaction

class InteractionToCtx():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def send(self, text=None, embed=None):
        await self.interaction.response.send_message(text, embed=embed)