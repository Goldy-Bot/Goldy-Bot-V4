import GoldyBot

async def yes_or_no(ctx:GoldyBot.InteractionToCtx, names:tuple=("Yes", "No!")):
    """
    Goldy Bot's yes or no button view. (Only the command author can interact with this!)
    """

    class yes_or_no_button_view(GoldyBot.nextcord.ui.View):
        def __init__(self, author:GoldyBot.Member, auto_delete:bool):
            super().__init__()
            self.value = None
            self.response_message:GoldyBot.nextcord.PartialInteractionMessage = None

            self.author = author
            self.auto_delete = auto_delete

        @GoldyBot.nextcord.ui.button(label=names[0], style=GoldyBot.nextcord.ButtonStyle.green)
        async def yes(self, button: GoldyBot.nextcord.ui.Button, interaction: GoldyBot.nextcord.Interaction):
            if self.author.member.id == interaction.user.id:
                self.response_message = await interaction.response.send_message("**Okay! 💛**", ephemeral=True)
                self.value = True
                self.stop()

        @GoldyBot.nextcord.ui.button(label=names[1], style=GoldyBot.nextcord.ButtonStyle.red)
        async def no(self, button: GoldyBot.nextcord.ui.Button, interaction: GoldyBot.nextcord.Interaction):
            if self.author.member.id == interaction.user.id:
                self.response_message = await interaction.response.send_message("**Alright, cancelled! 💚**", ephemeral=True)
                self.value = False
                self.stop()

    return yes_or_no_button_view(GoldyBot.Member(ctx), auto_delete)