import random

import GoldyBot

from .money import Money

class Member(Money):
    """Creates member database interface with ctx to allow for easy grabbing of member data."""
    def __init__(self, ctx, member) -> None:
        self.ctx = ctx
        self.actual_member:GoldyBot.member.Member = member

        self.database = GoldyBot.cache.database()

        # Generate document if member doesn't exists in database.
        GoldyBot.async_loop.run_until_complete(self.setup())

        super().__init__(member)

    async def get_member_data(self):
        """Returns member's database collection."""
        return await self.database.find_one("global", {"_id":int(self.actual_member.member_id)})

    async def setup(self):
        """Makes sure this member is setup in global and guild collection."""

        # Global setup if member does not exist in global collection.
        if await self.database.find_one("global", {"_id":int(self.actual_member.member_id)}) == None:
            await self.database.insert("global", data={
                "_id":int(self.actual_member.member_id),

                f"{self.actual_member.member_id}" : {}
            })

        # Guild setup if member does not exist in guild collection.
        if await self.database.find_one(GoldyBot.cache.FindGuilds().find_object_by_id(self.ctx.guild.id).database_collection_name, {"_id":int(self.actual_member.member_id)}) == None:
            await self.database.insert(GoldyBot.cache.FindGuilds().find_object_by_id(self.ctx.guild.id).database_collection_name, data={
                "_id":int(self.actual_member.member_id),

                f"{self.actual_member.member_id}" : {}
            })
