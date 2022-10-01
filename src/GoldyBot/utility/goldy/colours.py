from __future__ import annotations
from typing import Literal
import nextcord
import GoldyBot
from colorthief import ColorThief

class Colours:
    """Hardcoded GoldyBot colour codes. These can be used in Embeds and stuff."""
    AKI_PINK = 0xFF1493
    AKI_ORANGE = 0xF4900C
    AKI_RED = 0xff0051
    AKI_BLUE = 0X75E6DA
    BLUE = 0x3061f2
    GREEN = 0x00FF00
    YELLOW = 0xffff4d
    PURPLE = 0xFF00FF
    RED = 0xFF0000
    GREY = 0x3B3B3B
    WHITE = 0xFFFFFF
    
    def custom_colour(self, rgb:tuple=None, hex:int|str=None) -> Literal|int:
        """
        Method to create custom colour with rgb or hex values.
        (WARNING: Hex is currently not supported, if hex is entered value of ``WHITE`` will be returned.)
        """
        if not rgb == None:
            if isinstance(rgb, tuple):
                return nextcord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]).value

        return self.WHITE
    
    def get_colour_from_image(self, image_file:GoldyBot.files.File, quality:int=5) -> Literal|int:
        """Returns most common colour from any image."""

        if isinstance(image_file, GoldyBot.WebFile): # It's a web file.
            image_file:GoldyBot.WebFile
            return self.custom_colour(
                rgb=ColorThief(image_file.get_file()).get_color(quality)
            )

        else: # It's a normal file.
            return self.custom_colour(
                rgb=ColorThief(image_file.file_path).get_color(quality)
            )

class Colors(Colours):
    pass



# This section below is all Deprecated, use Colours enum class instead.
AKI_PINK = Colours.AKI_PINK
"""This is Deprecated, use ``Colours.AKI_PINK`` instead!"""
AKI_ORANGE = Colours.AKI_ORANGE
"""This is Deprecated, use ``Colours.AKI_ORANGE`` instead!"""
AKI_RED = Colours.AKI_RED
"""This is Deprecated, use ``Colours.AKI_RED`` instead!"""
AKI_BLUE = Colours.AKI_BLUE
"""This is Deprecated, use ``Colours.AKI_BLUE`` instead!"""
BLUE = Colours.BLUE
"""This is Deprecated, use ``Colours.BLUE`` instead!"""
GREEN = Colours.GREEN
"""This is Deprecated, use ``Colours.GREEN`` instead!"""
YELLOW = Colours.YELLOW
"""This is Deprecated, use ``Colours.YELLOW`` instead!"""
PURPLE = Colours.PURPLE
"""This is Deprecated, use ``Colours.PURPLE`` instead!"""
RED = Colours.RED
"""This is Deprecated, use ``Colours.RED`` instead!"""
GREY = Colours.GREY
"""This is Deprecated, use ``Colours.GREY`` instead!"""
WHITE = Colours.WHITE
"""This is Deprecated, use ``Colours.WHITE`` instead!"""