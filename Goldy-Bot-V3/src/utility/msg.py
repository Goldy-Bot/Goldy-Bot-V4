class error():
    api = "❤️ Goldy Bot couldn't connect to the '{}' API."
    server_not_registered = "**❤️ This server is not registered. Please contact my Developer: Dev Goldy/The Golden Pro (https://github.com/THEGOLDENPRO)**"
    command_disabled_by_server = "**🧡 This command is disabled by the server owner.**"
    command_exception = "**❤️{}, sorry but somethings not right with me. I have reported my error to my master ({}) and he should fix it soon, hold on please.**"
    contact_dev = "Contact a Dev."
    not_available_yet = "**💗 Sorry we don't quite support that yet, we will try our best get this working.**"
    do_not_have_item = "**❤️ {}, you don't own this item, you may need to purchase it from the shop.**"
    member_not_found = "**❤️ {}, member not found. Did you type their name correctly.**"

    command_these_ranks_only = "**💛 {}, that command is exclusive only to the rank(s) {}.**"
    cooldown = "**❤️ Stop! I can't respound this quick with that command. Try again in __{}__**"

class help():
    command_usage = "***🧡 {}, COMMAND USAGE: ``{}``***"
    command_not_found= "**❤️ Could not find the command or cog named that.**"

    class embed():
        title = "💟 Help - {}"
        des = """
        *Welcome to the NEW and improved help command.*
        
        Tip: If you want more info you can also do: 
        ``!help {cog}``, ``!help {command name}``
        """

class footer():
    type_1 = "🧡 Goldy Bot, aki community's very own bot."
    type_2 = "(💖 Goldy Bot V3, the rewriten Goldy Bot that is better than ever!)"

    giphy = "💜 Powered By Giphy"

class images(): #Contains all the image url to images goldy bot uses.
    class other():
        url_1 = "https://media.discordapp.net/attachments/876976105335177286/888876180009263174/Untitled-1.png"
        url_2 = "https://media.discordapp.net/attachments/876976105335177286/888878455758913596/Untitled-1.png"

    class no_pfp():
        logo_1 = "https://media.discordapp.net/attachments/739827705960202362/909107629379452988/logo_v2.png"

class admin():
    help_layout = """
    **💚__ADMIN COMMAND: ``{}``__**
    {}
    """

    class read_cache():
        class embed():
            title = "**💙 Goldy Bot's Cache**"

        class error():
            class too_big_embed():
                title = "**❤️ Sent in console!**"
                des = "***The cache dictinary is too big to send through discord so I sent it in the console instead.***"

    class give():
        help_context = """
**•``!give {member} money {amount}`` --> Gives money to a member.**
**•``!give {member} rank {amount}`` --> Adds a rank to a member.**
**•``!give {member} exp {amount}`` --> Gives a member exp.**
**•``!give {member} {item}`` --> Gives item to a member.**
        """

        main_layout = "**💚 {}, gave {} __'{}'__!**"

    class take():
        help_context = """
**•``!take {member} money {amount}`` --> Takes money from a member.**
**•``!take {member} {item}`` --> Takes item from a member.**
        """

        main_layout = "**💚 {}, took __'{}'__ from {}!**"

class shop():
    page_out_of_range = "**❤️ {}, honey we don't have that many pages.**"

class rank_system():
    class embed():
        level_up_context = """
        • **{} Lvl Up:** ``{} >>> {}``
        """

    class reward_embed():
        title = "**🎉Yahoo! {}, you've been rewarded.**"

        main_context = """
        **Money: {}**``{}``
        **Exp: ✨**``{}``
        """

        embed_url = "https://i.imgur.com/pUkr6rm.gif"

class bal():
    class embed():
        main_context = """
        **__{}__ **
        
        **Balence: {}**``{}``
        **Credit Card: 💳**``{}``
        **Net Worth: **📈``{}`` *__(NEW)__*

        """

        footer_context = "Yes, I just revealed your credit card details!"

class rank():
    class embed():
        main_context = """
        **__{}__ **
        
        **Rank: 🏷️**``{}``
        **Exp: ✨**``{}``

        """

        footer_context = "Level up by having a convo with another user."

class nicking():
    class failed():
        bad_word = "**❤️🚫 {}, we detected a bad word within your nick. Please do not nick into those type of names.**"
        bad_character = "**💛🚫 {}, you can't have '{}' in your nick. Sorry.**"
        same_nick = "**💛🚫 {}, you can't nick as another member's name. Please don't nick as someone else.**"
        unable = "**❤️ {}, we are unable to change your name for some reason. I may not have perms or you may be server owner.**"
        no_point = "**💗 {}, there's no point updating your nick, if you have no role/rank that offers a prefix.**"

    class buttons():
        class embed():           
            title = "**🏷️ Pick the prefix you would like to have.**"
        
        confirming = "**💚 Okay Picking that as your prefix...**"
        timeout = "**🧡 {}, well it looks like that timed out. Run the nick command again to pick your prefix.**"

    class embed():
        nick_new_context = """
        **💜 {}, we updated your nick to your current discord username: ``{}`` **
        
        ***(We also have a command to change your nick: ``!nick {{nick name}}``) ***
        """

        nick_content = """
        **💛 {}, we updated your nick to ``{}`` **
        
        ***(We also have a command to reset your nick: ``!nick reset`` or ``!nick-new``) ***
        """


class buy():
    class failed():
        no_money = "**❤️ {}, you don't have enough currency.**"
        already_own = "**🧡 {}, you already own this item.**"
        no_exist = "**🧡 {}, this item doesn't exist or atleast doesn't exist on this server.**"
        role_conflict = "**❤️ {}, sorry role conflict rules. The role '{}' is stoping you from buying '{}'.**"

        there_not_buyable = "**💜 Umm, are you sure their buyable.**"

    class embed():
        item_context = """
        **{}, your "{}" purchase has been compleate.**
        **{}**

        **Item Price: {}**``{}``
        **Your Balence Now: {}**``{}``

        """

        colour_context = """
        **🍭 {}, your "{}" colour purchase has been compleate. To apply the colour type: ``!colour {}``**

        **Colour Price: {}**``{}``
        **Your Balence Now: {}**``{}``

        """

class sell():
    class failed():
        no_exist = "**🧡 {}, This item doesn't exist.**"
        not_sellable = "**💜 {}, this item is not sellable.**"
        do_not_have_item = "**❤️ {}, you don't have this item.**"
    
    class embed():
        main_context = """
        **{}, your "{}" has been sold for {}``{}``.**

        **Your Balence Now: {}**``{}``
        **Sell Tax: {}**``{}%``
        """

class lb():
    class ranks():
        class embed():
            your_ranking = """
            **🧡__{}__**
            **Your Ranked: ``{}#``**
            """

        footer = "Yes, we now got leaderboards. 😄"

    class balance():
        class embed():
            your_ranking = """
            **💛__{}__**
            **🌍 Your Ranked ``{}#`` Worldwide**
            """

        footer = "Become the elon musk of the 💛goldy underworld. "

class rgb():
    toggle_on = "**💚🏮 {}, RGB MODE turned on.**"
    toggle_off = "**❤️🏮 {}, RGB MODE turned off.**"

    rgb_mode_is_off = "**🧡🏮 {}, RGB MODE is currently off. To toggle on, do ``!rgb on``.**"
    rgb_mode_is_on = "**💚🏮 {}, RGB MODE is currently on. To toggle off, do ``!rgb off``.**"