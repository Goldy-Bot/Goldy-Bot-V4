import GoldyBot

async def send_modal(ctx:GoldyBot.InteractionToCtx, modal:GoldyBot.nextcord.ui.Modal) -> GoldyBot.objects.slash.Message:
    return await ctx.send_modal(modal)