from __future__ import annotations
import nextcord

from .. import database
from GoldyBot.objects.slash import Interaction, InteractionToCtx

from . import role

class Member(database.member.Member):
    """A class representing a discord member in Goldy Bot."""
    def __init__(self, ctx, member_id:str|int=None, mention_str:str=None, member_object:nextcord.Member=None):
        self.ctx = ctx
        self.member_id_ = member_id
        self.mention_str_ = mention_str
        self.member_object_ = member_object

        if self.member_object_ == None:
            # Find the member.
            self.member = self.find_member(self.member_id)
        else:
            self.member = self.member_object_

        super().__init__(ctx, self)
        
    @property
    def member_id(self) -> str:
        """Returns id of discord member. Defaults to ctx author if ``member_id``, ``mention_str`` and ``member_user_object`` are None."""
        if not self.member_id_ == None: return str(self.member_id_)
        if not self.mention_str_ == None: return self.mention_str_[3:-1]
        if not self.member_object_ == None: return str(self.member_object_.id)
        else:
            if isinstance(self.ctx, Interaction):
                return str(InteractionToCtx(self.ctx).author.id)
            else:
                return str(self.ctx.author.id)
                
    @property
    def name(self):
        """Returns the discord name of member including tag. Does not return server nickname!"""
        return self.member.name

    @property
    def display_name(self):
        """Returns display name of member, so server nickname."""
        return self.member.display_name

    # Roles
    #---------
    def has_role(self, role:role.Role):
        """Checks if the member has a certain role."""
        if role.role in self.member.roles:
            return True
        else:
            return False

    async def add_role(self, role:role.Role):
        """This method addes the specified role to this member."""
        if not self.has_role(role):
            await self.member.add_roles(role)
            return True
        else:
            return True

    async def remove_role(self, role:role.Role):
        """This method removes the specified role from this member."""
        if self.has_role(role):
            await self.member.remove_roles(role)
            return True
        else:
            return None

    def find_member(self, member_id:int|str) -> nextcord.Member | None:
        """Finds the damn member!"""

        if not member_id == None:
            return nextcord.utils.get(self.ctx.guild.members, id=int(member_id))
        else:
            return None

    # Utils
    async def send(self, **args):
        args.pop("ephemeral")
        await self.member.send(**args)