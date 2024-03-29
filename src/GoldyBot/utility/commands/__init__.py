import GoldyBot
from . import _mention_, _send_, _icon_, _defer_, _send_modal_

mention = _mention_.mention
""""""
send = _send_.send
""""""
defer = _defer_.defer
""""""
get_member_pfp = _icon_.get_member_pfp
""""""
send_modal = _send_modal_.send_modal
""""""

# Aliases
#--------------------------
think = _defer_.defer
"""An alias of ``GoldyBot.utility.commands.defer``."""

def what_command_type(ctx):
    """Tells you whether this command is a slash command or a normal command."""
    if isinstance(ctx, GoldyBot.objects.slash.InteractionToCtx):
        return "slash"

    elif isinstance(ctx, GoldyBot.nextcord.Interaction):
        return "slash"
        
    elif isinstance(ctx, GoldyBot.objects.member.Member):
        if isinstance(ctx.ctx, GoldyBot.objects.slash.InteractionToCtx):
            return "slash"
        else:
            return "normal"
        
    elif isinstance(ctx, GoldyBot.objects.channel.Channel):
        if isinstance(ctx.ctx, GoldyBot.objects.slash.InteractionToCtx):
            return "slash"
        else:
            return "normal"
        
    else:
        return "normal"