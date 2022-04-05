import pymongo

MODULE_NAME = "DATABASE"

class Database():
    """Goldy Bot's class to interface with a Mongo Database."""
    def __init__(self, token:str):
        import GoldyBot
        self.config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

        try:
            self.client = pymongo.MongoClient(token, serverSelectionTimeoutMS=2000)
            GoldyBot.logging.log(self.client.server_info())
            self.members_data = self.client[self.config.read("collection_name")]

            GoldyBot.logging.log("info_2", f"[{MODULE_NAME}] [CONNECTED]")

        except Exception:
            GoldyBot.logging.log("error", "Couldn't connect to Database! Check the database URL you entered.")
            GoldyBot.Goldy().stop("Couldn't connect to Database! Check the database URL you entered.")