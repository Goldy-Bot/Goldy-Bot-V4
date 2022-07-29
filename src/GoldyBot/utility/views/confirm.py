import GoldyBot

async def yes_or_no(ctx:GoldyBot.InteractionToCtx, names:tuple=("Yes", "No!")):

    class yes_or_no_button_view(GoldyBot.nextcord.ui.View):
        def __init__(self, author:GoldyBot.Member):
            super().__init__()
            self.value = None

            self.author = author

        @GoldyBot.nextcord.ui.button(label=names[0], style=GoldyBot.nextcord.ButtonStyle.green)
        async def yes(self, button: GoldyBot.nextcord.ui.Button, interaction: GoldyBot.nextcord.Interaction):
            if self.author.member == interaction.user:
                await interaction.response.send_message("**Okay! 💛**", ephemeral=True)
                self.value = True
                self.stop()

        @GoldyBot.nextcord.ui.button(label=names[1], style=GoldyBot.nextcord.ButtonStyle.red)
        async def no(self, button: GoldyBot.nextcord.ui.Button, interaction: GoldyBot.nextcord.Interaction):
            if self.author.member == interaction.user:
                await interaction.response.send_message("**Alright, cancelled! 💚**", ephemeral=True)
                self.value = False
                self.stop()

    return yes_or_no_button_view(GoldyBot.Member(ctx))