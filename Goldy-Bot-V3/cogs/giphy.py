import nextcord
from nextcord.ext import commands
import asyncio

from src.goldy_func import *
from src.goldy_utility import *
import src.utility.msg as msg

from .giphy_cog import api

cog_name = "giphy"

class giphy(commands.Cog, name="🎞️Gifs"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 9

        loop = asyncio.get_event_loop()
        loop.create_task(api.api_key.get())

def setup(client):
    client.add_cog(giphy(client))

#Need Help? Check out this: {youtube playlist}