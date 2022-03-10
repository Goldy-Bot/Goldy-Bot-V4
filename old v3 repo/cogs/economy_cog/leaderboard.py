from src.goldy_func import print_and_log, Merge
from src.goldy_utility import *
import src.utility.msg as msg
import settings

from cogs.database import database

class global_(): #Class for all methods for the global balance leaderboard.

    class member():
        class ranking_num():
            
            @staticmethod
            async def get(member_id, data):
                list_index = 0
                for member in data:
                    list_index += 1
                    if member["_id"] == member_id:
                        return list_index

    class max_lb_display():
        class checks():
            @staticmethod
            async def is_available(server_info):
                try:
                    max_lb_display = server_info.config.max_lb_display
                    if max_lb_display in ["", None]:
                        return False
                    return True
                except AttributeError as e:
                    print_and_log("no_guild_config_value", "max_lb_display", server_info.names.code_name)
                    return False

        @staticmethod
        async def get(server_info): #Get's the max amount members to display on leaderboard number from guild config.
            """
            "max_lb_display":15
            """

            if await global_.max_lb_display.checks.is_available(server_info):
                max_lb_display = server_info.config.max_lb_display
                return max_lb_display
            else:
                return 15

    class hearts():
        @staticmethod
        async def get(rank_num:int):
            if rank_num == 1:
                return "💛 "

            if rank_num == 2:
                return "💙 "

            if rank_num == 3:
                return "💜 "

            else:
                return ""

    @staticmethod
    async def get(): #Returns rank and exp of all member's in order of exp.
        global_member_data = await database.global_.pull()

        list = []
        for member in global_member_data:
            if member["_id"] == 1:
                pass
            else:
                dict_1 = member[str(member["_id"])]
                dict_2 = {"_id": member["_id"]}

                list.append(Merge(dict(dict_1), dict_2))

        sort_ranking = sorted(list, key=lambda x: x["goldCoins"], reverse=True)
        return sort_ranking

    @staticmethod
    async def create(ctx, client, data): #Create global  leaderboard.
        server_info = servers.get(ctx.guild.id)
        leaderboard_context = ""
        num = 0
        list_index = 0

        money_emoji = await servers.money_emoji.get(ctx)
        
        max_display_num = await global_.max_lb_display.get(server_info)
        if max_display_num > len(data):
            max_display_num = len(data)

        for num in range(0, max_display_num):
            num += 1
            member_obj = await client.fetch_user(data[list_index]["_id"])
            leaderboard_context += f"**• ``{num}#`` {await global_.hearts.get(num)}{member_obj.mention} - {money_emoji}``{data[list_index]['goldCoins']}``**\n"
            
            list_index += 1

        rank_num = await global_.member.ranking_num.get(ctx.author.id, data)
        leaderboard_context += f"\n{msg.lb.balance.embed.your_ranking.format(ctx.author.mention, rank_num)}"

        embed = nextcord.Embed(title="**🌍 __Global Leaderboard__**", description=leaderboard_context, colour=settings.YELLOW)

        server_icon = await servers.get_icon(ctx, client)
        server_name = await servers.get_name(ctx)
        embed.set_author(name=f"{server_name} - 💳Balance", url=settings.github_page, icon_url=server_icon)
        embed.set_thumbnail(url=server_icon)
        embed.set_footer(text=msg.lb.balance.footer)

        return embed

#So you are horny.