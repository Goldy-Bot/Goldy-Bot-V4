import requests
import os
import random

from src.goldy_func import print_and_log, Merge
from src.goldy_utility import *
import src.utility.msg as msg
import settings

from . import endpoints
from config import config

API = "http://api.giphy.com/v1/gifs"
API_NAME = "Giphy"

async def request(web_dir, api_params: dict, ctx=None, client=None): #Main request funcion.
    main_header = {'User-Agent': str(settings.bot_name + config.bot_version)}

    main_payload = {'api_key': await api_key.get()}

    #Combing the extrat parameters with the main header.
    payload = Merge(main_payload, api_params)

    #Actual request.
    print_and_log(None, f"Requesting '{web_dir}'...")
    try:
        response = requests.get(API + web_dir, params=payload, headers=main_header)
        data = response.json()

        #Convert json to class and return.
        data_formatted = json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
        print_and_log("info_2", f"[DONE]")
        print_and_log()
        #return data_formatted
        return data

    except Exception as e:
        if not ctx == None:
            if not client == None:
                await goldy.log_error(ctx, client, f"{(msg.api).format(API_NAME)} >>> {e}\n DATA RETURNED BY API: {data}", None)
        print_and_log("error", f"[{API_NAME.upper()} : API] Request failed. >>> {e}\n DATA RETURNED BY API: {data}")

        return False


class gif():

    @staticmethod
    async def search(ctx, client, search_query): #Returns url to the first gif realated to that query. (This isn't a really good method, wouldn't recommend using it.)
        data = await request(endpoints.webdirs.search, {'q': search_query}, ctx, client)
        gif_url = data["data"][1]["images"]["original"]["url"]
        return gif_url

    @staticmethod
    async def all(ctx, client, search_query, return_limit : int=50): #Returns list of url's to all gifs realated to that query.
        data = await request(endpoints.webdirs.search, {'q': search_query, "limit": return_limit}, ctx, client)
        gifs = []
        for gif in data["data"]:
            gifs.append(gif["images"]["original"]["url"])

        return gifs

    @staticmethod
    async def random(ctx, client, search_tag, return_range : tuple): #Returns url of random gif related to the search tag.
        data = await request(endpoints.webdirs.search, {'q': search_tag}, ctx, client)

        a, b = return_range
        
        try:
            random_num = random.randint(a, b)
            gif_url = data["data"][random_num]["images"]["original"]["url"]
        except IndexError as e:
            try:
                random_num = random.randint(a, b)
                gif_url = data["data"][random_num]["images"]["original"]["url"]
            except IndexError as e:
                try:
                    random_num = random.randint(0, data["pagination"]["count"])
                    gif_url = data["data"][random_num]["images"]["original"]["url"]

                except IndexError as e:
                    print_and_log("error", f"[{API_NAME.upper()}] {e}")
                    gif_url = False

        return gif_url

class api_key():

    @staticmethod
    async def get(): #This method get's the secret key for use of the Giphy api.
        PATH = "config/giphy_api_key.txt"
        INFO = "Create a GIPHY API application if you would like to use the 'Gifs' API handler."
        no_exist_msg = "'{}' did not exist so we created the file for you, now if you would like to use 'gifs' pleasa enter a GIPHY API key."
        
        try:
            f = open(PATH, "r") #Opens text file containing bot token but creates if it doesn't exist.
            key = f.read()

            if key == "":
                print_and_log("warn", INFO)
                return False

            if key == "{ENTER GIPHY API KEY HERE}":
                print_and_log("warn", INFO)
                return False

            else:
                f.close()
                return str(key)

        except FileNotFoundError:
            f = open(PATH, "x")
            f = open(PATH, "w")
            f.write("{ENTER GIPHY API KEY HERE}")
            print_and_log("info", no_exist_msg.format(os.path.basename(PATH)))