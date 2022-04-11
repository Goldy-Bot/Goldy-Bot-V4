import GoldyBot

def get_prefix(command):
    try:
        guild = GoldyBot.cache.main_cache_dict[] #TODO: Finish this!
        prefix = server_info.prefix
        return prefix
    except AttributeError as e:
        return "!"