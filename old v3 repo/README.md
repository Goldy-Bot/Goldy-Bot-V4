# Goldy Bot V3 *(Cog Development Kit)*
<p align="center">
 <img src="https://user-images.githubusercontent.com/66202304/126993627-b1009d1d-b46d-4d16-a288-1800eb1f3c21.png" width="960" />
</p>

## Goldy Bot V3 - The rewriten Goldy Bot that is better than ever!

#### [⭐The Future of this Project.](https://gist.github.com/THEGOLDENPRO/6d9e0ee2376ac9b7743a0709eab06ca6)

#### WARNING: This should only be used if you are developing a custom cog for goldy bot as this a CDK (Cog Development Kit). This wasn't built just for the sake of running it on your server, althought you can but please don't open issues if you are not using it to develop a goldy bot cog/extenstion.

<p align="right">
 <img align="left" src="https://avatars.githubusercontent.com/u/87548952" width="180" />
 
 # *WTF is this!*
 Goldy Bot V3 is a privatly used discord bot I've developed for FUN! This version is the strong successor of the previous V2 that only operated in the [Aki Community](https://discord.gg/ZpYtBTcefC) Discord Server. What you are seeing here is the Cog Development Kit (CDK), I've open sourced Goldy Bot for the purpose of allowing members to       develop extenstions for the Official Bot and *also to show off my amazing code.*
</p> 

# ~~*Set Up*~~ *(outdated sorry)*
1. Download the [Latest CDK Release](https://github.com/TGP-Projects/Goldy-Bot-V3/releases) and extract the zip.
2. If your using VSCode open the workspace "goldy_bot_v3.code-workspace" from the folder. If your not using VScode you can just open the whole folder in your code editor.
3. Pip Install all modules:

```
python -m pip install -r requirements.txt
```
4. Now run "goldy.py" and you should get something simuler to this below. **Don't worry** if this isn't the case or you see something else.

<p align="center">
 <img src="https://user-images.githubusercontent.com/66202304/127023876-604c3a71-e05d-4d86-9020-98aa164d18f4.png" width="879" height="103" />
</p>

5. You should now see two new files in the config folder, "token.txt" and "database_url.txt". In "token.txt" enter you discord bot token (asumming that you already have a discord bot application set up in your [discord development portal](https://discord.com/developers/applications)) and you most likely won't be using a mongodb database for development so in "database_url.txt" enter "None" instead.

```python
None
```

6. Now run "goldy.py" again and you shouldn't get any errors. If you experience an error, [create an issue](https://github.com/TGP-Projects/Goldy-Bot-V3/issues/new).

7. Create your Cog. (Goldy Bot has a command line argument for creating a cog template.)

```
python goldy.py create cog
```

You should now see a new cog in the cogs folder named 'your_cog.py'.

8. Rename 'your_cog.py' to whatever you desire.

9. 😎👍 Now your fully setup and ready to start developing your cogs. 

**(Remember to keep them open sourced on GitHub and share them with us. Would love to see your creations for Goldy Bot.😍)**

*More INFO coming soon...*

**© Copyright (C) 2021 TGP Projects (Under the [GPL-3.0 License](LICENSE.md))**
