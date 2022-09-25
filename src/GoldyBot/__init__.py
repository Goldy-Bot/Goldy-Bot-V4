"""
💙 Goldy Bot V4 - BIG and Modern rewrite of Goldy Bot V3

Copyright (C) 2022 - Dev Goldy

----------------------------
[![Powered by Nextcord](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Nextcord-0d1620?logo=nextcord)](https://github.com/nextcord/nextcord "Powered by Nextcord Python API Wrapper")
[![Pypi Badge](https://img.shields.io/pypi/v/GoldyBot?style=flat)](https://pypi.org/project/GoldyBot/ "We're on pypi!")
[![Python Badge](https://img.shields.io/pypi/pyversions/GoldyBot?style=flat)](https://pypi.org/project/GoldyBot/ "Supported python versions.")
[![Docs Badge](https://img.shields.io/static/v1?label=docs&message=Available&color=light-green)](https://goldybot.devgoldy.me/)

<img src="https://raw.githubusercontent.com/Goldy-Bot/Goldy-Bot-V4/main/assets/banner_1.png" width="100%"/>
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
File = GoldyBot.files.File
"""Shortcut of object from ``GoldyBot.files.File``"""
WebFile = GoldyBot.files.WebFile
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
"""Alias of ``GoldyBot.colours``"""

# Stops Goldy Bot extensions made before the dev24 update from crashing. ('Colours' used to be all lowercase in previous versions.)
setattr(sys.modules[__name__], 'colours', Colours) 
setattr(sys.modules[__name__], 'colors', Colors) 

# Hearts
Hearts = utility.goldy.hearts.Hearts
"""Shortcut of object from ``GoldyBot.utility.goldy.hearts``"""

# Goldy Bot Currencies
Currencies = utility.goldy.currencies.Currencies
"""Shortcut of object from ``GoldyBot.utility.goldy.currencies``"""