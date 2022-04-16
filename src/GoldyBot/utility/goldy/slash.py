from nextcord import Interaction
import nextcord

class InteractionToCtx():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def send(self, text=None):
        #TODO: #13 Fix embed issue!
        await self.interaction.response.send_message(text)