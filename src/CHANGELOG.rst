Change Log
==========

v4.0dev25 = New Dev Release (23/02/2023)
---------------------------
- Fixed /cache command.
- Added mention method to command object.
- Added 'is_child' and 'parent_cmd' property to command object.
- Added dropdown view function in goldy bot utils.
- Added form view function in goldy bot utils.
- Improved GoldyBot dropdown view.
- Added LIME_GREEN.
- Added GoldyBot "send_modal()" method in commands utils.
- Added "Context" to main GoldyBot module.
- Fixed bug with nested sub commands.
- Added default timezone setting in Timestamps.
- Added button in /timestamp to allow for copying the timestamp on Desktop.

v4.0dev24 = New Dev Release (01/10/2022)
---------------------------
- Better typing added for "slash_options".
- give_money() and take_money() now returns boolean.
- Errors are now accessible right from GoldyBot's main module.
- Improved error handler in /timestamp command.
- Better typing in goldy bot utility module.
- Added Goldy Bot hearts class.
- Removed dev command /stop, you can now only stop the bot from the console.
- Improved Goldy Bot stop method. (it functions much better now)
- Removed all lower case 'Colours' variable in main GoldyBot module. ('colours' is now typed as 'Colours') (Backwards compatibility was added so this isn't a breaking change for extensions.)
- Added most common colour in image picker method in the GoldyBot.Colours class.
- Added the WebFile() object.
- Improved GoldyBot.Member() at grabbing member mention from command parameters.
- Added "convert_to_int" & "convert_to_string" arguments to 'Config().read()' method.
- Hidden commands now officially work with slash commands. A hidden slash command will only be visible to discord server administrators. To make a command hidden, set the hidden attribute to True.
- Added "file_name" property to WebFile object.
- Added "extensions" console command to return a list of all extensions currently running on GoldyBot.
- Added "remove()" method in File object.
- Added "downloaded_to_disk" parameter in WebFile object to allow for web files to be temporary downloaded to disk then deleted 5 seconds later.
- Fixed issue where interactions were failing because the command took too long to respond. (Added think() function in command utils.)

v4.0dev23 = BREAKING CHANGE! (16/09/2022)
---------------------------
- Optimizations/speed ups.
- Role object parameters have been changed, so make sure you update it in your code. A complete new redesign has been done to it. (BREAKING CHANGE!)
- Added python version to /goldy command.
- Much more accurate cpu usage percentage.
- Added rate limit warning. A warning will print in console if Goldy Bot is rate limited by Discord.
- Fixed some error handling stuff.
- Added custom_colour() method in ``GoldyBot.Colours``.
- Fixed Role() object. (It was having issues initializing.)
- Added incorrect config exception.
- Updated Nextcord to V2.2.0.

v4.0dev10 = New Release (25/06/2022)
---------------------------
- Backend changes and improvements.

v4.0dev9 - BREAKING CHANGE! (26/04/2022)
---------------------------
- 'toggle_slash_cmd' and 'toggle_normal_cmd' have been changed to 'slash_cmd_only' and 'normal_cmd_only'. I believe this is much easier to understand.

v4.0dev1 - First Dev Release (15/04/2022)
---------------------------
- Hi, this is the first dev release of Goldy Bot V4.