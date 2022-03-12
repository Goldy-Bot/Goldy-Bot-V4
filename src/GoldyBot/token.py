import GoldyBot

MODULE_NAME = "TOKEN"

def get():
    """Commands goldy bot to get the token."""
    file = GoldyBot.files.File(GoldyBot.paths.TOKEN)
    token = file.read()

    if token in ["", "{ENTER BOT TOKEN HERE}", None]:
        GoldyBot.log("error", "Please enter your discord token in the 'TOKEN.txt' file located in 'config' and run Goldy Bot again.")
        file.write("{ENTER BOT TOKEN HERE}")

        # Stop bot immedently.
        GoldyBot.Goldy.stop("There's no Discord Token!")

    else:
        return token