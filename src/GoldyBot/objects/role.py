import nextcord

import GoldyBot
from GoldyBot.errors import FailedToFindRole

class Role():
    """
    A class representing a discord role in Goldy Bot.
    
    Raises FailedToFindRole() when role is not found.
    """
    def __init__(self, ctx, role_id:str=None, code_name:str=None, role_name:str=None):
        role_:nextcord.Role = None

        if not role_id == None:
            role_ = ctx.guild.get_role(int(role_id))
            if role_ == None: raise FailedToFindRole(option_used="id", option_value=role_id)
            else: GoldyBot.logging.log(f"Found the role '{role_.name}' by id.")
        if not code_name == None:
            #TODO: #18 Create goldy bot method to find roles in guild config with code_name.
            pass
        if not role_name == None:
            role_ = nextcord.utils.get(ctx.guild.roles, name=role_name)
            if role_ == None: raise FailedToFindRole(option_used="role name", option_value=role_name)
            else: GoldyBot.logging.log(f"Found the role '{role_.name}' by name.")

        if role_id and code_name and role_name == None:
            GoldyBot.logging.log("error", "Either 'role_id', 'code_name' or 'role_name' has to be passed in the 'Role()'.")

        self.role_ = role_

    @property
    def role(self) -> nextcord.Role:
        """Returns the actual representation of the role in nextcord."""
        return self.role_