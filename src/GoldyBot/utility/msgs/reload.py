import GoldyBot.utility.goldy.colours as colours

help_des = 'An admin command for reloading the modules in GoldyBot.'

module = "💜 Module"
module_red = "❤️ Module"
module_blue = "💙 Module"
module_orange = "🧡 Module"

class ReloadedEmbed:
    title = f'{module} Reloaded!'
    des = '''**``{}`` has been reloaded! 👍**'''
    colour = colours.PURPLE

    thumbnail = "https://www.pngitem.com/pimgs/m/684-6848954_anime-thumbs-up-png-png-download-transparent-png.png"

class FailedToLoadEmbed:
    title = f"{module_red} Failed to Load!"
    des = "**The Module ``{}`` failed to load!**"
    colour = colours.RED

class ModuleNotFoundEmbed:
    title = f"{module_blue} Not Found!"
    des = "**The Module ``{}`` was not Found!**"
    colour = colours.AKI_BLUE

class AdminCanNotBeReloadedEmbed:
    title = f"{module_orange} Not Allowed!"
    des = "**The admin module can not be reloaded!**"
    colour = colours.AKI_ORANGE