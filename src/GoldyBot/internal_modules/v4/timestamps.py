import GoldyBot
from GoldyBot.utility.commands import *
import pytz

AUTHOR = 'Dev Goldy'
AUTHOR_GITHUB = 'https://github.com/THEGOLDENPRO'
OPEN_SOURCE_LINK = ''

class Timestamps(GoldyBot.Extension):
    """Timestamps extension."""
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

    def loader(self):

        @GoldyBot.command(help_des="Sends a discord timestamp of that time and date.",slash_cmd_only=True, slash_options={
            "date" : GoldyBot.nextcord.SlashOption(description="The date goes here like example, 13.08.2022 or even 2022/08/22.", required=True),
            "time" : GoldyBot.nextcord.SlashOption(description="The time goes here like example, 15:00.", required=True),
            "flag" : GoldyBot.nextcord.SlashOption(description="Choose a flag.", required=True, choices={
                "08/13/2022": "d",
                "August 13, 2022": "D",
                "6:00 PM": "t",
                "6:00:00 PM": "T",
                "August 13, 2022 6:00 PM" : "f",
                "Saturday, August 13, 2022 6:00 PM" : "F",
                "in 3 hours": "R"
            }),
            "timezone" : GoldyBot.nextcord.SlashOption(description="The timezone to convert to; Goldy Bot defaults to Europe/London timezone.", default="Europe/London")
        })
        async def timestamp(self:Timestamps, ctx, date, time, flag, timezone):
            datetime = GoldyBot.utility.datetime.user_input.get_time_and_date(f"{date} {time}")

            if not datetime == None:
                try:
                    # Convert to chosen timezone.
                    chosen_timezone = pytz.timezone(timezone)
                    datetime = chosen_timezone.normalize(chosen_timezone.localize(datetime, is_dst=True)) 

                    await send(ctx, f"<t:{int(datetime.timestamp())}:{flag}>")

                    return True

                except Exception as e:
                    GoldyBot.log("error", e)
                    pass

            message = await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                title="❓ Did you enter it correctly?",
                description="I couldn't read either your time or date properly, please could you try again. Perhaps you mistyped something.",
                colour=GoldyBot.utility.goldy.colours.RED
            ))

            await message.delete(delay=8)


def load():
    # This function get's executed when the module is loaded so run your extension classes in here.
    # Example: YourExtension(package_module_name=__name__)

    Timestamps(__name__)