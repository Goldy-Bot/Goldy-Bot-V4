from __future__ import annotations
from typing import Dict, List
from functools import wraps

import GoldyBot

# Adding events to GoldyBot YAY!!!
# -----------------------------------
def on_join():
    """Event that triggers when a member joins, uwu."""
    def decorator(func):
        @wraps(func)
        def wrapper():
            GoldyBot.cache.main_cache_dict["events"]["on_join"].append(func)
        
        return wrapper()
    return decorator

def on_leave():
    """Event that triggers when a member leaves."""
    def decorator(func):
        @wraps(func)
        def wrapper():
            GoldyBot.cache.main_cache_dict["events"]["on_leave"].append(func)
        
        return wrapper()
    return decorator


class Events():
    def __init__(self) :
        pass

    async def __trigger_functions(self, event_code_name:str, **args_to_pass_to_func):
        for function in GoldyBot.cache.main_cache_dict["events"][f"{event_code_name}"]:
        
            # The function is in a class/maybe extension.
            if list(function.__code__.co_varnames)[0] == "self":
                await function(
                    GoldyBot.cache.FindExtensions().find_object_by_extension_name(extension_name=str(function).split(" ")[1].split(".")[0]), 
                    **args_to_pass_to_func
                )
            
            else:
                await function(**args_to_pass_to_func)


    def register_all_nextcord_events(self):
        client = GoldyBot.cache.client()

        @client.event
        async def on_member_join(member:GoldyBot.nextcord.Member):
            member = GoldyBot.Member(ctx=None, member_object=member)

            await self.__trigger_functions("on_join", member=member)

        @client.event
        async def on_member_remove(member:GoldyBot.nextcord.Member):
            member = GoldyBot.Member(ctx=None, member_object=member)

            await self.__trigger_functions("on_leave", member=member)
