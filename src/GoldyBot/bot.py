import asyncio
import random
import sys
import nextcord
import nextcord.ext as nextcord_ext
from nextcord import Interaction
from nextcord.ext import commands
import os
import time

import GoldyBot

MODULE_NAME = "GOLDY CORE"

def start():
    """Start the nextcord bot."""
    
    TOKEN = GoldyBot.token.get()
    DATABASE_TOKEN = GoldyBot.token.get_database()
    intents = nextcord.Intents()
    loop = asyncio.get_event_loop()

    # Discord Bot
    client = commands.Bot(command_prefix = GoldyBot.utility.nextcordpy.prefix.get_prefix, 
    case_insensitive=True, intents=intents.all(), help_command=None)

    # Caching client object.
    GoldyBot.cache.main_cache_dict["client"] = client

    # Initializing Stuff
    #----------------------
    database = GoldyBot.database.Database(DATABASE_TOKEN) # Initializing goldy bot database connection.

    @client.event
    async def on_ready():
        # Goldy Setup.
        await GoldyBot.Goldy().setup(client)

        await GoldyBot.utility.presence.change(f"{GoldyBot.info.name}", status=GoldyBot.nextcord.Status.online)

        GoldyBot.log("info_2", f"[{MODULE_NAME}] [BOT READY]")

    # Goldy Setup.
    #---------------
    GoldyBot.async_loop.create_task(GoldyBot.Goldy().setup(client))

    # Core commands
    #----------------
    @GoldyBot.command(slash_cmd_only=True, required_roles=["bot_dev"])
    async def goldy(ctx):
        command_msg = GoldyBot.utility.msgs.goldy
        system = GoldyBot.system.System()
        hearts = ["🖤", "🤍", "💙", "💚", "💜", "🤎", "🧡", "❤️", "💛"]

        version = GoldyBot.info.bot_version
        nextcord_version = nextcord.__version__
        platform = system.os

        dev_goldy = GoldyBot.Member(ctx, member_id=332592361307897856)
        dev_goldy_mention = GoldyBot.utility.commands.mention(dev_goldy)

        embed = GoldyBot.utility.goldy.embed.Embed(title=command_msg.Embed.title)
        embed.color = GoldyBot.utility.goldy.colours.AKI_BLUE
        embed.set_thumbnail(url=GoldyBot.utility.goldy.get_pfp())

        embed.description = command_msg.Embed.des.format(version, nextcord_version, round(client.latency * 1000), 
        platform, system.cpu, system.ram, system.disk, hearts[8], dev_goldy_mention)

        message = await GoldyBot.utility.commands.send(ctx, embed=embed)

        t_end = time.time() + 15
        while time.time() < t_end:
            heart = random.choice(hearts)
            embed.description = command_msg.Embed.des.format(version, nextcord_version, round(client.latency * 1000), platform, system.cpu, system.ram, system.disk, heart, dev_goldy_mention)
            await message.edit(embed=embed)

            await asyncio.sleep(0.5)

    @GoldyBot.command(slash_cmd_only=True, required_roles=["bot_dev"], help_des="Dev command to shutdown Goldy Bot.", slash_options= {
        "reason" : GoldyBot.nextcord.SlashOption()
    })
    async def stop(ctx:GoldyBot.objects.InteractionToCtx, reason="A user ran the !stop command."):
        await ctx.send("*Shutting down...*")
        GoldyBot.Goldy().stop(reason)

    try:
        # Load internal modules.
        #----------------------------
        for module in os.listdir(GoldyBot.paths.INTERNAL_COGS_V4):
            if not module in ["__init__.py", "__pycache__"]:
                GoldyBot.modules.Module(module_file_name=module).load()

        # Load external modules.
        #----------------------------
        for module in os.listdir(GoldyBot.paths.MODULES):
            if not module in ["__pycache__", ".git"]:
                GoldyBot.modules.Module(module_file_name=module).load()

    except GoldyBot.errors.ModuleFailedToLoad:
        # I just don't want it to stop the whole bot.
        pass

    # Run Bot
    #----------
    try:
        client.run(TOKEN)
    except Exception as e: # Error Handling
        GoldyBot.logging.log("error", e); GoldyBot.Goldy().stop(e)