import asyncio
import json
import os
from typing import List
import nextcord
import GoldyBot
from . import config

MODULE_NAME = "GUILD"

GUILD_CONFIG_TEMPLATE_JSON_PATH = GoldyBot.paths.GOLDY_BOT + "/utility/guilds/guild_config_template.json"

class Guild():
    """Class that represents a discord guild in Goldy Bot."""
    def __init__(self, guild:nextcord.Guild):
        self.guild = guild
        self.database:GoldyBot.database.Database = GoldyBot.cache.main_cache_dict["database"]

        self.goldy_config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

        self.allowed_guilds = self.goldy_config.read("allowed_guilds")
        self.config_file = self.get_config_file()

        # Cache this!
        if self.is_allowed:
            GoldyBot.cache.main_cache_dict["guilds"][f"{self.code_name}"] = {}
            GoldyBot.cache.main_cache_dict["guilds"][f"{self.code_name}"]["object"] = self

    async def setup(self):
        """Setup's a guild in Goldy Bot with the given nextcord guild object. This will create a config and database collection for the guild."""
        if self.is_allowed:
            # Generate config folder for guild of there isn't already.
            #-----------------------------------
            if not self.config_exist:
                # If the config is empty, write the guild config template to it.
                template = GoldyBot.files.File(GUILD_CONFIG_TEMPLATE_JSON_PATH).read()
                template_json_obj = json.loads(template)
                template_json_obj["id"] = self.id
                template_json_obj["code_name"] = self.code_name
                template_json_obj["display_name"] = self.guild.name
                self.config_file.write(json.dumps(template_json_obj))

            # Create a database collection for the guild if there isn't already.
            #--------------------------------------------------------------------
            if not self.database == None:
                if not await self.database_exist:
                    await self.database.create_collection(f"{self.code_name} (server)", {"_id":1, 
                    "goldy":"I've created this collection automatically for a guild.", 
                    "notice":"Feel free to delete this document."})
            else:
                GoldyBot.logging.log("warn", f"[{MODULE_NAME}] Skipping database guild collection creation because database is disabled.")

            GoldyBot.logging.log(f"We ran setup for the guild '{self.code_name}'.")
        else:
            GoldyBot.logging.log("warn", f"Setup for '{self.code_name}' did not run because guild is not in goldy bot guild list.")

    @property
    def id(self):
        return self.guild.id

    @property
    def code_name(self):
        try:
            return self.allowed_guilds[f"{self.id}"]
        except KeyError:
            return None

    @property
    def nextcord_guild_object(self) -> nextcord.Guild:
        """Returns back the nextcord guild class you entered before."""
        return self.guild

    @property
    def config(self) -> config.GuildConfig:
        """Returns guild's config class."""
        #TODO: If the config does not exist run guild setup.
        if self.config_exist:
            return config.GuildConfig(GoldyBot.config.Config(GoldyBot.files.File(f"{GoldyBot.paths.CONFIG}/{self.code_name}/config.json")))

    @property
    def is_allowed(self) -> bool:
        """Commands Goldy Bot to check whether the guild is allowed to be active."""
        try:
            self.allowed_guilds[f"{self.id}"] # If this fails then guild is not in list.
            return True
        except KeyError:
            return False

    @property
    def has_config_been_edited(self) -> bool:
        """Commands Goldy Bot to check if the config of this guild has actually been edited or not. Returns False if config does not exist."""
        if self.config_exist:
            if self.config_file.read() == GoldyBot.files.File(GUILD_CONFIG_TEMPLATE_JSON_PATH).read():
                return False
            else:
                return True
        else:
            return False

    @property
    def config_exist(self) -> bool:
        """Commands Goldy Bot to check if the guild exist in config."""
        if self.code_name in os.listdir(GoldyBot.paths.CONFIG):
            if self.config_file.read() in ["", "{}"]:
                return False
            return True
        else:
            return False

    @property
    async def database_exist(self) -> bool:
        """Commands Goldy Bot to check if the guild exist in the database collections."""
        if self.database_collection_name in await self.database.list_collection_names():
            return True
        else:
            return False

    @property
    def database_collection_name(self) -> str:
        return f"{self.code_name} (server)"

    def channels(self) -> List[GoldyBot.objects.channel.Channel]:
        """Returns all channels in the guild. IDK if this method works well lmao, I haven't done much testing."""
        channels_list:List[GoldyBot.objects.channel.Channel] = []
        for nc_channel in self.guild.channels:
            channels_list.append(GoldyBot.objects.channel.Channel(None, channel_object=nc_channel))

        return channels_list

    def get_config_file(self) -> GoldyBot.files.File:
        # Create guild config folder.
        GUILD_CONFIG_FOLDER_PATH = GoldyBot.files.File(GoldyBot.paths.CONFIG + f"/{self.code_name}/").file_path

        # Create guild config file.
        config_file = GoldyBot.files.File(GUILD_CONFIG_FOLDER_PATH + "config.json")

        return config_file

    async def get_members(self, ctx):
        """Method to get all the discord guild members."""

        member_list_:List[GoldyBot.Member] = []
        for member in self.guild.members:
            member_list_.append(GoldyBot.objects.member.Member(ctx, member_object=member))

        return member_list_

    async def get_channels(self, ctx):
        """Method to get all the discord guild's channels."""

        channel_list_:List[GoldyBot.Channel] = []
        for channel in self.guild.channels:
            channel_list_.append(GoldyBot.objects.channel.Channel(ctx, channel_object=channel))

        return channel_list_