import pymongo
import GoldyBot

MODULE_NAME = "DATABASE"

class Database():
    """Goldy Bot's class to interface with a Mongo Database."""
    def __init__(self, database_token_url:str):
        import GoldyBot
        self.config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

        try:
            # Initializing MongoDB database
            self.client = pymongo.MongoClient(database_token_url, serverSelectionTimeoutMS=2000)
            self.client.server_info()
            self.database = self.client[self.config.read("database_name")]

            # Cache database class.
            GoldyBot.cache.main_cache_dict["database"] = self

            GoldyBot.logging.log("info_2", f"[{MODULE_NAME}] [CONNECTED]")

        except Exception:
            GoldyBot.logging.log("error", f"[{MODULE_NAME}] Couldn't connect to Database! Check the database URL you entered.")
            GoldyBot.Goldy().stop("Couldn't connect to Database! Check the database URL you entered.")

    def insert(self, collection:str, data) -> bool:
        """Tells database to insert the data provided into a collection."""
        self.database[collection].insert_one(data)
        GoldyBot.logging.log(f"[{MODULE_NAME}] Inserted '{data}' into '{collection}.'")
        return True

    def find(self, collection:str, query:dict):
        return self.database[collection].find(query) 

    def list_collection_names(self):
        return self.database.list_collection_names()

    def find_one(self, collection:str, query:dict):
        """Tells database to search for and return specific data from a collection."""
        data = self.database[collection].find_one(query)
        GoldyBot.logging.log(f"[{MODULE_NAME}] Found '{query}' in '{collection}.'")
        return data

    def create_collection(self, collection_name:str, data):
        self.database[collection_name].insert_one(data)

