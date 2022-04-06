"""
💛 Goldy Bot V4

Copyright (C) 2022 - Dev Goldy
"""

import nextcord
from . import files, paths, logging, goldy, cache, token, settings, config, info, database
from . import internal_cogs, ext, utility, objects

# Functions
log = logging.print_and_log

# Function Decorators
command = ext.commands.command
cmd = command

# Class Inheritors
Extenstion = ext.extenstions.Extenstion

slash_command = nextcord.Client.slash_command

# Classes
Goldy = goldy.Goldy
Database = database.Database
