import GoldyBot.utility.goldy.colours as colours

help_des = 'An admin command for unloading modules in GoldyBot.'

module = "🖤 Module"
module_blue = "💙 Module"
module_orange = "🧡 Module"

class UnloadedEmbed:
    title = f'{module} Unloaded!'
    des = '''**``{}`` has been unloaded! 👍**'''
    colour = colours.GREY

    thumbnail = "https://www.pngitem.com/pimgs/m/684-6848954_anime-thumbs-up-png-png-download-transparent-png.png"

class ModuleNotFoundEmbed:
    title = f"{module_blue} Not Found!"
    des = "**The Module ``{}`` was not Found!**"
    colour = colours.AKI_BLUE

class AdminCanNotBeUnloadedEmbed:
    title = f"{module_orange} Not Allowed!"
    des = "**The admin module can not be reloaded!**"
    colour = colours.AKI_ORANGE