from src.goldy_func import print_and_log, Merge
from src.goldy_utility import *
import src.utility.msg as msg
import settings

from cogs.database import database

class guild(): #Class for all methods for a guild ranks leaderboard.

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

            if await guild.max_lb_display.checks.is_available(server_info):
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
    async def get(ctx): #Returns rank and exp of all member's in order of exp.
        guild_member_data = await database.guild.pull(ctx)

        list = []
        for member in guild_member_data:
            if member["_id"] == 1:
                pass
            else:
                dict_1 = member[str(member["_id"])]
                dict_2 = {"_id": member["_id"]}

                list.append(Merge(dict(dict_1), dict_2))

        sort_ranking = sorted(list, key=lambda x: x["exp"], reverse=True)
        return sort_ranking

    @staticmethod
    async def create(ctx, client, data): #Create guild leaderboard.
        server_info = servers.get(ctx.guild.id)
        leaderboard_context = ""
        num = 0
        list_index = 0
        
        max_display_num = await guild.max_lb_display.get(server_info)
        if max_display_num > len(data):
            max_display_num = len(data)

        for num in range(0, max_display_num):
            num += 1
            member_obj = await client.fetch_user(data[list_index]["_id"])
            leaderboard_context += f"**• ``{num}#`` {await guild.hearts.get(num)}{member_obj.mention} - (🏷️:``{data[list_index]['rank']}`` ✨:``{data[list_index]['exp']}``)**\n"
            
            list_index += 1

        rank_num = await guild.member.ranking_num.get(ctx.author.id, data)
        leaderboard_context += f"\n{msg.lb.ranks.embed.your_ranking.format(ctx.author.mention, rank_num)}"

        embed = nextcord.Embed(title="**__🏆 Guild Leaderboard__**", description=leaderboard_context, colour=settings.AKI_ORANGE)

        server_icon = await servers.get_icon(ctx, client)
        server_name = await servers.get_name(ctx)
        embed.set_author(name=f"{server_name} - ✨Ranks", url=settings.github_page, icon_url=server_icon)
        embed.set_thumbnail(url=server_icon)
        embed.set_footer(text=msg.lb.ranks.footer)

        return embed