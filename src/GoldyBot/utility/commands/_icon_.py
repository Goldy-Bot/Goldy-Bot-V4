import nextcord
import GoldyBot

MISSING = nextcord.utils.MISSING

async def get_member_pfp(member:nextcord.Member) -> str:
    """Goldy Bot method for grabbing member profile picture url."""
    
    if not member.avatar == None:
        return member.avatar.url
    else:
        return GoldyBot.assets.NO_PFP_IMAGE