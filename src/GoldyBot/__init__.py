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

from . import database
from . import files, paths, logging, goldy, cache, token, settings, config, info, modules, system, errors, assets
from . import internal_modules, ext, utility, objects

# Functions
log = logging.print_and_log
"""Alias of ``GoldyBot.logging.log``"""

# Function Decorators
command = ext.commands.command
"""Alias of object from ``GoldyBot.ext.commands``"""
cmd = command
"""Alias of object from ``GoldyBot.ext.commands``"""

# Class Inheritors
Extension = ext.extensions.Extension
"""Alias of object from ``GoldyBot.ext.extensions``"""

setattr(sys.modules[__name__], 'Extenstion', Extension) # Stops Goldy Bot extensions made before the dev21 update from crashing.

# Classes
Goldy = goldy.Goldy
"""Alias of object from ``GoldyBot.goldy``"""
Database = database.Database
"""Alias of ``GoldyBot.database.Database``"""
Embed = utility.goldy.embed.Embed
"""Alias of object from ``GoldyBot.utility.goldy.embed``"""

# Async Loop
async_loop = asyncio.get_event_loop()
"""
Goldy Bot's async loop. You can use this to run async methods in non async functions.
Like this ``async_loop.run_until_complete(async_function())``
"""
nest_asyncio.apply(async_loop)

# Colours
colours = utility.goldy.colours.Colours
"""Alias of object from ``GoldyBot.utility.goldy.colours``"""

colors = utility.goldy.colours.Colors
"""Alias of ``GoldyBot.colours``"""