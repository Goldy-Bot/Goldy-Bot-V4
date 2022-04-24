import GoldyBot
from . import _mention_, _send_

mention = _mention_.mention
send = _send_.send

def what_command_type(ctx):
    """Tells you whether this command is a slash command or a normal command."""
    if isinstance(ctx, GoldyBot.utility.goldy.slash.InteractionToCtx):
        return "slash"
    else:
        return "normal"