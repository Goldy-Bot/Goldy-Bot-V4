"""
💛 Goldy Bot V4

Copyright (C) 2022 - Dev Goldy
"""

from . import files, paths, logging, goldy, cache, token, settings, config, info, database
from . import internal_cogs, utility, ext

# Functions
log = logging.print_and_log

# Function Decorators
command = ext.commands.command
cmd = command

# Classes
Goldy = goldy.Goldy
Database = database.Database
