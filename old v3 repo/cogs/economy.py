import nextcord
from nextcord.ext import commands
import asyncio
import datetime
import importlib

from src.goldy_func import *
from src.goldy_utility import *
import src.utility.msg as msg

from src.utility import members
from cogs import rgb, database

#Change 'your_cog' to the name you wish to call your cog. ('your_cog' is just a placeholder.)
cog_name = "economy"

class economy(commands.Cog, name="💶Economy"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = None

        importlib.reload(msg)

    @commands.command(aliases=['balence', 'bank'], description="Displays your current balance.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bal(self, ctx, target_member: nextcord.Member = None):
        if await can_the_command_run(ctx, cog_name) == True:
            if target_member == None:
                member_data = await database.database.member.pull(ctx)
                member_bank_info = await economy.member.get(ctx, self.client, member_data)

                member_bal = member_bank_info[0]
                member_bal = '{:.2f}'.format(round(member_bal, 2))
                account_num = member_bank_info[1]
                net_worth = member_bank_info[2]

                #Get money emoji.
                server_info = servers.get(ctx.guild.id) #Getting server info.
                money_emoji = server_info.config.money_emoji #Grabbing emoji

                description_message = ((msg.bal.embed.main_context).format(ctx.author.mention, money_emoji, member_bal, account_num, net_worth))
                title_message = f"💛 Your Balence!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.YELLOW)
                embed.set_footer(text=msg.bal.embed.footer_context)

                user_avatar = await members.profile.icon.get(ctx)
                embed.set_thumbnail(url=user_avatar)

                msg_ = await ctx.send(embed=embed)

                #RGB MODE
                if await rgb.rgb.member.get(ctx, member_data):
                    rgb_embed = rgb.rgb.rgb_embed(ctx, embed, settings.YELLOW, msg_)
                    await rgb_embed.create_embeds()
                    await rgb_embed.start()

            if not target_member == None:
                (ctx, member_ctx) = await goldy_methods.ctx_merger.merge(ctx, target_member)
                member_data = await database.database.member.pull(member_ctx)

                member_bank_info = await economy.member.get(member_ctx, self.client, member_data)

                member_bal = member_bank_info[0]
                member_bal = '{:.2f}'.format(round(member_bal, 2))
                account_num = member_bank_info[1]
                net_worth = member_bank_info[2]

                #Get money emoji.
                server_info = servers.get(member_ctx.guild.id) #Getting server info.
                money_emoji = server_info.config.money_emoji #Grabbing emoji

                description_message = ((msg.bal.embed.main_context).format(member_ctx.author.mention, money_emoji, member_bal, account_num, net_worth))
                title_message = f"💜 Their Balence!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.PURPLE)
                embed.set_footer(text=msg.bal.embed.footer_context)

                user_avatar = await members.profile.icon.get(ctx)
                embed.set_thumbnail(url=user_avatar)

                msg_ = await member_ctx.send(embed=embed)

                #RGB MODE
                if await rgb.rgb.member.get(member_ctx, member_data):
                    rgb_embed = rgb.rgb.rgb_embed(member_ctx, embed, settings.PURPLE, msg_)
                    await rgb_embed.create_embeds()
                    await rgb_embed.start()

    @bal.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy.log_error(ctx, self.client, error, "economy.bal")

    class member():
        
        @staticmethod
        async def get(ctx, client, member_data=None):
            from cogs.database import database
            if member_data == None:
                member_data = await database.member.pull(ctx)
            member_bal = member_data.goldCoins
            account_num = member_data.accountNum
            net_worth = await members.networth.get(ctx, member_data)

            return member_bal, account_num, net_worth

        @staticmethod
        async def add(ctx, client, amount): #Adds currency to member.
            from cogs.database import database

            member_data = await database.member.pull(ctx) #Pull member data.

            member_bal = member_data.goldCoins
            new_bal = member_bal + amount
            member_data.goldCoins = new_bal

            await database.member.push(ctx, member_data) #Push member data back.
            print_and_log(None, f"[{cog_name.upper()}] Added {amount} to {ctx.author}'s bank.")

            return new_bal

        @staticmethod
        async def subtract(ctx, client, amount): #Subtracts currency from member.
            from cogs.database import database
            member_data = await database.member.pull(ctx) #Pull member data.

            member_bal = member_data.goldCoins
            new_bal = member_bal - amount

            if new_bal < -1:
                return False

            if not new_bal < -1:
                member_data.goldCoins = new_bal
                await database.member.push(ctx, member_data) #Push member data back.
                print_and_log(None, f"[{cog_name.upper()}] Removed {amount} from {ctx.author}'s bank.")

            return new_bal



def setup(client):
    client.add_cog(economy(client))

#Need Help? Check out this: {youtube playlist}