from __future__ import annotations
import nextcord

from GoldyBot.objects.slash import Interaction, InteractionToCtx

class Channel():
    """A class representing a discord channel in Goldy Bot."""
    def __init__(self, ctx, channel_id:str|int=None, mention_str:str=None, channel_object:nextcord.abc.GuildChannel=None):

        self.ctx = ctx
        self.channel_id_ = channel_id
        self.mention_str_ = mention_str
        self.channel_object_ = channel_object

        if self.channel_object_ == None:
            # Find the channel.
            self.channel = self.find_channel(self.channel_id)
        else:
            self.channel = self.channel_object_
        
    @property
    def channel_id(self) -> str:
        """Returns id of discord channel. Defaults to ctx channel if ``channel_id``, ``mention_str`` and ``channel_object`` are None."""
        if not self.channel_id_ == None: return str(self.channel_id_)
        if not self.mention_str_ == None: return self.mention_str_[3:-1]
        if not self.channel_object_ == None: return str(self.channel_object_.id)
        else:
            if isinstance(self.ctx, Interaction):
                return str(InteractionToCtx(self.ctx).channel.id)
            else:
                return str(self.ctx.channel.id)
                
    @property
    def name(self):
        """Returns the discord channel name."""
        return self.channel.name

    @property
    def display_name(self):
        """Alias of ``Channel().name``"""
        return self.name

    def find_channel(self, channel_id:int|str) -> nextcord.abc.GuildChannel | None:
        """Finds the damn channel!"""

        if not channel_id == None:
            return nextcord.utils.get(self.ctx.guild.channels, id=int(channel_id))
        else:
            return None