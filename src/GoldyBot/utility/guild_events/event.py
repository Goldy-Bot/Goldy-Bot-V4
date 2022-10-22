from __future__ import annotations

import GoldyBot
from datetime import datetime

class GuildEvent():
    """This class allows you to control a guild event."""
    def __init__(self, ctx, name:str, description:str, entity_type:GoldyBot.nextcord.ScheduledEventEntityType, start_time:datetime, end_time:datetime=None, 
        channel:GoldyBot.Channel=None, metadata:GoldyBot.nextcord.EntityMetadata = None, image:GoldyBot.File=None, reason:str="Becauwse WatAshi said uwu and bawked, that's why i dow thiws"):

        self.ctx = ctx
        self.guild:GoldyBot.utility.guilds.guild.Guild = GoldyBot.cache.FindGuilds().find_object_by_id(ctx.guild.id)

        self._name = name
        self._description = description
        self._entity_type = entity_type
        self._start_time = start_time
        self._end_time = end_time
        self._channel = channel
        self._metadata = metadata
        self._image = image
        self._reason = reason

        self.ScheduledEvent:GoldyBot.nextcord.ScheduledEvent = None

        if self.guild == None:
            raise GoldyBot.errors.GoldyBotError("Guild is none. Guild does not exist in cache for some reason uwu.")

    @property
    def name(self) -> str:
        """The name of the guild event."""
        return self._name

    @property
    def description(self) -> str:
        """The description of the guild event."""
        return self._description

    @property
    def entity_type(self) -> GoldyBot.nextcord.ScheduledEventEntityType:
        """The entity type of the guild."""
        return self._entity_type

    @property
    def start_time(self) -> datetime:
        """Returns the start time and date of the event in datetime object."""
        return self._start_time

    @property
    def end_time(self) -> datetime|None:
        """Returns the end time and date of the event in datetime object."""
        return self._end_time

    @property
    def channel(self) -> GoldyBot.channel.Channel:
        """Returns the channel of this event."""
        return self._channel

    @property
    def metadata(self) -> GoldyBot.nextcord.EntityMetadata:
        return self._entity_type

    @property
    def image(self) -> GoldyBot.File:
        return self._image

    @property
    def reason(self) -> str:
        """Returns the set reasoning of this event, if none a sussy default message is returned instead."""
        return self._reason


    async def create(self) -> GoldyBot.nextcord.ScheduledEvent:
        """Creates the ⭐ fancy guild event."""
        self.ScheduledEvent = await self.guild.nextcord_guild_object.create_scheduled_event(
            name=self.name, description=self.name, entity_type=self.entity_type, start_time=self.start_time, end_time=self.end_time, channel=self.channel.channel
        )
        return self.ScheduledEvent