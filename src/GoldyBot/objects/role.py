from __future__ import annotations
import nextcord

import GoldyBot
from GoldyBot.errors import FailedToFindRole
from GoldyBot.objects.slash import Interaction, InteractionToCtx

class Role():
    """
    A class representing a discord role in Goldy Bot. Either 'role_id', 'role_name', 'mention_str' or 'role_object' has to be passed in the 'Role()'.
    
    Raises FailedToFindRole() when role is not found.
    """
    def __init__(self, ctx, role_id:str=None, role_name:str=None, role_object:nextcord.Role=None, mention_str:str=None):
        self.ctx = ctx
        self.role_id_ = role_id
        self.role_name_ = role_name
        self.mention_str_ = mention_str
        self.role_object_ = role_object

        self.role_ = None

        if self.role_object_ == None:
            self.role_ = self.find_role(self.role_id, self.role_name_)
        else:
            self.role_ = self.role_object_

    @property
    def role(self) -> nextcord.Role:
        """Returns the actual representation of the role in nextcord."""
        return self.role_

    @property
    def role_id(self) -> str|None:
        """Returns id of discord role. Returns ``None`` if ``role_id``, ``role_name``, ``mention_str`` and ``role_object`` are left blank."""
        if not self.role_id_ == None: return str(self.role_id_)
        if not self.mention_str_ == None: return self.mention_str_[3:-1]
        if not self.role_object_ == None: return str(self.role_object_.id)

        return None

    @property
    def role_name(self) -> str:
        """Returns the name of the role."""
        return self.role.name

    def find_role(self, role_id:int|str, role_name:str=None) -> nextcord.Role:
        role:nextcord.Role

        if role_name == None:
            if not role_id == None:
                role = self.ctx.guild.get_role(int(role_id))
            else:
                role = None

            if role == None:
                raise FailedToFindRole(option_used="id", option_value=role_id)
            else:
                GoldyBot.logging.log(f"Found the role '{role.name}' by id.")
                return role
            
        else:
            role = nextcord.utils.get(self.ctx.guild.roles, name=role_name)

            if role == None: 
                raise FailedToFindRole(option_used="role name", option_value=role_name)
            else:
                GoldyBot.logging.log(f"Found the role '{role.name}' by name.")
                return role