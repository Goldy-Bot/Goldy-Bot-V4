import GoldyBot

MODULE_NAME = "TOKEN"

def get() -> str:
    """Commands goldy bot to get the token."""
    file = GoldyBot.files.File(GoldyBot.paths.TOKEN)
    token = file.read()

    if token in ["", "{ENTER BOT TOKEN HERE}", None]:
        GoldyBot.log("error", "Please enter your discord token in the 'TOKEN.txt' file located in 'config' and run Goldy Bot again.")
        file.write("{ENTER BOT TOKEN HERE}")

        # Stop bot immediately.
        GoldyBot.Goldy().stop("There's no Discord Token!")

    else:
        return token

def get_database() -> str:
    """Commands goldy bot to get the database url token."""
    file = GoldyBot.files.File(GoldyBot.paths.DATABASE_TOKEN)
    database_token = file.read()

    if database_token in ["", "{ENTER DATABASE URL HERE}", None]:
        GoldyBot.log("error", "Please enter your MongoDB database URL in the 'DATABASE_TOKEN.txt' file located in 'config' and run Goldy Bot again.")
        file.write("{ENTER DATABASE URL HERE}")

        # Stop bot immediately.
        GoldyBot.Goldy().stop("There's no MongoDB database URL!")

    else:
        return database_token