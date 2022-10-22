"""
💙 Goldy Bot V4 - BIG and Modern rewrite of Goldy Bot V3

Copyright (C) 2022 - Dev Goldy

----------------------------
.. include:: ../docs_template/README.md
"""

import sys
import nextcord
import asyncio
import nest_asyncio

from .objects import *
from .errors import *

from . import database
from . import files, paths, logging, goldy, cache, token, settings, config, info, modules, system, assets
from . import internal_modules, ext, utility, objects

from nextcord.ext.commands import Context

# Functions
log = logging.print_and_log
"""Shortcut of ``GoldyBot.logging.log``"""

# Function Decorators
command = ext.commands.command
"""Shortcut of object from ``GoldyBot.ext.commands``"""
cmd = command
"""Alias of object from ``GoldyBot.ext.commands``"""

# Class Inheritors
Extension = ext.extensions.Extension
"""Shortcut of object from ``GoldyBot.ext.extensions``"""

setattr(sys.modules[__name__], 'Extenstion', Extension) # Stops Goldy Bot extensions made before the dev21 update from crashing.

# Classes
Goldy = goldy.Goldy
"""Shortcut of object from ``GoldyBot.goldy``"""
Database = database.Database
"""Shortcut of ``GoldyBot.database.Database``"""
Embed = utility.goldy.embed.Embed
"""Shortcut of object from ``GoldyBot.utility.goldy.embed``"""
GuildEvent = utility.guild_events.GuildEvent
"""Shortcut of object from ``GoldyBot.utility.guild_events.GuildEvent``"""
File = files.File
"""Shortcut of object from ``GoldyBot.files.File``"""
WebFile = files.WebFile
"""Shortcut of object from ``GoldyBot.files.WebFile``"""

# Async Loop
async_loop = asyncio.get_event_loop()
"""
Goldy Bot's async loop. You can use this to run async methods in non async functions.
Like this ``async_loop.run_until_complete(async_function())``
"""
nest_asyncio.apply(async_loop)

# Colours
Colours = utility.goldy.colours.Colours
"""Shortcut of object from ``GoldyBot.utility.goldy.colours``"""

Colors = utility.goldy.colours.Colors
"""Alias of ``GoldyBot.Colours``"""

# Stops Goldy Bot extensions made before the dev24 update from crashing. ('Colours' used to be all lowercase in previous versions.)
setattr(sys.modules[__name__], 'colours', Colours) 
setattr(sys.modules[__name__], 'colors', Colors) 

# Hearts
Hearts = utility.goldy.hearts.Hearts
"""Shortcut of object from ``GoldyBot.utility.goldy.hearts``"""

# Goldy Bot Currencies
Currencies = utility.goldy.currencies.Currencies
"""Shortcut of object from ``GoldyBot.utility.goldy.currencies``"""