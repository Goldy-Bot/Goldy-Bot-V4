import nextcord

def mention(member):
    """Fixes slash commands compatibility when mentioning a member the normal way."""

    if isinstance(member, nextcord.Member):
        return member.mention
    else:
        return member