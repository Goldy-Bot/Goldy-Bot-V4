"""
💙 Goldy Bot V4

Copyright (C) 2022 - Dev Goldy
"""

import nextcord
import asyncio

from .objects import *

from .database import database
from . import files, paths, logging, goldy, cache, token, settings, config, info, modules, system, errors, assets
from . import internal_modules, ext, utility, objects

# Functions
log = logging.print_and_log
""""""

# Function Decorators
command = ext.commands.command
""""""
cmd = command
""""""

# Class Inheritors
Extenstion = ext.extenstions.Extenstion
""""""

# Classes
Goldy = goldy.Goldy
""""""
Database = database.Database
""""""

# Async Loop
async_loop = asyncio.get_event_loop()
"""
Goldy Bot's async loop. You can use this to run async methods in non async functions.
Like this ``async_loop.run_until_complete(async_function())``
"""
