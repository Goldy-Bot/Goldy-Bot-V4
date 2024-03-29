import os
import sys
import GoldyBot

MODULE_NAME = "PATHS"
"""This module contains all the variables with paths to Goldy Bot folders and files."""

# Creating Path to module
module_path = ""
platform = sys.platform

if platform == "win32":
    module_path_list = os.path.abspath(GoldyBot.__file__).split("\\"); module_path_list.pop(-1)

    for file in module_path_list: module_path += f"{file}/"

else:
    module_path_list = GoldyBot.__file__.split("/"); module_path_list.pop(-1)

    for file in module_path_list: module_path += f"{file}/"

# Goldy Bot Module Path
GOLDY_BOT = module_path[:-1]
"""Path to Goldy Bot module."""

# Folders
LOGS = "./logs"
CONFIG = "./config"
MODULES = "./modules"

ASSETS = f"{GOLDY_BOT}/assets"
INTERNAL_COGS_V4 = f"{GOLDY_BOT}/internal_modules/v4"
INTERNAL_MODULES_V4 = INTERNAL_COGS_V4
INTERNAL_COGS_V3 = f"{GOLDY_BOT}/internal_modules/v3"
TEMPLATES = f"{GOLDY_BOT}/templates"

# Files
TOKEN = CONFIG + "/BOT_TOKEN.txt"
DATABASE_TOKEN = CONFIG + "/DATABASE_TOKEN.txt"
GOLDY_CONFIG_JSON = CONFIG + "/goldy.json"
DATA_JSON = "./data.json"

# Templates
GOLDY_CONFIG_JSON_TEMPLATE = f"{TEMPLATES}/goldy_config.json"