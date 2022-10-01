import GoldyBot
from . import _mention_, _send_, _icon_, _defer_

mention = _mention_.mention
""""""
send = _send_.send
""""""
defer = _defer_.defer
""""""
get_member_pfp = _icon_.get_member_pfp
""""""

# Aliases
#--------------------------
think = _defer_.defer
"""An alias of ``GoldyBot.utility.commands.defer``."""

def what_command_type(ctx):
    """Tells you whether this command is a slash command or a normal command."""
    if isinstance(ctx, GoldyBot.objects.slash.InteractionToCtx):
        return "slash"
        
    if isinstance(ctx, GoldyBot.objects.member.Member):
        if isinstance(ctx.ctx, GoldyBot.objects.slash.InteractionToCtx):
            return "slash"
        else:
            return "normal"
    else:
        return "normal"