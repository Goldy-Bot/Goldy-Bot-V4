from . import role

class Member():
    """A class representing a discord member in Goldy Bot."""
    def __init__(self, ctx):
        self.ctx = ctx

    def has_role(self, role:role.Role):
        """Checks if the member has a certain role."""
        if role.role in self.ctx.author.roles:
            return True
        else:
            return False