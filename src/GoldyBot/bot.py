import asyncio
import nextcord
from nextcord.ext import commands, tasks
import os
import time
from platform import python_version

import GoldyBot

MODULE_NAME = "GOLDY CORE"

def start():
    """Start the nextcord bot."""

    asyncio.set_event_loop(GoldyBot.async_loop)
    
    TOKEN = GoldyBot.token.get()
    DATABASE_TOKEN = GoldyBot.token.get_database()
    intents = nextcord.Intents()

    # Discord Bot
    client = commands.Bot(command_prefix = GoldyBot.utility.nextcordpy.prefix.get_prefix, 
    case_insensitive=True, intents=intents.all(), help_command=None)

    # Caching client object.
    GoldyBot.cache.main_cache_dict["client"] = client

    # Initializing Stuff
    #----------------------
    GoldyBot.database.Database(DATABASE_TOKEN) # Initializing goldy bot database connection.

    @client.event
    async def on_ready():
        # Goldy Setup.
        await GoldyBot.Goldy().setup(client)

        await GoldyBot.utility.presence.change(f"{GoldyBot.info.name}", status=GoldyBot.nextcord.Status.online)

        GoldyBot.log("info_2", f"[{MODULE_NAME}] [BOT READY]")

    # Initializing Loops
    #-------------------------
    @tasks.loop(seconds=1) # Rate Limited Warning.
    async def rate_limit_warning():
        if client.is_ws_ratelimited() == True:
            GoldyBot.logging.log("warn", "We're being rate limited!")

    rate_limit_warning.start()

    @tasks.loop(seconds=1) # Stop Bot Loop
    async def stop_bot():
        if GoldyBot.cache.main_cache_dict["bot_stop"]:
            await client.close()

    stop_bot.start()

    # Goldy Setup.
    #---------------
    GoldyBot.async_loop.create_task(GoldyBot.Goldy().setup(client))

    # Core commands
    #----------------
    @GoldyBot.command(slash_cmd_only=True, required_roles=["bot_dev", "bot_admin"])
    async def goldy(ctx):
        command_msg = GoldyBot.utility.msgs.goldy
        system = GoldyBot.system.System()
        hearts = GoldyBot.Hearts

        version = GoldyBot.info.bot_version
        nextcord_version = nextcord.__version__
        python_ver = python_version()
        platform = system.os

        dev_goldy = GoldyBot.Member(ctx, member_id=332592361307897856) # Hard coded my discord id LMAO.
        dev_goldy_mention = GoldyBot.utility.commands.mention(dev_goldy)

        embed = GoldyBot.utility.goldy.embed.Embed(title=command_msg.Embed.title)
        embed.color = GoldyBot.utility.goldy.colours.AKI_BLUE
        embed.set_thumbnail(url=GoldyBot.utility.goldy.get_pfp())

        embed.description = command_msg.Embed.des.format(version, nextcord_version, python_ver, round(client.latency * 1000), 
        platform, f"{system.cpu:.1f}", system.ram, system.disk, hearts.YELLOW, dev_goldy_mention)

        message = await GoldyBot.utility.commands.send(ctx, embed=embed)

        t_end = time.time() + 15
        while time.time() < t_end:
            heart = hearts.random()
            embed.description = command_msg.Embed.des.format(version, nextcord_version, python_ver, round(client.latency * 1000), platform, f"{system.cpu:.1f}", system.ram, system.disk, heart, dev_goldy_mention)
            await message.edit(embed=embed)

            await asyncio.sleep(0.5)



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
        # I just don't want it to stop the whole bot so I'm passing this exception.
        pass

    # Run Bot
    #----------
    try:
        GoldyBot.async_loop.run_until_complete(client.start(TOKEN))
    except Exception as e: # Error Handling
        GoldyBot.logging.log("error", e); GoldyBot.Goldy().stop(e)
