# Goldy Bot V4 *(Modern Rewrite)*

[![Powered by Nextcord](https://custom-icon-badges.herokuapp.com/badge/-Powered%20by%20Nextcord-0d1620?logo=nextcord)](https://github.com/nextcord/nextcord "Powered by Nextcord Python API Wrapper")
[![Pypi Badge](https://img.shields.io/pypi/v/GoldyBot?style=flat)](https://pypi.org/project/GoldyBot/ "Powered by Nextcord Python API Wrapper")

<p align="center">
 <img src="./assets/banner_1.png" width="960" />
</p>

## Goldy Bot V4 - BIG and Modern rewrite of Goldy Bot V3
### ⚠️Warning: Goldy Bot module is only intended for development, therefore you may find difficulty using it for other uses.
### ☢️NOTICE: Goldy Bot is still currently in DEEP development, so expect unfinished code and much bugs.

<p align="right">
 <img align="left" src="./assets/pfp_1.png" width="200" />
 
 # *WTF is this!*
 Goldy Bot V4 is yet *another* rewrite of Goldy Bot, a discord bot that I develop for FUN. This is the third rewrite but the first rewrite to become open source, I've done this to allow developers across the world to create add-ons/extenstions for my bot that I can then add to the official production bot. 
 
 Feel free to use this module to develop your extenstions.
</p> 

#### [⭐The Future of this Project.](https://gist.github.com/THEGOLDENPRO/6d9e0ee2376ac9b7743a0709eab06ca6)

## *Install/Set Up*
1. **Install package from pip.**
```sh
#Windows/Linux

pip install GoldyBot
```

2. **Download MongoDB Community. (You'll need this!) >>> https://www.mongodb.com/try/download/community**

After finishing the install progress the MongoDB compass should open, copy the local host url and click connect. You'll need the url later!

<p align="center">
 <img src="https://user-images.githubusercontent.com/66202304/165760334-96614bf7-ccfc-46a0-a625-7433b1f4bb9b.png" width="530" />
</p>

3. **Now create a run.py file, type this and run it.** 
```python
import GoldyBot

goldy = GoldyBot.Goldy()

goldy.start()
```
Goldy Bot should shut itself down and create a config folder containing a 'bot token' text file.

4. **Enter your discord bot token in the ``bot_token.txt`` file.**
```txt
{ENTER BOT TOKEN HERE}
```
Save that! Make sure you pasted it WITHOUT the curly brackets ({}).

5. **Then in ``goldy.json`` edit the following for Goldy Bot to start functioning.**
```json
"database_name" : "",

"allowed_guilds" : {
}
```
Give the database a name and add your bot testing guild id to "allowed_guilds" or else Goldy Bot will refuse to work.

So like this! (This is just an example!)
```json
"database_name" : "members_data",

"allowed_guilds" : {
    "863416692083916820" : "bot_test_server"
}
```

6. **Now run Goldy Bot.**
It will create another txt file and stop running. This is your database url, remember the url I told you to copy, paste that in this text file WITHOUT the curly brackets ({}).

7. **Then run Goldy Bot once again.**
```
python run.py
```
Now you should see a folder being created for your guild and also a database folder in your MongoDB database.

<p align="center">
 <img src="https://user-images.githubusercontent.com/66202304/165758807-ed28eab3-393a-496f-b76a-7bcf67479c75.png" width="930" />
</p>

8. **Now your all set for development!**

Documentation presenting how to create your very first extension is coming soon...

<br>

**© Copyright (C) 2022 Dev Goldy (Under the [GPL-3.0 License](LICENSE.md))**
