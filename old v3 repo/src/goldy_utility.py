import asyncio
import settings
import json
from types import SimpleNamespace
import nextcord
import os

from . import goldy_func, goldy_error, goldy_cache
from .utility import cmds
try:
    import config.config as config
except ModuleNotFoundError as e:
    pass

async def can_the_command_run(ctx, cog_name=None): #Moved the can_the_command_run function to the new utility folder in src.
    return await cmds.can_the_command_run(ctx, cog_name)

class goldy():

    class cogs():

        @staticmethod
        def load(client, path_to_cog : str): #Loads a cog into goldy bot.
            try:
                client.load_extension(path_to_cog)
                print("💚  Loaded {}".format(path_to_cog))

            except Exception as e:
                print("❤️ Failed to load {} []".format(path_to_cog, e))

        @staticmethod
        def unload(client, path_to_cog : str): #Loads a cog into goldy bot.
            try:
                client.unload_extension(path_to_cog)
                print("💙  Unloaded {}".format(path_to_cog))

            except Exception as e:
                print("❤️ Failed to load {} []".format(path_to_cog, e))

    @staticmethod
    async def in_production_mode(): #Checks weather goldy bot is in development or production mode.
        #Is bot in dev mode or production mode?
        try:
            if config.bot_mode == 'P':
                return True

            if config.bot_mode == 'D':
                return False
        except AttributeError as e:
            goldy_func.print_and_log("info", "Defaulted bot mode to 'Devlopment' because there was no config file. Edit the bot mode in 'config.py' and then restart goldy.")
            return False

    @staticmethod
    async def log_error(ctx=None, client=goldy_cache.client, error=None, command_name=None): #Goldy Bot Error reporter. This handles reporting the error to the member and master.
        await goldy_error.log(ctx, client, error, command_name) #Redirecting to the new error handler. I left this old function as an aliases as removing it will break all of goldy bot and 
                                                                    #to save time going through every piece of code

class guild_func():
    class server_icon():

        @staticmethod
        async def get(ctx, client): #Get guild icon.
            try:
                server_icon = ctx.guild.icon.url
            except AttributeError as e:
                try:
                    server_icon = client.user.display_avatar.url
                except AttributeError as e:
                    server_icon = "https://htmlcolors.com/color-image/2f3136.png"
                    pass

            return server_icon

    

class goldy_methods(): #Useful methods.

    class dict():
        @staticmethod
        async def merge(dict1, dict2):
            res = {**dict1, **dict2}
            return res

    class ctx_merger():
        @staticmethod
        async def merge(ctx, target_member_obj): #Creates a ctx object for mentioned members, just pass the member object.
            temp_ctx = ctx #Temporary storing ctx.

            target_member_ctx = ctx #Set overwriten ctx to it's own varible.
            target_member_ctx.author = target_member_obj #Overwriting ctx.author to create a ctx for the target member.

            executer_ctx = temp_ctx

            return (executer_ctx, target_member_ctx)

class antispam():
    class file():
        @staticmethod
        async def read(counter, message): #Reads antispam txt.
            with open("anti_spam.txt", "r+") as file: #Reads anti_spam.tx
                for lines in file:
                    if lines.strip("\n") == str(message.author.id):
                        counter += 1

                file.writelines(f"{str(message.author.id)}\n")

            return counter

class servers():
    class cogs():
        #'[]' means none.
        #'[""]' means all.

        @staticmethod
        def is_allowed(guild_id, cog_name, server_info=None): #Checks if discord server allows the cog.

            if server_info == None: #If server info was not given get the info.
                server_info = servers.get(guild_id)
            
            if cog_name == None: #Just return none if cog_name is None.
                return None

            if cog_name == "core":
                return True

            try:
                cog_allowed = True

                allowed_cogs = server_info.config.allowed_cogs
                disallowed_cogs = server_info.config.disallowed_cogs

                #Convert whole list into lower case.
                allowed_cogs_temp = []
                disallowed_cogs_temp = []
                for cog in allowed_cogs:
                    allowed_cogs_temp.append(cog.lower())
                for cog in disallowed_cogs:
                    disallowed_cogs_temp.append(cog.lower())

                #Delete and replace.
                del allowed_cogs
                del disallowed_cogs
                allowed_cogs = allowed_cogs_temp
                disallowed_cogs = disallowed_cogs_temp

                if not disallowed_cogs == []:
                    if cog_name.lower() in disallowed_cogs: #If cog in list return immediately.
                        return False

                    if disallowed_cogs == ["."]:
                        cog_allowed = False

                if not allowed_cogs == []:
                    if cog_name.lower() in allowed_cogs: #If cog in list return True immediately.
                        return True

                    if allowed_cogs == ["."]:
                        cog_allowed = True
                    
                return cog_allowed

            except Exception as e:
                goldy_func.print_and_log("warn", "Error exception in 'cogs.is_allowed' function.")
                goldy_func.print_and_log("error", e)

    class logging():
        class errors():

            @staticmethod
            async def is_allowed(server_info): #Checks if discord server allows error logging.
                try:
                    is_allowed = server_info.config.allow_error_logging
                except AttributeError as e:
                    return False
        
                return is_allowed

    class bad_characters():
        @staticmethod
        async def get(server_info):
            server_code_name = server_info.names.code_name
            
            try:
                f = open (f'./config/{server_code_name}/badwords.json', "r")
                guild_badwords_json = json.loads(f.read())

            except FileNotFoundError as e:
                goldy_func.print_and_log("warn", f"'badwords.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()

                f = open (f'./config/{server_code_name}/badwords.json', "r")
                guild_badwords_json = json.loads(f.read())

            try:
                f = open(f"./config/global/badwords.json", "r")
                global_badwords_json = json.loads(f.read())

            except FileNotFoundError as e:
                goldy_func.print_and_log("warn", f"'badwords.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()

                f = open (f"./config/global/badwords.json", "r")
                global_badwords_json = json.loads(f.read())

            combinded_list = global_badwords_json["bad_characters"] + guild_badwords_json["bad_characters"]
            return combinded_list

        @staticmethod
        async def is_allowed(server_info):
            try:
                is_allowed = server_info.config.allow_bad_characters
            except AttributeError as e:
                return False
    
            return is_allowed

    class bad_words():

        @staticmethod
        async def get(server_info): #Get's global badwords and additional badwords from guild. (Called when want list of disallowed words.)
            server_code_name = server_info.names.code_name
            
            try:
                f = open (f'./config/{server_code_name}/badwords.json', "r")
                guild_badwords_json = json.loads(f.read())

            except FileNotFoundError as e:
                goldy_func.print_and_log("warn", f"'badwords.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()

                f = open (f'./config/{server_code_name}/badwords.json', "r")
                guild_badwords_json = json.loads(f.read())

            try:
                f = open(f"./config/global/badwords.json", "r")
                global_badwords_json = json.loads(f.read())

            except FileNotFoundError as e:
                goldy_func.print_and_log("warn", f"'badwords.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()

                f = open (f"./config/global/badwords.json", "r")
                global_badwords_json = json.loads(f.read())

            combinded_list = global_badwords_json["badwords"] + guild_badwords_json["badwords"]
            return combinded_list

        @staticmethod
        async def is_allowed(server_info):
            try:
                is_allowed = server_info.config.allow_bad_words
            except AttributeError as e:
                return False
    
            return is_allowed

    class prefix():

        @staticmethod
        def get(client, message): #Get's prefix of guild.
            try:
                server_info = servers.get(message.guild.id)
                prefix = server_info.prefix
                return prefix
            except AttributeError as e:
                return "!"

    class checks():
        @staticmethod
        async def is_plus_guild(ctx):
            if ctx.channel.guild.id in config.GOLDY_PLUS_GUILDS:
                return True
            else:
                return False

    class hidden_cogs():
        @staticmethod
        async def get(ctx):
            server_data = servers.get(ctx.guild.id)

            try:
                return server_data.config.hidden_cogs
            except AttributeError:
                return None

    class channels():
        @staticmethod
        async def get(ctx, channel_name:str): #Finds the id of a specified channel in the guild's config (servers.json).
            server_info = servers.no_format.get(ctx.guild.id)
            try:
                if not server_info["channels"][channel_name] in ["", None]:
                    return server_info["channels"][channel_name] #Returns id.
            except KeyError as e:
                goldy_func.print_and_log("warn", f"servers.channels.get function couldn't find the channel '{channel_name}' in '{server_info['names']['code_name']}'s channels dict so we returned false.")
                return False

    @staticmethod
    def get(guild_id): #The "get" function here is used to find a server in the servers.json using the guild id. (Used to get config settings of the server a command was executed from.) (THIS function is to not be awaited.)
        try:
            f = open ('./config/servers.json', "r", encoding="utf8")
            servers_json = json.loads(f.read())
            
            for server in servers_json: #Loop through all servers in json.
                if servers_json[server]["id"] == guild_id: #If server id matches with the wanted id, return the server dict.

                    server_json = json.dumps(servers_json[server])
                    server_info = json.loads(server_json, object_hook=lambda d: SimpleNamespace(**d))
                    
                    return server_info #Returns the json but as python dict so you can easily pick the data.

            return False #Returns false if server was not found.

        except FileNotFoundError:
            f = open("./config/servers.json", "x", encoding="utf8") #Creating the json file here.
            f = open("./config/servers.json", "w", encoding="utf8") #Now I'm opening it as write.

            json.dump(settings.servers_example_layout, f) #Dumping the example layout in the json file.
            
            goldy_func.print_and_log("warn", "'./config/servers.txt' did not exist so we created the file for you with an example, now please configurate it to your likeing and run 'bot.py' again.")

    class no_format():
        @staticmethod
        def get(guild_id): #Exactly like the other get function above me but I return the data unformated.
            try:
                f = open ('./config/servers.json', "r", encoding="utf8")
                servers_json = json.loads(f.read())
                
                for server in servers_json: #Loop through all servers in json.
                    if servers_json[server]["id"] == guild_id: #If server id matches with the wanted id, return the server dict.
                        return servers_json[server] #Returns the json.

                return False #Returns false if server was not found.

            except FileNotFoundError:
                f = open("./config/servers.json", "x", encoding="utf8") #Creating the json file here.
                f = open("./config/servers.json", "w", encoding="utf8") #Now I'm opening it as write.

                json.dump(settings.servers_example_layout, f) #Dumping the example layout in the json file.
                
                goldy_func.print_and_log("warn", "'./config/servers.txt' did not exist so we created the file for you with an example, now please configurate it to your liking and run 'bot.py' again.")

    @staticmethod
    async def get_name(ctx): #This method returns the discord guild display name.add()
        server_data = servers.get(ctx.guild.id)

        if not server_data.names.server_name in ["", None]:
            return server_data.names.server_name
        else:
            return ctx.guild.name

    @staticmethod
    async def get_icon(ctx, client=goldy_cache.client):
        try:
            server_icon = ctx.guild.icon.url
        except AttributeError as e:
            try:
                server_icon = client.user.display_avatar.url
            except AttributeError as e:
                server_icon = "https://htmlcolors.com/color-image/2f3136.png"
                pass

        return server_icon

    class money_emoji():
        @staticmethod
        async def get(ctx): #This method returns the guild's money emoji.
            server_data = servers.get(ctx.guild.id)

            if not server_data.config.money_emoji in ["", None]:
                return server_data.config.money_emoji
            else:
                return "💷"

    @staticmethod
    #Function that checks if a server was added to servers.json, creates config
    async def update(): # folder for the server and creates a database for it.                    
        import cogs.database as database
        database = database.database

        new_server_found = False

        try:
            f = open ('./config/servers.json', "r")
            servers_json = json.loads(f.read())
            
            for server in servers_json: #Loop through all servers in json.
                if not server in os.listdir("config/"):
                    goldy_func.print_and_log("info_2", "New Server found in 'servers.json'. Creating folder...")
                    
                    #Creating server folder.
                    goldy_func.create_folder(f"./config/{server}")

                    #Create and write to items.json
                    f = open(f"./config/{server}/items.json", "x")
                    f = open(f"./config/{server}/items.json", "w")

                    items_layout = {"commands": {"list":[]}, "roles": {"list":[]}, "colours": {"list":[]}}
                    json.dump(items_layout, f) #Dumping the example layout in the json file.

                    #Create and write to badwords.json
                    badwords_file = open(f"./config/{server}/badwords.json", "x")
                    badwords_file = open(f"./config/{server}/badwords.json", "w")

                    json.dump({"badwords":[], "bad_characters":[]}, badwords_file) #Dumping the example layout in the json file.

                    #Add server to database.
                    await database.guild.create(server)

                    new_server_found = True

                if not f"{server} (server)" in await database.guild.list():
                    goldy_func.print_and_log("info", "A server in 'servers.json' did not have a collection in the database, creating one right now.")
                    await database.guild.create(server)

                    new_server_found = True

            if not "global" in os.listdir("config/"): #Checks if global folder is in config.
                goldy_func.create_folder(f"./config/global")

                #Create and write to items.json
                f = open(f"./config/global/items.json", "x")
                f = open(f"./config/global/items.json", "w")

                items_layout = {"commands": {"list":[]}, "colours": {"list":[]}}
                json.dump(items_layout, f) #Dumping the example layout in the json file.

                #Create and write to badwords.json
                badwords_file = open(f"./config/global/badwords.json", "x")
                badwords_file = open(f"./config/global/badwords.json", "w")
                
                json.dump({"badwords":[], "bad_characters":[]}, badwords_file) #Dumping the example layout in the json file.

            #Check if "level_up_msgs.json" is in config.
            if not "level_up_msgs.json" in os.listdir("config/"):
                #Create and write to level_up_msgs.json
                level_up_msgs_file = open(f"./config/level_up_msgs.json", "x")
                level_up_msgs_file = open(f"./config/level_up_msgs.json", "w")
                
                json.dump({"1" : {"msg": "**😊 Congrats! You've leveled up!**", 
                "gif_url" : "https://c.tenor.com/E5NzfAAtVFoAAAAi/girl--cute.gif", 
                "msg_creator_id" : 332592361307897856}}, level_up_msgs_file) #Dumping the example layout in the json file.

            #Check if "level_up_msgs.json" is in config.
            if not "level_rewards.json" in os.listdir("config/"):
                #Create and write to level_up_msgs.json
                level_rewards_file = open(f"./config/level_rewards.json", "x")
                level_rewards_file = open(f"./config/level_rewards.json", "w")
                
                json.dump({"{level_num_here}" : {"money" : 200, "exp" : 10}}, level_rewards_file) #Dumping the example layout in the json file.

            return new_server_found

        except FileNotFoundError:
            f = open("./config/servers.json", "x") #Creating the json file here.
            f = open("./config/servers.json", "w") #Now I'm opening it as write.

            json.dump(settings.servers_example_layout, f) #Dumping the example layout in the json file.
            
            goldy_func.print_and_log("warn", "'config/servers.txt' did not exist so we created the file for you with an example, now please configurate it to your likeing and run 'bot.py' again.")

            return False