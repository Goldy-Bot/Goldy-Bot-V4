import json
import GoldyBot
import pprint

from GoldyBot.errors import ModuleFailedToLoad, ModuleNotFound

class Admin(GoldyBot.Extenstion):
    def __init__(self):
        super().__init__(self)

    def loader(self):
        
        @GoldyBot.command(required_roles=["bot_dev"])
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

        @GoldyBot.command(required_roles=["bot_dev"])
        async def reload(self:Admin, ctx, module_name:str):
            embed = GoldyBot.utility.goldy.embed.Embed()
            embed.color = GoldyBot.utility.goldy.colours.PURPLE

            module_name = module_name.lower()
            if module_name.endswith(".py"):
                module_name = module_name[:-3]

            if module_name == "admin":
                embed.title = self.msg.reload.AdminCanNotBeReloadedEmbed.title
                embed.description = self.msg.reload.AdminCanNotBeReloadedEmbed.des.format(module_name)
                embed.color = self.msg.reload.AdminCanNotBeReloadedEmbed.colour
                await ctx.send(embed=embed)
                return False

            try:
                module = GoldyBot.modules.Module(module_file_name = module_name + ".py")
            except ModuleNotFound:
                embed.title = self.msg.reload.ModuleNotFoundEmbed.title
                embed.description = self.msg.reload.ModuleNotFoundEmbed.des.format(module_name)
                embed.color = self.msg.reload.ModuleNotFoundEmbed.colour
                await ctx.send(embed=embed)
                return False
            
            try:
                module.reload()
            except ModuleFailedToLoad:
                embed.title = self.msg.reload.FailedToLoadEmbed.title
                embed.description = self.msg.reload.FailedToLoadEmbed.des.format(module.name)
                embed.color = self.msg.reload.FailedToLoadEmbed.colour
                await ctx.send(embed=embed)
                return False

            embed.title = self.msg.reload.ReloadedEmbed.title
            embed.description = self.msg.reload.ReloadedEmbed.des.format(module.name)
            embed.color = self.msg.reload.ReloadedEmbed.colour
            embed.set_thumbnail(url=self.msg.reload.ReloadedEmbed.thumbnail)
            await ctx.send(embed=embed)
            return True

        @GoldyBot.command(required_roles=["bot_dev"])
        async def unload(self:Admin, ctx, module_name:str):
            command_msg = self.msg.unload
            embed = GoldyBot.utility.goldy.embed.Embed()
            embed.color = GoldyBot.utility.goldy.colours.GREY
            module_name = module_name.lower()

            if module_name.endswith(".py"):
                module_name = module_name[:-3]

            if module_name == "admin":
                embed.title = command_msg.AdminCanNotBeUnloadedEmbed.title
                embed.description = command_msg.AdminCanNotBeUnloadedEmbed.des.format(module_name)
                embed.color = command_msg.AdminCanNotBeUnloadedEmbed.colour
                await ctx.send(embed=embed)
                return False

            try:
                module = GoldyBot.modules.Module(module_file_name = module_name + ".py")
            except ModuleNotFound:
                embed.title = command_msg.ModuleNotFoundEmbed.title
                embed.description = command_msg.ModuleNotFoundEmbed.des.format(module_name)
                embed.color = command_msg.ModuleNotFoundEmbed.colour
                await ctx.send(embed=embed)
                return False
            
            module.unload()

            embed.title = command_msg.UnloadedEmbed.title
            embed.description = command_msg.UnloadedEmbed.des.format(module.name)
            embed.color = command_msg.UnloadedEmbed.colour
            embed.set_thumbnail(url=self.msg.reload.ReloadedEmbed.thumbnail)
            await ctx.send(embed=embed)
            return True

def load():
    Admin()