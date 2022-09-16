import nextcord
import GoldyBot

MISSING = nextcord.utils.MISSING
EMPTY_DISCORD_STRING = "**‎ **"

async def send(ctx, text=None, embed=None, tts=None, 
    embeds=None, file=None, files=None, stickers=None, delete_after=None, nonce=None, allowed_mentions=None, 
    reference=None, mention_author=None, view=None, private=False) -> nextcord.Message:
    """Goldy Bot method for sending messages."""
    message:GoldyBot.objects.slash.Message

    if GoldyBot.utility.commands.what_command_type(ctx) == "slash":
        if not embed == None:
            if not file == None:
                if not text == None:
                    message = await ctx.send(content=text, embed=embed, file=file, delete_after=delete_after, 
                    allowed_mentions=allowed_mentions, ephemeral=private)
                    return message
                else: # Without context.
                    message = await ctx.send(embed=embed, file=file, delete_after=delete_after, 
                    allowed_mentions=allowed_mentions, ephemeral=private)
                    return message
            
            if not files == None:
                message = await ctx.send(content=text, embed=embed, files=files, delete_after=delete_after, 
                allowed_mentions=allowed_mentions, ephemeral=private, view=view)
                return message

            if not view == None:
                message = await ctx.send(content=text, embed=embed, 
                delete_after=delete_after, allowed_mentions=allowed_mentions, 
                ephemeral=private, view=view)
                return message

            message = await ctx.send(content=text, embed=embed, 
            delete_after=delete_after, allowed_mentions=allowed_mentions, 
            ephemeral=private)
            return message

        if not embeds == None:
            if not file == None:
                message = await ctx.send(content=text, embeds=embeds, file=file, delete_after=delete_after, 
                allowed_mentions=allowed_mentions, ephemeral=private, view=view)
                return message

            if not files == None:
                message = await ctx.send(content=text, embeds=embeds, files=files, delete_after=delete_after, 
                allowed_mentions=allowed_mentions, ephemeral=private, view=view)
                return message

            if not view == None:
                message = await ctx.send(content=text, embeds=embeds, 
                delete_after=delete_after, allowed_mentions=allowed_mentions, 
                ephemeral=private, view=view)
                return message

            message = await ctx.send(content=text, embeds=embeds, delete_after=delete_after, 
            allowed_mentions=allowed_mentions, ephemeral=private)
            return message

        if not file == None:
            message = await ctx.send(content=text, file=file, 
            delete_after=delete_after, allowed_mentions=allowed_mentions, 
            ephemeral=private)
            return message
        
        if not files == None:
            message = await ctx.send(content=text, files=files, 
            delete_after=delete_after, allowed_mentions=allowed_mentions, 
            ephemeral=private)
            return message

        if not view == None:
            message = await ctx.send(content=text, delete_after=delete_after, 
            allowed_mentions=allowed_mentions, 
            ephemeral=private, view=view)
            return message

        message = await ctx.send(content=text, delete_after=delete_after, 
        allowed_mentions=allowed_mentions, ephemeral=private)
        return message

    if GoldyBot.utility.commands.what_command_type(ctx) == "normal":
        message = await ctx.send(text, embed=embed, tts=tts, embeds=embeds, file=file, files=files, 
        stickers=stickers, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions, 
        reference=reference, mention_author=mention_author, view=view)
        return message
    