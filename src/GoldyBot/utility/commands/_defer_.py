import nextcord

async def defer(ctx:nextcord.Interaction) -> None:
    """Warns Goldy Bot that this interaction may take longer than usual. This also informs the user that goldy is currently thinking. (ONLY WORKS WITH SLASH COMMAND!)"""
    interaction = ctx
    await interaction.response.defer()