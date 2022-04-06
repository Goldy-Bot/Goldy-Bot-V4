import nextcord
from nextcord.ext import commands
import asyncio
import datetime
import random

from ...GoldyBotV3.src.goldy_func import *
from ...GoldyBotV3.src.goldy_utility import *
from ...GoldyBotV3.src.utility import msg
from ...GoldyBotV3.src.utility import members as u_members

from . import shop, database, economy, rgb

cog_name = "rank_system"

class rank_system(commands.Cog, name="🔺Rank System"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 5

    @commands.command(aliases=["level", "exp", "xp"], description="Shows your current rank and exp.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rank(self, ctx, target_member: nextcord.Member = None):
        if await can_the_command_run(ctx, cog_name) == True:
            if target_member == None:
                member_data = await database.database.member.pull(ctx)
                member_rank_info = await rank_system.member.get(ctx, self.client, member_data)

                member_rank = member_rank_info[0]
                member_exp = member_rank_info[1]

                description_message = ((msg.rank.embed.main_context).format(ctx.author.mention, member_rank, member_exp))
                title_message = f"🧡 Your Rank!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.AKI_ORANGE)
                embed.set_footer(text=msg.rank.embed.footer_context)

                user_avatar = await u_members.profile.icon.get(ctx)
                embed.set_thumbnail(url=user_avatar)

                msg_ = await ctx.send(embed=embed)

                #RGB MODE
                if await rgb.rgb.member.get(ctx, member_data):
                    rgb_embed = rgb.rgb.rgb_embed(ctx, embed, settings.AKI_ORANGE, msg_)
                    await rgb_embed.create_embeds()
                    await rgb_embed.start()

            if not target_member == None: #Allows members to look at other members rank.
                (ctx, member_ctx) = await goldy_methods.ctx_merger.merge(ctx, target_member)

                member_data = await database.database.member.pull(member_ctx)
                member_rank_info = await rank_system.member.get(member_ctx, self.client, member_data)

                member_rank = member_rank_info[0]
                member_exp = member_rank_info[1]

                description_message = ((msg.rank.embed.main_context).format(member_ctx.author.mention, member_rank, member_exp))
                title_message = f"💙 Their Rank!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.AKI_BLUE)
                embed.set_footer(text=msg.rank.embed.footer_context)

                user_avatar = await u_members.profile.icon.get(ctx)
                embed.set_thumbnail(url=user_avatar)

                msg_ = await member_ctx.send(embed=embed)

                #RGB MODE
                if await rgb.rgb.member.get(member_ctx, member_data):
                    rgb_embed = rgb.rgb.rgb_embed(member_ctx, embed, settings.AKI_BLUE, msg_)
                    await rgb_embed.create_embeds()
                    await rgb_embed.start()

    @rank.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.rank")

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=['what-exp', 'what-xp'], description="Does the maths to find out how much exp you need to unlock a certain level.")
    async def what_exp(self, ctx, arg1:int=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if arg1 == None:
                await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!what-exp {level}"))

            if not arg1 == None:
                try:
                    exp = int(arg1) * 8 * int(arg1) + 25
                    await ctx.send("**🧡 {}, you will need ``{}`` exp to rank up to Level ``{}``**".format(ctx.message.author.mention, exp, arg1))
                except ValueError:
                    await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!what-exp {level}"))

    @what_exp.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.BadArgument, commands.CommandInvokeError, commands.ExpectedClosingQuoteError)):
            await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!what-exp {level}"))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.what_exp")

    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.command(aliases=['lb', 'lead'], description="The amazing leaderboard.")
    async def leaderboard(self, ctx, option=None):
        if await can_the_command_run(ctx, cog_name) == True:

            if option in ["rank", "exp", None]:
                import cogs.rank_system_cog.leaderboard as ranks_lb

                async with ctx.typing():
                    data = await ranks_lb.guild.get(ctx)
                embed = await ranks_lb.guild.create(ctx, self.client, data)
                await ctx.send(embed=embed)
                return

            if option in ["bal", "bank", "money"]:
                import cogs.economy_cog.leaderboard as balance_lb

                async with ctx.typing():
                    data = await balance_lb.global_.get()
                embed = await balance_lb.global_.create(ctx, self.client, data)
                await ctx.send(embed=embed)
                return

            await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!lb {option: rank/exp, bal/bank/money}"))

    @leaderboard.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.leaderboard")

    @commands.Cog.listener()
    async def on_message(self, message): #Runs when any message is sent in guild channels.
        ctx = message
        if await can_the_command_run(ctx, cog_name) == True:

            try:
                guild_id = ctx.guild.id
                is_guild = True
            except AttributeError as e:
                is_guild = False

            if is_guild == True:
                if not message.author.bot == True: #Checks if message isn't sent by a bot.
                    if not message.content.startswith("!") == True:
                        member_data = await database.database.member.pull(ctx)

                        exp_amount = 4
                        try: #If algorithum exsits, import it and use it.
                            from .ranks_system import secret_algorithm as secret
                            data = await secret.oh_yes_goldy_that_feels_good(message, member_data, cog_name) #Algorithm
                            member_data = data[0]
                            exp_amount = data[1]
                        except ImportError as e:
                            pass

                        await rank_system.member.exp.add(ctx, exp_amount)
                        
                        if await rank_system.member.checks.can_level_up(member_data):
                            #Rank up member
                            previous_rank = await rank_system.member.rank.add(ctx, 1)

                            #Give level role.
                            current_rank = (previous_rank + 1)

                            items_data = await shop.items.find(ctx)
                            level_roles_dict = await rank_system.member.level_roles.get(items_data)
                            
                            if not level_roles_dict == False:
                                version_to_use = await rank_system.servers.level_roles.which_version(level_roles_dict)
                                if version_to_use == "v1":
                                    await rank_system.member.level_roles.give(ctx, level_roles_dict, current_rank)
                                if version_to_use == "v2":
                                    await rank_system.member.level_roles.version_2.give(ctx, level_roles_dict, current_rank)

                            #Level up message.
                            await rank_system.embed.level_up_msg(ctx, self.client, current_rank, previous_rank)

                            #Give reward if there is one for the level.
                            data = await rank_system.member.rank_rewards.give(ctx, self.client, current_rank)

                            if (type(data) is tuple) == True:
                                try:
                                    money = data[0]
                                    exp = data[1]
                                except TypeError as e:
                                    pass

                                server_info = servers.get(ctx.channel.guild.id)
                                await rank_system.embed.reward_msg(ctx, server_info, money, exp)




    class member():
        class checks():
            @staticmethod
            async def can_level_up(member_data): #Checks if member can rank up at current exp level.
                next_level = member_data.rank + 1

                if member_data.exp > next_level * 8 * next_level + 25:
                    return True  
                else:
                    return False

        class level_roles():
            class version_2(): #A more advanced version of the level_roles give method.

                @staticmethod
                async def give(ctx, level_roles_dict:dict, current_rank): #Gives member the apropiate level up role and removes the old one.
                    if await servers.checks.is_plus_guild(ctx) == True: #Only works if guild is 'goldy plus' certificed.

                        #Get list and index of current rank.
                        index_of_current_rank = await rank_system.member.level_roles.version_2.list.find(current_rank, level_roles_dict["list"])

                        if not index_of_current_rank == False:

                            #Find out previous role with index of current rank.
                            previous_rank = level_roles_dict["list"][index_of_current_rank - 1]

                            #Find previous and current level role in guild.
                            current_rank_role = await rank_system.member.level_roles.version_2.find(ctx, current_rank)
                            previous_rank_role = await rank_system.member.level_roles.version_2.find(ctx, previous_rank)

                            #Give new member level role.
                            if not current_rank_role == False:
                                try:
                                    await ctx.author.add_roles(current_rank_role)
                                except Exception as e:
                                    pass
                            
                            #Remove previous level role from member.
                            if not previous_rank_role == False:
                                try:
                                    await ctx.author.remove_roles(previous_rank_role)
                                except Exception as e:
                                    pass

                            return True
                        
                        else:
                            return False

                class list():
                    @staticmethod
                    async def find(level:int, level_roles_list:list): #Finds level in level_roles list.
                        try:
                            index_num = level_roles_list.index(level)
                            return index_num
                        except ValueError as e:
                            return False

                @staticmethod
                async def find(ctx, rank): #Finds the level role by name and returns the object of the first role found.
                    guild_roles = ctx.guild.roles
                    for role in guild_roles:
                        if str(rank) in role.name:
                            return role

                    return False

            @staticmethod
            async def give(ctx, level_roles_dict:dict, current_rank): #Gives member the apropiate level up role and removes the old one.
                if await servers.checks.is_plus_guild(ctx) == True: #Only works if guild is 'goldy plus' certificed.
                    guild = ctx.channel.guild

                    #If current_rank rank lower than 5, do not minus 5 to find out previous_rank.
                    if current_rank <= 5:
                        previous_rank = (current_rank - 1)
                    else:
                        previous_rank = (current_rank - 5)

                    #If current_rank is in level_roles list try to give level role to member.
                    if current_rank in level_roles_dict["list"]:

                        #Give new level role.
                        try:
                            next_role = nextcord.utils.get(guild.roles,name=f"Level {current_rank}")
                            await ctx.author.add_roles(next_role)
                        except Exception as e:
                            pass
                        
                        #Remove previous level role.
                        try:
                            previous_role = nextcord.utils.get(guild.roles,name=f"Level {previous_rank}")
                            await ctx.author.remove_roles(previous_role)
                        except Exception as e:
                            pass
                        
                else:
                    return False

            @staticmethod
            async def get(items_data): #Returns '+level_roles' dict.
                try:
                    level_roles = items_data[1]["roles"]["+level_roles"]
                except KeyError as e:
                    return False

                return level_roles

        class rank_rewards():
            @staticmethod
            async def give(ctx, client, current_rank): #Attemps to give the member a reward for getting to that level if there is one.
                money = None
                exp = None

                #Get reward data.
                reward = await rank_system.member.rank_rewards.get(current_rank)
                if reward == None:
                    return False

                else:
                    #Give rewards.

                    try: #If reward countains money give the money.
                        money = reward.money
                        await economy.economy.member.add(ctx, client, int(money))
                    except AttributeError as e:
                        pass

                    try: #If reward countains exp give member the expirence.
                        exp = reward.exp
                        await economy.economy.member.add(ctx, client, int(exp))
                    except AttributeError as e:
                        pass

                return (money, exp)
            
            @staticmethod
            async def get(rank): #Returns dict of rewards for that level/rank. (Returns "None" if there is no rewards.)
                try:
                    f = open (f'config/level_rewards.json', "r", encoding="utf8")
                    level_rewards_normal = json.loads(f.read())

                except FileNotFoundError as e:
                    print_and_log("warn", f"'level_rewards.json' was not found. Running update function and trying again. >>> {e}")
                    await servers.update()

                    f = open (f'config/level_rewards.json', "r", encoding="utf8")
                    level_rewards_normal = json.loads(f.read())

                try:
                    rewards = json.dumps(level_rewards_normal[str(rank)])
                    rewards_formatted = json.loads(rewards, object_hook=lambda d: SimpleNamespace(**d))
                except KeyError as e: #Usally occures if rank has no rewards.
                    return None

                return rewards_formatted

        @staticmethod
        async def get(ctx, client, member_data=None): #Get's both the rank and exp of a member. (0 = rank, 1 = exp)
            if not member_data == None: member_data = await database.database.member.pull(ctx)

            member_rank = member_data.rank
            member_exp = member_data.exp

            return member_rank, member_exp

        class rank():
            @staticmethod
            async def add(ctx, amount: int): #Adds ranks to a member.
                member_data = await database.database.member.pull(ctx)

                previous_rank = member_data.rank
                member_data.rank = (member_data.rank + amount)
                await database.database.member.push(ctx, member_data)

                return previous_rank

            @staticmethod
            async def what_rank(member_data): #Checks what rank the member should be leveled up to acording to their exp.
                pass

        class exp():
            @staticmethod
            async def add(ctx, amount: int): #Adds exp to member.
                member_data = await database.database.member.pull(ctx) #Pull member data.

                member_exp = member_data.exp
                new_exp = member_exp + round(amount)
                member_data.exp = new_exp

                await database.database.member.push(ctx, member_data) #Push member data back.

                return new_exp

            @staticmethod
            async def subtract(ctx, amount: int): #Subtracts exp from member.
                member_data = await database.database.member.pull(ctx) #Pull member data.

                member_exp = member_data.exp
                new_exp = member_exp - round(amount)

                if new_exp < -1:
                    return False

                if not new_exp < -1:
                    member_data.goldCoins = new_exp
                    await database.database.member.push(ctx, member_data) #Push member data back.

                return new_exp

    class servers():
        class level_roles():
            
            @staticmethod
            async def which_version(level_roles): #Checks the guild's settings to see if it specifies to use any particular level_roles give method version.
                try:
                    version = level_roles["version_to_use"]
                except KeyError as e:
                    return "v1"

                if version.lower().replace(" ", "-") in ["v1", "version-1", "v-1", "version1"]:
                    return "v1"

                if version.lower().replace(" ", "-") in ["v2", "version-2", "v-2", "version2"]:
                    return "v2"

                return "v1"


    class random_level_up_msg():

        @staticmethod
        async def get(): #Get's random level up message from "level_up_msgs.json".
            try:
                f = open (f'config/level_up_msgs.json', "r", encoding="utf8")
                level_up_msgs_normal = json.loads(f.read())

            except FileNotFoundError as e:
                print_and_log("warn", f"'level_up_msgs.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()

                f = open (f'config/level_up_msgs.json', "r", encoding="utf8")
                level_up_msgs_normal = json.loads(f.read())


            max_msgs_num = len(level_up_msgs_normal.keys())
            random_num = random.randint(1, max_msgs_num) #Test to see what happends if max num is also 1.

            level_up_message = json.dumps(level_up_msgs_normal[str(random_num)])
            level_up_message_formatted = json.loads(level_up_message, object_hook=lambda d: SimpleNamespace(**d))

            return level_up_message_formatted

    class embed():
        @staticmethod
        async def reward_msg(ctx, server_info, money_rewarded, exp_rewarded):
            #Embed
            description_message = ((msg.rank_system.reward_embed.main_context).format(server_info.config.money_emoji, money_rewarded, exp_rewarded))
            embed = nextcord.Embed(title=(msg.rank_system.reward_embed.title).format(ctx.author.name), description=description_message, colour=settings.Aki_Pink)
            embed.set_footer(text=msg.footer.type_2)
            embed.set_thumbnail(url=msg.rank_system.reward_embed.embed_url)
            await ctx.channel.send(embed=embed)

        @staticmethod
        async def level_up_msg(ctx, client, current_rank, previous_level):
            #Get random Gif & Msg.
            level_up_message = await rank_system.random_level_up_msg.get()

            message_creator = await client.fetch_user(level_up_message.msg_creator_id)

            #Embed
            description_message = ((msg.rank_system.embed.level_up_context).format(ctx.author.mention, previous_level, current_rank))
            embed = nextcord.Embed(title=level_up_message.msg, description=description_message, colour=settings.AKI_RED)
            embed.set_footer(text=f"(⭐Message By '{message_creator.name}')")
            embed.set_thumbnail(url=level_up_message.gif_url)
            await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(rank_system(client))

#Need Help? Check out this: {youtube playlist}