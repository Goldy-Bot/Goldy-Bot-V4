import asyncio
import pymongo
import motor.motor_asyncio
import GoldyBot

MODULE_NAME = "DATABASE"

class Database():
    """Goldy Bot's class to interface with a Mongo Database."""
    def __init__(self, database_token_url:str):
        self.database_token_url = database_token_url
        self.loop = asyncio.get_event_loop()

        config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

        try:
            # Initializing MongoDB database
            self.client:pymongo.MongoClient = motor.motor_asyncio.AsyncIOMotorClient(self.database_token_url, serverSelectionTimeoutMS=2000)
            self.loop.run_until_complete(self.client.server_info())
            self.database = self.client[config.read("database_name")]

            # Cache database class.
            GoldyBot.cache.main_cache_dict["database"] = self

            GoldyBot.logging.log("info_2", f"[{MODULE_NAME}] [CONNECTED]")

        except Exception:
            GoldyBot.logging.log("error", f"[{MODULE_NAME}] Couldn't connect to Database! Check the database URL you entered.")
            GoldyBot.Goldy().stop("Couldn't connect to Database! Check the database URL you entered.")

    async def insert(self, collection:str, data) -> bool:
        """Tells database to insert the data provided into a collection."""
        await self.database[collection].insert_one(data)
        GoldyBot.logging.log(f"[{MODULE_NAME}] Inserted '{data}' into '{collection}.'")
        return True

    async def find(self, collection:str, query:dict):
        return await self.database[collection].find(query)

    async def list_collection_names(self):
        return await self.database.list_collection_names()

    async def find_one(self, collection:str, query:dict):
        """Tells database to search for and return specific data from a collection."""
        data = await self.database[collection].find_one(query)
        if not data == None:
            GoldyBot.logging.log(f"[{MODULE_NAME}] Found '{query}' in '{collection}.'")
            return data
        else:
            GoldyBot.logging.log(f"[{MODULE_NAME}] '{query}' was not found in '{collection}.'")
            return None
        

    async def create_collection(self, collection_name:str, data):
        await self.database[collection_name].insert_one(data)
        GoldyBot.logging.log(f"[{MODULE_NAME}] Database collection '{collection_name}' created.")

