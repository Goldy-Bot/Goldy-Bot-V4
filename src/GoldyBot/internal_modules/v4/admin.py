import json
import GoldyBot
import pprint

class Admin(GoldyBot.Extenstion):
    def __init__(self):
        super().__init__(self)

        self.msg = GoldyBot.utility.msgs

    def loader(self):
        
        @GoldyBot.command()
        async def cache(self:Admin, ctx):
            cache_embed = GoldyBot.utility.goldy.embed.Embed(title=self.msg.cache.Embed.title)
            cache_embed.color = GoldyBot.utility.goldy.colours.BLUE

            cache_string_formatted = pprint.pformat(GoldyBot.cache.main_cache_dict, indent=2)

            if len(cache_string_formatted) >= 5000:
                cache_embed.description = "Oh oh, the cache is way too long to display in an embed right now. I'll print it in the console instead."
                await ctx.send(embed=cache_embed)

                GoldyBot.logging.log("info", cache_string_formatted)
            else:
                cache_embed.description = f"```{cache_string_formatted}```"
                await ctx.send(embed=cache_embed)

        @GoldyBot.command()
        async def reload(self:Admin, ctx, module_name:str):
            module = GoldyBot.modules.Module(module_file_name = module_name + ".py")
            module.reload()
            
            await ctx.send(f"Reloaded {module.name}!")

def load():
    Admin()