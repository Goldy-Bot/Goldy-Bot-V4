from __future__ import annotations
from typing import Dict, List
from functools import wraps

import GoldyBot

class Events:
    """The class that holds all event decorators in GoldyBot, a instance of this should exist in goldy cache."""
    # Adding events to GoldyBot YAY!!!
    def __init__(self):
        pass
    
    @staticmethod
    def on_join():
        """Event that triggers when a member joins, uwu."""

        def decorator(func):
            @wraps(func)
            def wrapper():
                GoldyBot.cache.main_cache_dict["events"]["on_join"].append(func)
                return "uwu"
            
            return wrapper()
        return decorator

def __register_all_nextcord_events():
    client = GoldyBot.cache.client()

    @client.event
    async def on_member_join(member:GoldyBot.nextcord.Member):
        member = GoldyBot.Member(ctx=None, member_object=member)

        for function in GoldyBot.cache.main_cache_dict["events"]["on_join"]:
            
            # The function is in a class/maybe extension.
            if list(function.__code__.co_varnames)[0] == "self":
                await function(
                    GoldyBot.cache.FindExtensions().find_object_by_extension_name(extension_name=str(function).split(" ")[1].split(".")[0]), 
                    member
                )
            
            else:
                await function(member)
