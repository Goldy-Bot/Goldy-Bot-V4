import GoldyBot
"""
Just a test extenstion.
"""

class JeffTheKiller(GoldyBot.Extenstion):
    def __init__(self):
        super().__init__(self)
        
    def loader(self):

        @GoldyBot.command()
        async def jeff(self, ctx):
            await ctx.send("jiff")

JeffTheKiller()