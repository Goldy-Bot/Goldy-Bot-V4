import GoldyBot
from GoldyBot.utility.commands import *

AUTHOR = 'Dev Goldy'
AUTHOR_GITHUB = 'https://github.com/THEGOLDENPRO'
OPEN_SOURCE_LINK = 'https://github.com/Goldy-Bot/Example-GoldyBot-Module'

class Help(GoldyBot.Extension):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

    def loader(self):

        @GoldyBot.command()
        async def help(self:Help, ctx):
            pass

def load():
    #Help(__name__) # Help extension is not done yet.
    pass