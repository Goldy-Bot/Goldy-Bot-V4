import datetime
import nextcord
from nextcord import member
from nextcord import message
from nextcord.ext import commands
import asyncio
import importlib

from . import database
from ...GoldyBotV3.src import goldy_error, goldy_func, goldy_cache, goldy_utility
from ...GoldyBotV3.src.utility import cmds, members
from ...GoldyBotV3.src.utility import msg
from ...GoldyBotV3 import settings

cog_name = "rgb"

class rgb(commands.Cog, name="🏮RGB MODE"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = None #The position this cog will be placed in the help command.

        importlib.reload(msg)

    @commands.command(description="🎮 True gamers know what this amazing command does.")
    @commands.cooldown(1, 1.8, commands.BucketType.user)
    async def rgb(self, ctx, para_1=None):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            if await database.database.member.checks.has_item(ctx, "!rgb"):
                if not para_1 == None:
                    is_done = await rgb.member.toggle(ctx, para_1.lower())
                    if is_done[0] == True:
                        if is_done[1] == "on":
                            await ctx.send(msg.rgb.toggle_on.format(ctx.author.mention))
                        
                        if is_done[1] == "off":
                            await ctx.send(msg.rgb.toggle_off.format(ctx.author.mention))

                    else:
                        await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!rgb {on/off}"))

                else:
                    member_data = await database.database.member.pull(ctx)
                    rgb_ = await rgb.member.get(ctx, member_data)

                    if rgb_: await ctx.send(msg.rgb.rgb_mode_is_on.format(ctx.author.mention))
                    else: await ctx.send(msg.rgb.rgb_mode_is_off.format(ctx.author.mention))

            else:
                await ctx.send(msg.error.do_not_have_item.format(ctx.author.mention))

    @rgb.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.rgb")


    class member():
        @staticmethod
        async def toggle(ctx, on_off:str): #Toggles rgb on or off.
            member_data = await database.database.member.pull(ctx)
            
            if on_off.lower() == "on":
                try:
                    member_data.rgb = True
                    await database.database.member.push(ctx, member_data)
                    return (True, "on")
                except AttributeError as e:
                    await database.database.member.add_object(ctx, "rgb", True)
                    return (True, "on")

            if on_off.lower() == "off":
                try:
                    member_data.rgb = False
                    await database.database.member.push(ctx, member_data)
                    return (True, "off")
                except AttributeError as e:
                    await database.database.member.add_object(ctx, "rgb", False)
                    return (True, "off")

            return (False, None)

        @staticmethod
        async def get(ctx, member_data): #Get's the "rgb" object from the member data.
            try:
                rgb = member_data.rgb #The new object name.
                return rgb
            except AttributeError:
                await database.database.member.add_object(ctx, "rgb", False)
                return False

    class rgb_embed():
        def __init__(self, ctx, embed, ending_colour=0xF6FF00, msg=None):
            self.ctx = ctx
            self.embed:nextcord.Embed = embed
            self.message = msg
            self.rgb_gradient_colors = colours.rgb_gradient_colors
            self.rgb_gradient_colors.append(ending_colour)
            self.embed_list = []
            
        async def create_embeds(self): #Creates embed for each colour.
            for colour_ in self.rgb_gradient_colors:
                new_embed = self.embed.copy()
                new_embed.colour = colour_

                self.embed_list.append(new_embed)

        async def switch(self, embed): #Switch to that embed.
            if self.message == None:
                self.message = await self.ctx.send(embed=embed)
            else:
                await self.message.edit(embed=embed)

        async def start(self): #Starts the cycle of colours.
            for embed_ in self.embed_list:
                await self.switch(embed_)
                await asyncio.sleep(0.6)

class colours: #RGB Colours Cycle Settings
    Yellowish = 0xF6FF00
    Greenish = 0xAEFF00
    Green = 0x2EFF00
    Light_Greenish = 0x00FF70
    Light_Blue = 0x00FFC1
    Sky_Blue = 0x00C5FF
    Blue = 0x0087FF
    Even_More_Blue = 0x0032FF
    Even_Even_More_Blue = 0x1700FF
    Purple = 0x6C00FF
    Still_Purpleish = 0x9700FF
    Pinkish = 0xE800FF
    Pink = 0xFF00B6
    Redish_Pink = 0xFF006C
    Redish = 0xFF003A
    Red = 0xFF0000
    Orangeish = 0xFF5900
    Still_Orangeish = 0xFF9B00

    rgb_gradient_colors = [Yellowish, Greenish, Green, Light_Greenish, Light_Blue, Sky_Blue, Blue, 
    Even_More_Blue, Even_Even_More_Blue, Purple, Still_Purpleish, Pinkish, Pink, Redish_Pink, 
    Redish, Red, Orangeish, Still_Orangeish]

def setup(client):
    client.add_cog(rgb(client))
