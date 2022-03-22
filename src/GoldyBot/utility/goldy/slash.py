from nextcord import Interaction

class InteractionToCtx():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def send(self, text):
        await self.interaction.response.send_message(text)