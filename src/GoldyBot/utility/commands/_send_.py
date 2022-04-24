import nextcord
import GoldyBot

MISSING = nextcord.utils.MISSING

async def send(ctx, text=MISSING, embed=MISSING):
    """Goldy Bot method for sending messages."""
    
    message:GoldyBot.utility.goldy.slash.Message = await ctx.send(text, embed=embed)
    return message