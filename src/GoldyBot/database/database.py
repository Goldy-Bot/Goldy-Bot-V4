from __future__ import annotations
import asyncio
from typing import Any, List
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
            if not database_token_url.lower() in ["none", "null"]: 
                # Initializing MongoDB database
                self.client:pymongo.MongoClient = motor.motor_asyncio.AsyncIOMotorClient(self.database_token_url, serverSelectionTimeoutMS=2000)
                self.loop.run_until_complete(self.client.server_info())
                self.database = self.client[config.read("database_name")]

                # Cache database class.
                GoldyBot.cache.main_cache_dict["database"] = self

                GoldyBot.logging.log("info_2", f"[{MODULE_NAME}] [CONNECTED]")
            
            else:
                GoldyBot.logging.log("info_5", f"[{MODULE_NAME}] [DATABASE DISABLED]")
                GoldyBot.logging.log("info_3", f"[{MODULE_NAME}] Database is disabled because '{database_token_url}' was entered.")

        except Exception:
            GoldyBot.logging.log("error", f"[{MODULE_NAME}] Couldn't connect to Database! Check the database URL you entered.")
            GoldyBot.Goldy().stop("Couldn't connect to Database! Check the database URL you entered.")

    async def insert(self, collection:str, data) -> bool:
        """Tells database to insert the data provided into a collection."""
        await self.database[collection].insert_one(data)
        GoldyBot.logging.log(f"[{MODULE_NAME}] Inserted '{data}' into '{collection}.'")
        return True

    async def edit(self, collection:str, query, data:dict) -> bool:
        """Tells database to find and edit a document with the data provided in a collection."""
        await self.database[collection].update_one(query, {"$set": data})
        GoldyBot.logging.log(f"[{MODULE_NAME}] Edited '{query}' into '{data}.'")
        return True

    async def remove(self, collection:str, data) -> bool:
        """Tells database to find and delete a copy of this data from the collection."""
        await self.database[collection].delete_one(data)
        GoldyBot.logging.log("INFO_5", f"[{MODULE_NAME}] Deleted '{data}' from '{collection}.'")
        return True

    async def find(self, collection:str, query, key, max_to_find=50) -> List[dict]:
        """Searches for documents with the query."""
        try:
            document_list = []
            cursor = self.database[collection].find(query).sort(key)

            for document in await cursor.to_list(max_to_find):
                document_list.append(document)

            return document_list
        except KeyError as e:
            GoldyBot.logging.log("error", f"[{MODULE_NAME}] Could not find the collection '{collection}'!")
            return None

    async def find_all(self, collection:str, max_to_find=100) -> List[dict] | None:
        """Finds and returns all documents in a collection. This took me a day to make! 😞"""
        try:
            document_list = []
            cursor = self.database[collection].find().sort('_id')

            for document in await cursor.to_list(max_to_find):
                document_list.append(document)

            return document_list
        except KeyError as e:
            GoldyBot.logging.log("error", f"[{MODULE_NAME}] Could not find the collection '{collection}'!")
            return None

    async def get_collection(self, collection):
        """Returns cursor of the following collection."""
        return self.database[collection]

    async def list_collection_names(self) -> List[str]:
        """Returns list of all collection names."""
        return await self.database.list_collection_names()

    async def find_one(self, collection:str, query:dict) -> (Any | None):
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

    async def delete_collection(self, collection_name:str):
        await self.database[collection_name].drop()
        GoldyBot.logging.log("INFO_5", f"[{MODULE_NAME}] Database collection '{collection_name}' dropped.")

    def new_instance(self, database_name:str):
        """Starts a new database instance the efficiant way. 👍"""
        class NewDatabase(Database):
            def __init__(self, database_self:Database):
                self.database = database_self.client[database_name]

        return NewDatabase(self)

