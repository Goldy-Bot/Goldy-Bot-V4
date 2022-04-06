import traceback
import nextcord
from nextcord.ext import commands
import json
import time
import asyncio
import math
import random
from types import SimpleNamespace

import GoldyBot
from ...GoldyBotV3 import settings
from ...GoldyBotV3.src import goldy_func, goldy_utility, goldy_error
import pymongo

config = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON))

database_url = None

cog_name = "DATABASE"

#Connect to Database
try:
    goldy_func.print_and_log(None, "MongoClient connecting to database...")
    database_url = goldy_func.get_database_url()

    if not database_url == None:
        if not database_url == False:
            client = pymongo.MongoClient(goldy_func.get_database_url(), serverSelectionTimeoutMS=2000)
            members_data = client[config.read("collection_name")]

            client.server_info()

            goldy_func.print_and_log("info_2", "[CONNECTED]")
            goldy_func.print_and_log()

    if database_url == None:
        goldy_func.print_and_log(None, "[DATABASE DISABLED]")
        goldy_func.print_and_log("warn", "MongoDB database is disabled as 'None' has been passed in the database_url.txt or goldy failed to connect to the database. Database functions will still work for development purposes but no databases will be effected and there may be errors everywhere.")
        goldy_func.print_and_log()

except Exception as e:
    database_url = None
    goldy_func.print_and_log("error", "Couldn't connect to Database! Check the cluster URL you entered.")
    goldy_func.print_and_log("warn", ">>> " + str(e))
    goldy_func.print_and_log()

class database(commands.Cog):
    def __init__(self, client):
        global database_url
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = None

    class guild():
        
        @staticmethod
        async def create(code_name): #Creates database collection for discord guild.
            try:

                #Check if guild collection exists.
                list_of_collections = members_data.list_collection_names()

                if not f"{code_name} (server)" in list_of_collections:
                    #Create guild collection.
                    guild_collection = members_data[f"{code_name} (server)"]

                    #Add content
                    guild_collection.insert_one({"_id":1, "goldy":"Hello, I have automatically created a database collection for this discord guild.", "notice":"Feel free to delete this document."})

                    goldy_func.print_and_log("info_2", f"[{cog_name}] Added a guild collection for {code_name} to the database.")

                else:
                    goldy_func.print_and_log(None, f"[{cog_name}] The {code_name}'s guild collection already exits so I'm not creating a new one.")

            except Exception as e:
                goldy_func.print_and_log("error", f"Exception in database guild.create method. {e}")

        @staticmethod
        async def list(): #Returns a list of all the guild collections in the database. (Used for checking if a collection has been created for a guild.)
            try:
                list_of_collections = members_data.list_collection_names()
                return list_of_collections

            except Exception as e:
                goldy_func.print_and_log("error", f"Exception in database guild.list method. {e}")
                return False

        @staticmethod
        async def pull(ctx): #Pulls all data from a guild database and returns them in a list.
            list_ = []

            try:
                x = goldy_utility.servers.get(ctx.guild.id)
                guild_collection = members_data[f"{x.names.code_name} (server)"]

                guild_member_data = guild_collection.find({})
                for member in guild_member_data:
                    list_.append(member)

                return list_

            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())

    class global_():
        @staticmethod
        async def pull(): #Pulls all data from the global database and returns them in a list.
            list_ = []

            try:
                global_collection = members_data["global"]

                global_member_data = global_collection.find({})
                for member in global_member_data:
                    list_.append(member)

                return list_

            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())

    class member():

        @staticmethod
        async def add(ctx): #Add member to guild database and global database. (Used to add new members.)
            member = ctx.author
            try:
                if not database_url == None: #Checks if database is disabled.
                        
                    #Finding guild database
                    x = goldy_utility.servers.get(ctx.guild.id)
                    guild_collection = members_data[f"{x.names.code_name} (server)"]

                    #Global database.
                    global_collection = members_data["global"]

                    #First check if member is already in database.
                    in_database = await database.member.checks.in_database(ctx, guild_collection, global_collection)

                    #If member not in global database add them.
                    if not in_database[0] == True:
                        random_account_num = random.randint(100000000000, 999999999999) #Generate random bank number.

                        push_format = {"_id": member.id, f"{member.id}": {"goldCoins": 500, "accountNum": random_account_num, "exp_per_message": 7}}
                        global_collection.insert_one(push_format)

                        goldy_func.print_and_log(None, f"[{cog_name}] Added the member '{member.name}' to global database.")

                    #If member not in guild database add them.
                    if not in_database[1] == True:
                        push_format = {"_id": member.id, f"{member.id}": {"rank": 0, "exp": 0}}
                        guild_collection.insert_one(push_format)

                        goldy_func.print_and_log(None, f"[{cog_name}] Added the member '{member.name}' to guild database.")

                    else:
                        goldy_func.print_and_log(None, f"[{cog_name}] '{member.name}' is already in that database.")

                else:
                    goldy_func.print_and_log(None, f"[{cog_name}] Added the member '{member.name}' to database.")

            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())
                
        @staticmethod
        async def pull(ctx): #Pulls memeber data from database. (Used to get member data.)
            member = ctx.author

            async def add_to_database_then_try_again(ctx):

                goldy_func.print_and_log("info", f"Somethings not right with '{member.name}'s member data so I'm adding them to the database their missing from and trying again.")

                await database.member.add(ctx) #Try to add member to database.

                #Find member's guild data.
                guild_member_data = guild_collection.find_one({"_id": member.id})

                #Find member's global data.
                global_member_data = global_collection.find_one({"_id": member.id})

                #Combind the data.
                combined_member_data = goldy_func.Merge(guild_member_data[f"{member.id}"], global_member_data[f"{member.id}"])

                #Convert json to python class.
                combined_member_data = json.dumps(combined_member_data)
                combined_member_data = json.loads(combined_member_data, object_hook=lambda d: SimpleNamespace(**d)) 

                return combined_member_data #Returns the json but as python class so you can easily pick the data.

            try:
                if not database_url == None: #Checks if database is disabled.
                    
                    #Finding guild database
                    x = goldy_utility.servers.get(ctx.guild.id)
                    guild_collection = members_data[f"{x.names.code_name} (server)"]

                    #Global database.
                    global_collection = members_data["global"]

                    #Find member's guild data.
                    guild_member_data = guild_collection.find_one({"_id": member.id})

                    #Find member's global data.
                    global_member_data = global_collection.find_one({"_id": member.id})

                    #Check if data was found.
                    if not guild_member_data == None:
                        if not global_member_data == None:

                            #Combind the data.
                            combined_member_data = goldy_func.Merge(guild_member_data[f"{member.id}"], global_member_data[f"{member.id}"])

                            #Convert json to python class.
                            combined_member_data = json.dumps(combined_member_data)
                            combined_member_data = json.loads(combined_member_data, object_hook=lambda d: SimpleNamespace(**d)) 

                            return combined_member_data #Returns the json but as python class so you can easily pick the data.

                        else: #If not try to add member to database.
                            result = await add_to_database_then_try_again(ctx)
                            return result

                    else: #If not try to add member to database.
                        result = await add_to_database_then_try_again(ctx)
                        return result

            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())
        
        @staticmethod
        async def push(ctx, member_data): #Push member data to database. (Used to push the dam member data back up to where the fuck it even came from.)
            member = ctx.author
            try:
                if not database_url == None: #Checks if database is disabled.
                    
                    #Grab and delete rank and exp from combind data.
                    member_rank = int(member_data.rank)
                    member_exp = int(member_data.exp)

                    #Delete rank and exp.
                    del member_data.rank
                    del member_data.exp

                    #Try to grab and delete the colours list and member colour object from combined data. (Added with the devlopment of the colours extenstion.)
                    try: colours_list = []; colours_list = list(member_data.colours); del member_data.colours
                    except AttributeError: pass

                    try: colour = None; colour = member_data.colour; del member_data.colour
                    except AttributeError: pass

                    #Finding guild database
                    x = goldy_utility.servers.get(ctx.guild.id)
                    guild_collection = members_data[f"{x.names.code_name} (server)"]

                    #Global database.
                    global_collection = members_data["global"]

                    #Push data to guild database.
                    guild_push_format = { "$set": { "_id": member.id, f"{member.id}": {"rank": member_rank, "exp": member_exp, "colour": colour, "colours": colours_list} }}
                    guild_query = {"_id": member.id}
                    guild_collection.update_one(guild_query, guild_push_format)

                    goldy_func.print_and_log(None, f"[{cog_name}] Updated '{member.name}'s guild member data.")

                    #Push data to global database.
                    sn = SimpleNamespace(data_array=member_data)
                    sa = json.loads(json.dumps(sn, default=lambda s: vars(s)))
                    global_push_format = { "$set": { "_id": member.id, f"{member.id}" : sa["data_array"] }}
                    global_query = {"_id": member.id}
                    global_collection.update_one(global_query, global_push_format)

                    goldy_func.print_and_log(None, f"[{cog_name}] Updated '{member.name}'s global member data.")
                    
            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())

        @staticmethod
        async def add_object(ctx, object_name : str, object_value, member_data=None): #Adds new object to member's global data or guild data.
            
            try:
                if member_data == None:
                    member_data = await database.member.pull(ctx)
                    setattr(member_data, object_name, object_value)
                    await database.member.push(ctx, member_data)

                else:
                    setattr(member_data, object_name, object_value)
                    
                goldy_func.print_and_log(None, f"[{cog_name.upper()}] Added object '{object_name}' with value '{object_value}' to '{ctx.author}'s member data.")
                return member_data

            except Exception as e:
                await goldy_error.log(None, error=traceback.format_exc())

        class checks():
            
            @staticmethod
            async def in_database(ctx, guild_collection, global_collection): #Checks if memeber is in the global and guild database.
                global_database = global_collection.find({})
                guild_database = guild_collection.find({})

                in_global = False
                in_guild = False

                for member in global_database: #Checking Global database for member.
                    if member["_id"] == ctx.author.id:
                        in_global = True

                for guild_member in guild_database: #Checking Guild database for member.
                    if guild_member["_id"] == ctx.author.id:
                        in_guild = True

                return in_global, in_guild #Where I left off. (06/08/2021)

            @staticmethod
            async def has_item(ctx, code_name, type=None, member_data=None): #Checks if memeber has item.
                #Find member data.
                if member_data == None:
                    member_data = await database.member.pull(ctx)
                
                try:
                    if type in ["colour", "color"]:
                        #Find colour in member's colours list.
                        if str(code_name) in member_data.colours:
                            return True
                        else:
                            return False
                    else:
                        #Find item in member's items list.
                        if str(code_name) in member_data.items:
                            return True
                        else:
                            return False

                except Exception as e: #Usally occurs if member has no items list.
                    try:
                        goldy_func.print_and_log("warn", "I got an error exception in member.checks.has_item but this may be because the member doesn't have a items list so I'm creating one for him.")
                        
                        #Creating items list.
                        await database.member.add_object(ctx, "items", [])

                        #Creating colours list.
                        await database.member.add_object(ctx, "colours", [])

                        await database.member.push(ctx, member_data) #Updating member data in database.

                        return False

                    except Exception as e:
                        await goldy_error.log(None, error=traceback.format_exc())
                        return False

    """
    def pull_everything(self): #Pull all member data in (Used in situations where you would need all the database.)
        lol = self.collection.find({})
        for member in lol:
            dict[member]

        print(dict)
    """



def setup(client):
    client.add_cog(database(client))