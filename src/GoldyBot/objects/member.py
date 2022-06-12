from __future__ import annotations
import nextcord

from . import role

class Member():
    """A class representing a discord member in Goldy Bot."""
    def __init__(self, ctx, member_id:str|int=None, mention_str:str=None):
        self.ctx = ctx
        self.member_id_ = member_id
        self.mention_str_ = mention_str

        # Find the member.
        self.member = self.find_member(self.member_id)
        
    @property
    def member_id(self) -> str:
        """Returns id of discord member."""
        if not self.member_id_ == None: return str(self.member_id_)
        if not self.mention_str_ == None: return self.mention_str_[3:-1]
        
        return None

    @property
    def name(self):
        """Returns the discord name of member including tag. Does not return server nickname!"""
        return self.member.name

    @property
    def display_name(self):
        """Returns display name of member, so server nickname."""
        return self.member.display_name

    def has_role(self, role:role.Role):
        """Checks if the member has a certain role."""
        if role.role in self.member.roles:
            return True
        else:
            return False

    def find_member(self, member_id:int|str) -> nextcord.Member | None:
        """Finds the damn member!"""
        if not member_id == None:
            return nextcord.utils.get(self.ctx.guild.members, id=int(member_id))
        else:
            return None