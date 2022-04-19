import GoldyBot
from .. import goldy

class CommandNotFound:
    class Embed:
        title = "❤️ COMMAND NOT FOUND!"
        des = "**❤️ Could not find the command or cog named that.**"

class CommandUsage:
    class Embed:
        title = "🧡 COMMAND USAGE!"
        des = "***🧡{}, please use the correct command usage or else goldy ain't understanding you: ``{}``***"
        thumbnail = "https://pa1.narvii.com/6962/5aea6e415556771b6d52941a58a68bab12b571a2r1-490-390_hq.gif"
        colour = goldy.colours.AKI_ORANGE

class CommandNoPerms:
    class Embed:
        title = "💔 NO PERMS!"
        des = "***💔{}, you don't have permission to use this command.***"
        thumbnail = "https://c.tenor.com/fLBpWkmS5Y8AAAAd/looney-tunes-daffy-duck.gif"
        colour = goldy.colours.RED

class CommandGuildNotRegistered:
    class Embed:
        title = "🧡 GUILD NOT REGISTERED!"
        des = "***🧡{}, this guild is not registered.***"
        thumbnail = "http://comics-porn.info/img/anime-sweating-gif-5.jpg"
        colour = goldy.colours.AKI_ORANGE