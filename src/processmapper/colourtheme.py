# MIT License

# Copyright (c) 2022 CS Goh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from dataclasses import dataclass, field

### Font :
# "Microsoft YaHei UI"
# "DengXian"
# "Segoe UI"
# "Tahoma"
# "Microsoft Jhenghei"
# simhei.ttf
# "ARIALUNI.TTF"
# "arial.ttf"

DEFAULT_FONT = "arial.ttf"
DEFAULT_TITLE_FONT_SIZE = 26
DEFAULT_SUBTITLE_FONT_SIZE = 18
DEFAULT_SWIMLANE_FONT_SIZE = 12
DEFAULT_LANE_FONT_SIZE = 12
DEFAULT_ELEMENT_FONT_SIZE = 12
DEFAULT_CONNECTOR_FONT_SIZE = 12
DEFAULT_FOOTER_FONT_SIZE = 12


default_colour_settings = {
    "theme": "DEFAULT",
    "settings": {
        "background": {
            "background_fill_colour": "#FFFFFF",
        },
        "title": {
            "title_font": DEFAULT_FONT,
            "title_font_size": DEFAULT_TITLE_FONT_SIZE,
            "title_font_colour": "#000000",
            "subtitle_font": DEFAULT_FONT,
            "subtitle_font_size": DEFAULT_SUBTITLE_FONT_SIZE,
            "subtitle_font_colour": "#000000",
        },
        "swimlane": {
            "swimlane_font": DEFAULT_FONT,
            "swimlane_font_size": DEFAULT_SWIMLANE_FONT_SIZE,
            "swimlane_font_colour": "#000000",
            "swimlane_fill_colour": "#D9D9D9",
        },
        "lane": {
            "lane_font": DEFAULT_FONT,
            "lane_font_size": DEFAULT_LANE_FONT_SIZE,
            "lane_font_colour": "#000000",
            "lane_fill_colour": "#D9D9D9",
        },
        "element": {
            "element_font": DEFAULT_FONT,
            "element_font_size": DEFAULT_ELEMENT_FONT_SIZE,
            "element_font_colour": "#000000",
            "element_fill_colour": "#D9D9D9",
        },
        "connector": {
            "connector_font": DEFAULT_FONT,
            "connector_font_size": DEFAULT_CONNECTOR_FONT_SIZE,
            "connector_font_colour": "#000000",
            "connector_line_width": 1,
            "connector_line_colour": "#000000",
            "connector_arrow_colour": "#000000",
            "connector_arrow_size": 10,
        },
        "footer": {
            "footer_font": DEFAULT_FONT,
            "footer_font_size": DEFAULT_FOOTER_FONT_SIZE,
            "footer_font_colour": "#000000",
        },
    },
}

# greywoof_colour_settings = {}

# bluemountain_colour_settings = {}

# orangepeel_colour_settings = {}

# greenturtle_colour_settings = {}

ColourThemesSettings = [
    default_colour_settings,
    # greywoof_colour_settings,
    # bluemountain_colour_settings,
    # orangepeel_colour_settings,
    # greenturtle_colour_settings,
    ### Add more themes here
]


@dataclass
class ColourTheme:
    """Colour theme for the Roadmapper."""

    def __init__(self, colour_theme_name: str) -> None:
        """Initialise the colour theme."""

        found = False
        for theme in ColourThemesSettings:
            if theme["theme"] == colour_theme_name:
                found = True

        if found == False:
            raise ValueError(f"Colour theme {colour_theme_name} not recognised.")

        self._colour_theme_name = colour_theme_name

    def get_colour_theme_settings(self, processmap_component: str) -> tuple:
        """Get the colour theme settings for the specified roadmap component.

        Args:
            roadmap_component (str): Roadmap component to get the colour theme settings for.
                                        Components are: "background", "title", "timeline", "marker", "group", "task", "milestone", "footer"

        Returns:
            background_colour (str): If roadmap_component is "background"

            title_font (str): If roadmap_component is "title"
            title_font_size (int): If roadmap_component is "title"
            title_font_colour (str): If roadmap_component is "title"
            subtitle_font (str): If roadmap_component is "title"
            subtitle_font_size (int): If roadmap_component is "title"
            subtitle_font_colour (str): If roadmap_component is "title"



            footer_font_colour (str): If roadmap_component is "footer"
        """

        colour_settings = None

        for _, value in enumerate(ColourThemesSettings):
            if value["theme"] == self._colour_theme_name:
                colour_settings = value["settings"]
                break

        ### get the colour scheme for the specified roadmap component
        ### values() returns a list of dictionaries, convert it to tuple. e.g. {1, 2} -> (1, 2)
        return tuple(colour_settings[processmap_component].values())
