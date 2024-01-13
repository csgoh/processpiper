# Painter class - Wrapper for Pillow library
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
import math
import os
import sys
from .colourtheme import ColourTheme
from PIL import Image, ImageDraw, ImageFont, ImageColor
import drawsvg as dw
import textwrap
from .helper import Helper


class UnsupportedOSException(Exception):
    pass


class Painter:
    width: int
    height: int
    output_type: str

    # --Colour scheme attributes - Start
    background_fill_colour: str
    title_font: str
    title_font_size: int
    title_font_colour: str

    pool_font: str
    pool_font_size: int
    pool_font_colour: str
    pool_fill_colour: str
    pool_text_alignment: str

    lane_font: str
    lane_font_size: int
    lane_font_colour: str
    lane_fill_colour: str
    lane_text_alignment: str
    lane_background_fill_colour: str

    element_font: str
    element_font_size: int
    element_font_colour: str
    element_fill_colour: str
    element_outline_colour: str
    element_outline_width: int
    element_text_alignment: str

    connector_font: str
    connector_font_size: int
    connector_font_colour: str
    connector_line_width: int
    connector_line_colour: str
    connector_arrow_colour: str
    connector_arrow_size: int

    footer_font: str
    footer_font_size: int
    footer_font_colour: str
    # --Colour scheme attributes - End

    def __init__(self, width: int = 500, height: int = 500) -> None:
        """Initialise the painter"""
        self.width = width
        self.height = height

    def set_colour_theme(self, colour_theme: str) -> None:
        """Set colour palette

        Args:
            colour_palette (str): Name of the colour palette. Eg. OrangePeel
        """
        self.colour_theme = ColourTheme(colour_theme)
        (self.background_fill_colour,) = self.colour_theme.get_colour_theme_settings(
            "background"
        )
        (
            self.title_font,
            self.title_font_size,
            self.title_font_colour,
        ) = self.colour_theme.get_colour_theme_settings("title")
        (
            self.pool_font,
            self.pool_font_size,
            self.pool_font_colour,
            self.pool_fill_colour,
            self.pool_text_alignment,
        ) = self.colour_theme.get_colour_theme_settings("pool")
        (
            self.lane_font,
            self.lane_font_size,
            self.lane_font_colour,
            self.lane_fill_colour,
            self.lane_text_alignment,
            self.lane_background_fill_colour,
        ) = self.colour_theme.get_colour_theme_settings("lane")
        (
            self.element_font,
            self.element_font_size,
            self.element_font_colour,
            self.element_fill_colour,
            self.element_outline_colour,
            self.element_outline_width,
            self.element_text_alignment,
        ) = self.colour_theme.get_colour_theme_settings("element")
        (
            self.connector_font,
            self.connector_font_size,
            self.connector_font_colour,
            self.connector_line_width,
            self.connector_line_colour,
            self.connector_arrow_colour,
            self.connector_arrow_size,
        ) = self.colour_theme.get_colour_theme_settings("connector")
        (
            self.footer_font,
            self.footer_font_size,
            self.footer_font_colour,
        ) = self.colour_theme.get_colour_theme_settings("footer")

    def set_element_font_size(self, font_size: int) -> None:
        """Set the font size for all element type"""

        if not isinstance(font_size, int):
            raise TypeError("font_size must be an integer")

        self.element_font_size = font_size

    def set_title_font_size(self, font_size: int) -> None:
        """Set the font size for the title"""

        if not isinstance(font_size, int):
            raise TypeError("font_size must be an integer")

        self.title_font_size = font_size

    def get_font_path(self, font_name: str) -> str:
        """Get the path to the font file"""
        if sys.platform.startswith("win"):  # Windows
            return os.path.join("C:\\", "Windows", "Fonts", f"{font_name}.ttf")
        elif sys.platform.startswith("darwin"):  # macOS
            return os.path.join(
                "/", "System", "Library", "Fonts", "Supplemental", f"{font_name}.ttf"
            )
        elif sys.platform.startswith("linux"):  # Linux
            font_dir = "/usr/share/fonts/truetype/msttcorefonts"

            if os.path.exists(os.path.join(font_dir, f"{font_name}.ttf")):
                return os.path.join(font_dir, f"{font_name}.ttf")
            # This is cater for cases where msttcorefonts is not installed
            linux_font_name = "DejaVuSans"  # Default font for Linux
            return os.path.join(
                "/",
                "usr",
                "share",
                "fonts",
                "truetype",
                "dejavu",  # Use the DejaVu font directory instead of msttcorefonts
                f"{linux_font_name}.ttf",
            )
        else:
            raise UnsupportedOSException("Unsupported operating system")

    def draw_grid(self):
        """Draw a grid of dots to help with alignment"""
        #  Set the dot size and spacing
        spacing = 10

        # Draw the grid of dots
        for x in range(0, self.width, spacing):
            for y in range(0, self.height, spacing):
                if x > 0 and y > 0:
                    self.draw_dot(x, y, "grey")
                    if x % 50 == 0 or y % 50 == 0:
                        self.draw_dot(x, y, "blue")
                    if x % 100 == 0 or y % 100 == 0:
                        self.draw_dot(x, y, "red")

    def set_background_colour(self) -> None:
        """Set surface background colour"""
        if self.background_fill_colour == "transparent":
            # Set transparent background
            self.draw_box(0, 0, self.width, self.height, (0, 0, 0, 0))
        else:
            self.draw_box(0, 0, self.width, self.height, self.background_fill_colour)

    def draw_box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_fill_colour: str = "",
        box_outline_colour: str = "",
        box_outline_width=0,
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        return [(x, y), (x + width, y + height)]

    def draw_box_with_outline(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_outline_colour: str = "",
        box_outline_transparency: int = 1,
        box_outline_width: int = 1,
        box_fill_colour: str = "",
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """

        self.draw_box(
            x, y, width, height, box_fill_colour, box_outline_colour, box_outline_width
        )

    def draw_rounded_box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_fill_colour: str = "",
        box_outline_colour: str = "",
        box_outline_width: int = 0,
    ) -> None:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        return 20, [(x, y), (x + width, y + height)]

    def draw_box_with_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: int,
        box_outline_colour: str,
        box_outline_width: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> list:
        box_x1, box_y1, box_x2, box_y2 = (
            box_x,
            box_y,
            box_x + box_width,
            box_y + box_height,
        )
        match style:
            case "rectangle":
                self.draw_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour,
                    box_outline_colour,
                    box_outline_width,
                )
            case "rounded":
                self.draw_rounded_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour,
                    box_outline_colour,
                    box_outline_width,
                )
            case "arrowhead":
                self.draw_arrowhead_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour,
                    box_outline_colour,
                    box_outline_width,
                )
            case _:
                raise ValueError("Invalid style")

        multi_lines = []
        wrap_lines = []

        # Make '\n' work
        multi_lines = text.splitlines()

        font, single_char_width, _, _ = self.get_char_width(
            "a", text_font, text_font_size
        )

        # wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, int(box_width / single_char_width)))

        pad = 4
        line_count = len(wrap_lines)

        display_lines = []
        for i, line in enumerate(wrap_lines):
            font_width, font_height = self.get_text_dimension(
                line, text_font, text_font_size
            )

            match text_alignment:
                case "centre":
                    x = box_x1 + (box_width - font_width) / 2
                case "left":
                    x = box_x1 + 15
                case "right":
                    x = box_x2 - font_width - 15
                case _:
                    x = box_x1 + (box_width - font_width) / 2

            total_line_height = (font_height * line_count) + (pad * (line_count - 1))

            single_line_height = font_height

            y = (
                box_y1
                + ((box_height - total_line_height) / 2)
                + ((single_line_height * i) + (pad * i))
            )

            display_lines.append((x, y, line))

        return display_lines

    def get_char_width(self, chars, text_font, text_font_size):
        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)
        left, _, right, bottom = font.getbbox(chars)
        char_width = right - left
        font_width = right
        font_height = bottom
        return font, char_width, font_width, font_height

    def draw_box_with_vertical_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: str,
        box_outline_colour: str,
        box_outline_width: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> list:
        """Draw a box with vertical text"""

        multi_lines = []
        wrap_lines = []

        # Make '\n' work
        multi_lines = text.splitlines()

        font, single_char_width, _, _ = self.get_char_width(
            "a", text_font, text_font_size
        )

        # wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, int(box_height / single_char_width)))

        box_x1, box_y1, box_x2, box_y2 = (
            box_x,
            box_y,
            box_x + box_width,
            box_y + box_height,
        )
        match style:
            case "rectangle":
                self.draw_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour=box_fill_colour,
                    box_outline_colour=box_outline_colour,
                    box_outline_width=box_outline_width,
                )
            case "rounded":
                self.draw_rounded_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour,
                    box_outline_colour,
                    box_outline_width,
                )
            case "arrowhead":
                self.draw_arrowhead_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour,
                    box_outline_colour,
                    box_outline_width,
                )
            case _:
                raise ValueError("Invalid style")

        pad = 5
        line_count = len(wrap_lines)

        display_lines = []
        for i, line in enumerate(wrap_lines):
            font_width, font_height = self.get_text_dimension(
                line, text_font, text_font_size
            )

            total_line_height = (font_height * line_count) + (pad * (line_count - 1))
            match text_alignment:
                case "centre":
                    x = (
                        box_x1
                        + ((box_width - total_line_height) / 2)
                        + ((font_height * i) + (pad * i))
                    )
                case "left":
                    x = box_x1 + 15
                case "right":
                    x = box_x2 - font_width - 15
                case _:
                    x = box_x1 + (box_width - font_width) / 2

            y = box_y1 + ((box_height - font_width) / 2)

            display_lines.append((x, y, font_width, font_height, line))

        return display_lines

    def draw_polygon(
        self,
        points: list,
        outline_colour: str = "",
        outline_width: int = 1,
        fill_colour: str = "",
    ):
        raise NotImplementedError

    def draw_diamond(
        self, x: int, y: int, width: int, height: int, fill_colour: str
    ) -> None:
        """Draw a diamond

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Diamond width
            height (int): Diamond height
            fill_colour (str): Diamond fill colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """

        # Calculate the coordinates of the four points of the diamond.
        # points = super().draw_diamond(x, y, width, height, fill_colour)
        points = [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2),
        ]

        # Use Pillow's ImageDraw module to draw a polygon with the given points and fill color.
        # self.__cr.polygon(points, fill=fill_colour)
        self.draw_polygon(points, fill_colour=fill_colour)

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: float,
        outline_colour: str,
        outline_width: int = 1,
        fill_colour: str = "",
    ) -> None:
        raise NotImplementedError
        # return (x - radius, y - radius, x + radius, y + radius)
        # return (x, y, radius)

    def draw_dot(self, x: int, y: int, colour: str) -> None:
        raise NotImplementedError

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        line_colour: str,
        line_transparency: int,
        line_width: int,
        line_style: str = "solid",
    ) -> list:
        """Draw a line

        Args:
            x1 (int): Line begin X coordinate
            y1 (int): Line begin Y coordinate
            x2 (int): Line end X coordinate
            y2 (int): Line end Y coordinate
            line_colour (str): Line colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            line_transparency (int): Line transparency. 0 is opaque and 255 is transparent
            line_width (int): Line width
            line_style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """

        def linspace(start, stop, n):
            if n == 1:
                yield stop
                return
            h = (stop - start) / (n - 1)
            for i in range(n):
                yield start + h * i

        lines = []
        if line_style == "solid":
            lines.append(((x1, y1), (x2, y2)))
        elif line_style == "dashed":
            # given a line between x1, y1 and x2, y2, divide it into multiple shorter lines
            # and draw them with a gap in between.

            # Calculate the number of dashes
            gap_counts = int((y2 - y1) / 7)

            for i, (x, y) in enumerate(
                zip(
                    linspace(x1, x2, gap_counts),
                    linspace(y1, y2, gap_counts),
                )
            ):
                if i % 2 == 0:
                    # self.__cr.line(
                    #     (x, y, x, y + 10),
                    #     width=line_width,
                    #     fill=(r, g, b, int(255 * line_transparency)),
                    # )
                    lines.append((x, y, x, y + 10))

        return lines

    def draw_vertical_dashed_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        connector_line_width,
        connector_line_colour,
    ):  # sourcery skip: remove-unnecessary-cast
        """Draw a vertical dashed line"""
        gap_size = 10
        y1 = int(y1)
        y2 = int(y2)
        if y1 > y2:
            for i in range(y2, y1, gap_size):
                new_y = max(i - 5, y2)
                self.draw_line(
                    x1, i, x2, new_y, connector_line_colour, 1, connector_line_width
                )
        else:
            for i in range(y1, y2, gap_size):
                new_y = min(i + 5, y2)
                self.draw_line(
                    x1, i, x2, new_y, connector_line_colour, 1, connector_line_width
                )

    def draw_horizontal_dashed_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        connector_line_width,
        connector_line_colour,
    ):
        """Draw a horizontal dashed line"""
        gap_size = 10
        x1 = int(x1)
        x2 = int(x2)

        if x1 > x2:
            x1 += 10
            for i in range(x2, x1, gap_size):
                new_x = max(i - 5, x2)
                self.draw_line(i, y1, new_x, y2, connector_line_colour, 1, 1)
        else:
            for i in range(x1, x2, gap_size):
                new_x = min(i + 5, x2)
                self.draw_line(i, y1, new_x, y2, connector_line_colour, 1, 1)

    def draw_right_angle_dot_line(self, x1: int, y1: int, x2: int, y2: int):
        if x1 < x2 and y1 < y2 or x1 >= x2 and y1 >= y2:
            right_angle_point = (x2, y1)
        else:
            right_angle_point = (x1, y2)
        self.draw_horizontal_dashed_line(
            x1, y1, right_angle_point[0], right_angle_point[1]
        )
        self.draw_vertical_dashed_line(
            right_angle_point[0], right_angle_point[1], x2, y2
        )

    def draw_dashed_line(
        self,
        points: tuple,
        connector_line_width: int = 0,
        connector_line_colour: str = "",
    ):
        """Draw a dashed line between two points"""
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 == x2:
                self.draw_vertical_dashed_line(
                    x1, y1, x2, y2, connector_line_width, connector_line_colour
                )
            elif y1 == y2:
                self.draw_horizontal_dashed_line(
                    x1, y1, x2, y2, connector_line_width, connector_line_colour
                )

    def get_points(
        self,
        nearest_points,
    ):
        """Get the points to draw a line between two elements"""
        x1, y1 = nearest_points["source_points"]
        x2, y2 = nearest_points["target_points"]
        face_source = nearest_points["source_name"]
        face_target = nearest_points["target_name"]

        # Helper.printc(
        #     f"      GET_POINTS(): {x1=}, {y1=}, {face_source=}, {x2=}, {y2=}, {face_target=}",
        #     show_level="draw_connection",
        # )
        points, _ = self.get_connection_points(x1, y1, face_source, x2, y2, face_target)

        return points

    def draw_right_angle_line(
        self,
        x1: int,
        y1: int,
        face_source: str,
        x2: int,
        y2: int,
        face_target: str,
        connection_style: str,
        connector_line_width: int = 0,
        connector_line_colour: str = "",
    ):
        """Draw a right angle line between two points"""
        points, right_angle_points = self.get_connection_points(
            x1, y1, face_source, x2, y2, face_target
        )
        Helper.printc(
            "\t" * 2
            + f"DRAW_RIGHT_ANGLE_LINE() {x1=}, {y1=}, {face_source=}, {x2=}, {y2=}, {face_target=}",
            show_level="draw_connection",
        )

        if connection_style == "dashed":
            self.draw_dashed_line(points, connector_line_width, connector_line_colour)
        else:
            # self.__cr.line(
            #     points, fill=(connector_line_colour), width=connector_line_width
            # )
            for idx, point in enumerate(points):
                if idx < len(points) - 1:
                    self.draw_line(
                        point[0],
                        point[1],
                        points[idx + 1][0],
                        points[idx + 1][1],
                        connector_line_colour,
                        1,
                        connector_line_width,
                        "solid",
                    )

        return right_angle_points

    def get_connection_points(self, x1, y1, face_source, x2, y2, face_target):
        """Get the points to draw a line between two elements"""
        tab_count = 3
        if x1 == x2 and y1 == y2:
            # Shapes are on top of each other / overlapping. NOTE: This should never happen
            Helper.printc(
                "\t" * tab_count + "Shapes are on top of each other / overlapping",
                show_level="draw_connection",
            )
            Helper.printc(
                "\t" * tab_count
                + "A: right_angle_line: x1 == x2 and y1 == y2: {x1}, {y1}, {x2}, {y2}",
                show_level="draw_connection",
            )
            points = [(x1, y1)]
            right_angle_point = points

        if x1 != x2 and y1 == y2:
            # Shapes are on the same horizontal line
            Helper.printc(
                "\t" * tab_count + "Shapes are on the same horizontal line",
                show_level="draw_connection",
            )
            Helper.printc(
                "\t" * tab_count
                + "B: right_angle_line: x1 != x2 and y1 == y2: {x1}, {y1}, {x2}, {y2}",
                show_level="draw_connection",
            )
            elbow_height = 40
            if face_source.find("top") != -1:
                points = [
                    (x1, y1),
                    (x1, y1 - elbow_height),
                    (x2, y2 - elbow_height),
                    (x2, y2),
                ]
                right_angle_point = [(x1, y1 - elbow_height), (x2, y2 - elbow_height)]
            elif face_source.find("bottom") != -1:
                # points = [(x1, y1), (x1, y1 + elbow_height), (x2, y2 + elbow_height)]
                # right_angle_point = [(x1, y1 + elbow_height)]
                if y2 <= y1:
                    angle_height = 40
                else:
                    angle_height = y2 - y1 + 40

                points = [
                    (x1, y1),
                    (x1, y1 + angle_height),
                    (x2, y1 + angle_height),
                    (x2, y2),
                ]
                right_angle_point = [
                    (x1, y1 + angle_height),
                    (x2, y1 + angle_height),
                ]
            else:
                points = [(x1, y1), (x2, y1)]
                right_angle_point = [(x1, y1)]

        if x1 == x2 and y1 != y2:
            # Shapes are on the same vertical line
            Helper.printc(
                "\t" * tab_count + "Shapes are on the same vertical line",
                show_level="draw_connection",
            )
            Helper.printc(
                "\t" * tab_count
                + "C: right_angle_line: x1 == x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}",
                show_level="draw_connection",
            )
            points = [(x1, y1), (x1, y2)]
            right_angle_point = [(x1, y1)]

        if x1 != x2 and y1 != y2:
            # Shapes are on different horizontal and vertical lines
            # check if face1 string contained the word "right"
            Helper.printc(
                "\t" * tab_count
                + "Shapes are on different horizontal and vertical lines",
                show_level="draw_connection",
            )
            if face_source.find("bottom") != -1:
                if face_target.find("bottom") != -1:
                    Helper.printc(
                        "\t" * tab_count + "D-bottom: both bottom",
                        show_level="draw_connection",
                    )
                    # if so, then the line should be drawn from the bottom side of the box
                    if y2 <= y1:
                        angle_height = 50
                    else:
                        angle_height = y2 - y1 + 50

                    points = [
                        (x1, y1),
                        (x1, y1 + angle_height),
                        (x2, y1 + angle_height),
                        (x2, y2),
                    ]
                    right_angle_point = [
                        (x1, y1 + angle_height),
                        (x2, y1 + angle_height),
                    ]
                elif face_target.find("top") != -1:
                    Helper.printc(
                        "\t" * tab_count + "D-bottom: source bottom, target top",
                        show_level="draw_connection",
                    )
                    elbow_height = 40
                    points = [
                        (x1, y1),
                        (x1, y1 + elbow_height),
                        (x2, y1 + elbow_height),
                        (x2, y2),
                    ]
                    right_angle_point = [
                        (x1, y1 + elbow_height),
                        (x2, y1 + elbow_height),
                    ]
                else:  # target face is
                    Helper.printc(
                        "\t" * tab_count + "D-bottom: source bottom",
                        show_level="draw_connection",
                    )
                    # if so, then the line should be drawn from the bottom side of the box
                    points = [
                        (x1, y1),
                        (x1, y2),
                        (x2, y2),
                    ]
                    right_angle_point = [(x1, y2)]
            elif face_source.find("right") != -1:
                Helper.printc(
                    "\t" * tab_count
                    + "D-right: right_angle_line: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}",
                    show_level="draw_connection",
                )
                if face_target.find("left") != -1:
                    elbow_height = x2 - x1 - 40
                    points = [
                        (x1, y1),
                        (x1 + elbow_height, y1),
                        (x1 + elbow_height, y2),
                        (x2, y2),
                    ]
                    right_angle_point = [
                        (x1 + elbow_height, y1),
                        (x1 + elbow_height, y2),
                    ]
                elif face_target.find("right") != -1:
                    elbow_height = 40
                    # both faces are right
                    Helper.printc(
                        "\t" * tab_count + "D-right-right (x1 < x2)",
                        show_level="draw_connection",
                    )
                    points = [
                        (x1, y1),
                        (x2 + elbow_height, y1),
                        (x2 + elbow_height, y2),
                        (x2, y2),
                    ]
                    right_angle_point = [
                        (x2 + elbow_height, y1),
                        (x2 + elbow_height, y2),
                    ]
                elif face_target.find("top") != -1:
                    if y1 < y2:
                        Helper.printc(
                            "\t" * 2 + "D-right-top (y1 < y2)",
                            show_level="draw_connection",
                        )
                        points = [
                            (x1, y1),
                            (x2, y1),
                            (x2, y2),
                        ]
                        right_angle_point = [
                            (x2, y1),
                        ]
                    else:
                        Helper.printc(
                            "\t" * tab_count + "D-right-top (y1 >= y2)",
                            show_level="draw_connection",
                        )
                        vertical_elbow_height = 40
                        horizontal_elbow_height = 60
                        points = [
                            (x1, y1),
                            (x2 + horizontal_elbow_height, y1),
                            (x2 + horizontal_elbow_height, y2 - vertical_elbow_height),
                            (x2, y2 - vertical_elbow_height),
                            (x2, y2),
                        ]
                        right_angle_point = [
                            (x2 + horizontal_elbow_height, y1),
                            (x2 + horizontal_elbow_height, y2 - vertical_elbow_height),
                            (x2, y2 - vertical_elbow_height),
                        ]
                else:
                    Helper.printc(
                        "\t" * tab_count + "D-right-bottom",
                        show_level="draw_connection",
                    )
                    points = [
                        (x1, y1),
                        (x2, y1),
                        (x2, y2),
                    ]
                    right_angle_point = [
                        (x2, y1),
                    ]
            elif face_source.find("top") != -1 and face_target.find("top") != -1:
                Helper.printc(
                    "\t" * tab_count
                    + "D-top: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}",
                    show_level="draw_connection",
                )
                # draw 1 right angle line
                elbow_height = 40
                points = [
                    (x1, y1),
                    (x1, y1 - elbow_height),
                    (x2, y1 - elbow_height),
                    (x2, y2),
                ]
                # right_angle_point = (x2, y2 - elbow_height)
                right_angle_point = [(x1, y1 - elbow_height), (x2, y1 - elbow_height)]
            elif face_source.find("top") != -1 and face_target.find("bottom") != -1:
                Helper.printc(
                    "\t" * tab_count
                    + "D-top/bottom: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}",
                    show_level="draw_connection",
                )
                # draw 1 right angle line
                elbow_height = 20
                points = [
                    (x1, y1),
                    (x1, y1 - elbow_height),
                    (x2, y1 - elbow_height),
                    (x2, y2),
                ]
                # right_angle_point = (x2, y1 - elbow_height)
                right_angle_point = [(x1, y1 - elbow_height), (x2, y1 - elbow_height)]
            else:
                Helper.printc(
                    "\t" * tab_count
                    + "D-else: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}",
                    show_level="draw_connection",
                )
                # if so, then the line should be drawn from the bottom side of the box
                points = [(x1, y1), (x1, y2), (x2, y2)]
                right_angle_point = [(x1, y2)]
                # for point in points:
                #     self.draw_circle(point[0], point[1], 4, "yellow")

        if x1 > x2:
            if y1 <= y2:
                if abs(y1 - y2) == 10:
                    Helper.printc(
                        "\t" * tab_count
                        + "E: x1 > x2 and y1 <= y2: {x1}, {y1}, {x2}, {y2}",
                        show_level="draw_connection",
                    )
                    elbow_height = 40
                    points = [
                        (x1, y1),
                        (x1, y1 - elbow_height),
                        (x2, y1 - elbow_height),
                        (x2, y2),
                    ]
                    # right_angle_point = (x2, y1 - elbow_height)
                    right_angle_point = [
                        (x1, y1 - elbow_height),
                        (x2, y1 - elbow_height),
                    ]
                if abs(y1 - y2) >= 100:
                    elbow_height = 40
                    if (
                        face_source.find("bottom") == -1
                        or face_target.find("right") == -1
                    ):
                        Helper.printc(
                            "\t" * tab_count
                            + "F2: x1 > x2 and y1 <= y2: {x1}, {y1}, {x2}, {y2}",
                            show_level="draw_connection",
                        )
                        points = [
                            (x1, y1),
                            (x1, y1 + elbow_height),
                            (x2, y1 + elbow_height),
                            (x2, y2),
                        ]
                        # right_angle_point = (x2, y1 - elbow_height)
                        right_angle_point = [
                            (x1, y1 - elbow_height),
                            (x2, y1 - elbow_height),
                        ]
                    else:
                        Helper.printc(
                            "\t" * tab_count
                            + "F1: x1 > x2 and y1 <= y2: {x1}, {y1}, {x2}, {y2}",
                            show_level="draw_connection",
                        )
                        points = [
                            (x1, y1),
                            (x1, y2),
                            (x2, y2),
                        ]
                        right_angle_point = [(x1, y2)]
            elif len(points) == 0:
                Helper.printc(
                    "\t" * tab_count
                    + "G: x1 > x2 and y1 > y2: {x1=}, {y1=}, {x2=}, {y2=}",
                    show_level="draw_connection",
                )
                elbow_height = (y1 - y2) / 2
                points = [
                    (x1, y1),
                    (x1, y1 - elbow_height),
                    (x2, y2 + elbow_height),
                    (x2, y2),
                ]
                # for point in points:
                #     self.draw_circle(point[0], point[1], 2, "green")
                # right_angle_point = (x2, y2 + elbow_height)
                right_angle_point = [
                    (x1, y1 - elbow_height),
                    (x2, y1 - elbow_height),
                ]

        return points, right_angle_point

    def draw_connection(
        self,
        points,
        label: str = "",
        connection_style: str = "solid",
        connector_font: str = "",
        connector_font_size: int = 0,
        connector_font_color: str = "",
        connector_line_width: int = 0,
        connector_line_colour: str = "",
        connector_arrow_colour: str = "",
        connector_arrow_size: int = 0,
    ):
        Helper.printc(f"        >>>> POINTS : {points}", show_level="draw_connection")

        if points is None:
            return

        previous_point = points[0]

        if connection_style == "dashed":
            self.draw_dashed_line(points, connector_line_width, connector_line_colour)
        else:
            for point in points[1:]:
                self.draw_line(
                    previous_point[0],
                    previous_point[1],
                    point[0],
                    point[1],
                    line_colour=connector_line_colour,
                    line_transparency=255,
                    line_width=connector_line_width,
                    line_style=connection_style,
                )
                previous_point = point

        # -- draw the text label at the middle points
        num_points = len(points)
        mid = num_points // 2

        # print(f"       MID={mid}")
        # font = ImageFont.truetype("arial.ttf", size=18)
        # left, _, right, bottom = font.getbbox("#")
        # font_width = right
        # font_height = bottom
        # font_width, font_height = self.get_text_dimension(label, connector_font, connector_font_size)
        font_width, font_height = self.get_multitext_dimension(
            label, connector_font, connector_font_size
        )

        start_x = points[mid - 1][0]
        start_y = points[mid - 1][1]
        end_x = points[mid][0]
        end_y = points[mid][1]

        if start_x == end_x:  # Same X Axis
            # label = f"X:{label}"
            text_width = font_width  # * len(label)
            x_mid = start_x + 5
            if start_y > end_y:
                y_mid = start_y - ((abs(start_y - end_y) / 2) + (font_height / 2))
            else:
                y_mid = start_y + ((abs(start_y - end_y) / 2) - (font_height / 2))
            # Helper.printc(f"        1. @@@ {points=}, {num_points=}, {mid=}, {(start_x, start_y)}, {(end_x, end_y)}, {(x_mid, y_mid)=}", show_level="draw_connection")
        elif start_y == end_y:  # Same Y Axis
            # label = f"Y:{label}"
            text_width = font_width  # * len(label)
            if start_x > end_x:
                x_mid = start_x - ((abs(start_x - end_x) / 2) + (text_width / 2))
            else:
                x_mid = start_x + ((abs(start_x - end_x) / 2) - (text_width / 2))
            y_mid = start_y + 5
            # Helper.printc(f"        2. @@@ {text_width=}, {points=}, {num_points=}, {mid=}, {(start_x, start_y)}, {(end_x, end_y)}, {(x_mid, y_mid)=}", show_level="draw_connection")

        # -- draw text --

        self.draw_text(
            x_mid,
            y_mid,
            label,
            font=connector_font,
            font_size=connector_font_size,
            font_colour=connector_font_color,
        )

        if connection_style == "dashed":
            # --Draw round circle at the beginning of the line
            self.draw_circle(
                points[0][0],
                points[0][1],
                radius=6,
                outline_colour=connector_arrow_colour,
                fill_colour="white",
            )

            self.draw_arrow_head(
                points[-2][0],
                points[-2][1],
                points[-1][0],
                points[-1][1],
                connector_line_colour,
                connector_arrow_size,
                "white",
            )
        else:
            self.draw_arrow_head(
                points[-2][0],
                points[-2][1],
                points[-1][0],
                points[-1][1],
                connector_line_colour,
                connector_arrow_size,
                connector_line_colour,
            )

    def draw_line_and_arrow(
        self,
        x1: int,
        y1: int,
        face1: str,
        x2: int,
        y2: int,
        face2: str,
        label: str = "",
        connection_style: str = "solid",
        connector_font: str = "",
        connector_font_size: int = 0,
        connector_font_color: str = "",
        connector_line_width: int = 0,
        connector_line_colour: str = "",
        connector_arrow_colour: str = "",
        connector_arrow_size: int = 0,
    ):
        """Draw a line and arrow between two boxes"""

        right_angle_points = self.draw_right_angle_line(
            x1,
            y1,
            face1,
            x2,
            y2,
            face2,
            connection_style,
            connector_line_width,
            connector_line_colour,
        )

        label_x_pos, label_y_pos = right_angle_points[-1]
        arrow_angle_points = right_angle_points[-1]

        label_w, label_h = self.get_multitext_dimension(label, connector_font, 12)
        if label_x_pos == x1 and label_y_pos == y1:
            # There is no right angle point
            label_x_pos = max(x1 + 5, x1 + (((x2 - x1) - label_w) / 2))
            if y1 == y2:
                label_y_pos = y1 - label_h - 3
            else:
                label_y_pos = y1 + ((y2 - y1) / 2) - (label_h / 2)

        else:
            label_x_pos += 5
            if y1 == y2 or (abs(y1 - y2) <= 10):
                label_y_pos = label_y_pos + label_h
            else:
                label_y_pos = y1 + ((y2 - y1) / 2) - (label_h / 2)
            # Helper.printc(
            #     f"        @@@ {label=} With right angle point",
            #     35,
            #     show_level="draw_connection",
            # )

        self.draw_text(
            label_x_pos,
            label_y_pos,
            label,
            connector_font,
            connector_font_size,
            connector_font_color,
        )

        if connection_style == "dashed":
            # --Draw round circle at the beginning of the line
            self.draw_circle(
                x1,
                y1,
                radius=6,
                outline_colour=connector_arrow_colour,
                fill_colour="white",
            )

            # --Draw white arrow head at the end of the line

            self.draw_arrow_head(
                arrow_angle_points[0],
                arrow_angle_points[1],
                x2,
                y2,
                connector_arrow_colour,
                connector_arrow_size,
                "white",
            )
        else:
            self.draw_arrow_head(
                arrow_angle_points[0],
                arrow_angle_points[1],
                x2,
                y2,
                connector_arrow_colour,
                connector_arrow_size,
            )

    def draw_arrow_head(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        connector_arrow_outline_colour: str,
        connector_arrow_size: int,
        connector_arrow_fill_colour: str = "",
    ):
        """Draw an arrow head at the end of a line"""

        dx = x2 - x1
        dy = y2 - y1

        vector_length = math.sqrt(dx * dx + dy * dy)

        # normalized direction vector components
        normalised_dx = dx / vector_length
        normalised_dy = dy / vector_length

        # perpendicular vector
        perpendicular_vector_x = -normalised_dy
        perpendicular_vector_y = normalised_dx

        # points forming arrowhead
        # with length L and half-width H
        # arrowend = end
        length = connector_arrow_size
        height = connector_arrow_size - 5
        left_x = x2 - length * normalised_dx + height * perpendicular_vector_x
        left_y = y2 - length * normalised_dy + height * perpendicular_vector_y

        right_x = x2 - length * normalised_dx - height * perpendicular_vector_x
        right_y = y2 - length * normalised_dy - height * perpendicular_vector_y

        shape = [(x2, y2), (left_x, left_y), (right_x, right_y), (x2, y2)]
        outline_colour = connector_arrow_outline_colour
        if not connector_arrow_fill_colour:
            fill_colour = outline_colour
        else:
            fill_colour = connector_arrow_fill_colour
        # self.__cr.polygon(shape, fill=connector_arrow_colour)
        # self.__cr.polygon(shape, fill=fill_colour, outline=outline_colour, width=2)
        self.draw_polygon(shape, outline_colour, 2, fill_colour)

    def draw_text(
        self, x: int, y: int, text: str, font: str, font_size: int, font_colour: str
    ) -> None:
        raise NotImplementedError

    def get_text_dimension(self, text: str, font: str, font_size: int) -> tuple:
        """Get text dimension

        Args:
            text (str): Text that is used to calculate dimension
            font (str): Font name
            font_size (int): Font size

        Returns:
            (text_width (int), text_height (int)): Text dimension (width, height)
        """
        # Use Pillow's ImageFont module to get the dimensions of the text.
        # image_font = ImageFont.truetype(self.get_font_path(font), font_size)

        # ascent, descent = image_font.getmetrics()

        # _, _, right, bottom = image_font.getbbox(text)
        # font_width = right
        # font_height = bottom

        text_lines = text.splitlines()
        longest_text = max(text_lines, key=len)

        _, _, font_width, font_height = self.get_char_width(
            longest_text, font, font_size
        )

        return font_width, font_height

    def get_multitext_dimension(
        self, text: str, text_font: str, text_font_size: int
    ) -> tuple:
        """Get text dimension

        Args:
            text (str): Text that is used to calculate dimension
            font (str): Font name
            font_size (int): Font size

        Returns:
            (text_width (int), text_height (int)): Text dimension (width, height)
        """
        # Use Pillow's ImageFont module to get the dimensions of the text.

        multi_lines = []
        wrap_lines = []

        # Make '\n' work
        multi_lines = text.splitlines()

        # image_font = ImageFont.truetype(self.get_font_path(text_font), text_font_size)
        # left, _, right, bottom = image_font.getbbox("a")
        # single_char_width = right - left

        # font, _, single_char_width = self.get_single_char_width(
        #     text_font, text_font_size
        # )

        # wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, 70))

        pad = 4
        line_count = len(wrap_lines)

        max_width = 0
        max_height = 0
        for line in wrap_lines:
            font_width, font_height = self.get_text_dimension(
                line, text_font, text_font_size
            )
            max_width = max(max_width, font_width)
            max_height += font_height + pad

        return max_width, max_height

    def set_surface_size(self, width: int, height: int) -> tuple:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        return 0, 0, width, height

    def save_surface(self, filename: str) -> None:
        raise NotImplementedError


class PNGPainter(Painter):
    """A wrapper class for Pillow library"""

    def __init__(self, width: int = 500, height: int = 500) -> None:
        """Initialise the painter"""
        super().__init__(width, height)

        self.__surface = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self.__cr = ImageDraw.Draw(self.__surface)

    def draw_box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_fill_colour: str,
        box_outline_colour: str = "",
        box_outline_width: int = 0,
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        shape = super().draw_box(
            x, y, width, height, box_fill_colour, box_outline_colour, box_outline_width
        )

        if box_outline_colour:
            self.__cr.rectangle(
                shape,
                fill=box_fill_colour,
                outline=box_outline_colour,
                width=box_outline_width,
            )
        else:
            self.__cr.rectangle(shape, fill=box_fill_colour)

    def draw_rounded_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        radius, shape = super().draw_rounded_box(x, y, width, height)
        self.__cr.rounded_rectangle(shape, radius, fill=box_fill_colour)

    def draw_box_with_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: int,
        box_outline_colour: str,
        box_outline_width: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> list:
        display_lines = super().draw_box_with_text(
            box_x=box_x,
            box_y=box_y,
            box_width=box_width,
            box_height=box_height,
            box_fill_colour=box_fill_colour,
            box_outline_colour=box_outline_colour,
            box_outline_width=box_outline_width,
            text=text,
            text_alignment=text_alignment,
            text_font=text_font,
            text_font_size=text_font_size,
            text_font_colour=text_font_colour,
            style=style,
        )

        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        for x, y, line in display_lines:
            self.__cr.text((x, y), line, fill=text_font_colour, anchor="la", font=font)

    def draw_box_with_vertical_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: str,
        box_outline_colour: str,
        box_outline_width: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> None:
        """Draw a box with vertical text"""

        display_lines = super().draw_box_with_vertical_text(
            box_x=box_x,
            box_y=box_y,
            box_width=box_width,
            box_height=box_height,
            box_fill_colour=box_fill_colour,
            box_outline_colour=box_outline_colour,
            box_outline_width=box_outline_width,
            text=text,
            text_alignment=text_alignment,
            text_font=text_font,
            text_font_size=text_font_size,
            text_font_colour=text_font_colour,
            style=style,
        )

        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        # Rotate text
        for x, y, font_width, font_height, line in display_lines:
            rotated_img = Image.new("RGBA", (font_width, font_height))
            rotated_draw = ImageDraw.Draw(rotated_img)
            rotated_draw.text((0, 0), line, font=font, fill=(text_font_colour))
            rotated_img = rotated_img.rotate(90, expand=1)
            self.__surface.paste(rotated_img, (int(x), int(y)), rotated_img)

    def draw_polygon(
        self,
        points: list,
        outline_colour: str = "black",
        outline_width: int = 1,
        fill_colour: str = "",
    ):
        self.__cr.polygon(
            points, fill=fill_colour, outline=outline_colour, width=outline_width
        )

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: float,
        outline_colour: str,
        outline_width: int = 1,
        fill_colour: str = "",
    ) -> None:
        """Draw a circle"""
        points = (x - radius, y - radius, x + radius, y + radius)

        outline_red, outline_green, outline_blue = ImageColor.getrgb(outline_colour)
        if not fill_colour:
            # If no fill colour is specified, use the outline colour as the fill colour.
            fill_red, fill_green, fill_blue = outline_red, outline_green, outline_blue
            self.__cr.ellipse(
                points,
                fill=(fill_red, fill_green, fill_blue),
                outline=(outline_red, outline_green, outline_blue),
                width=outline_width,
            )
        elif fill_colour == "transparent":
            self.__cr.ellipse(
                points,
                outline=(outline_red, outline_green, outline_blue),
                width=outline_width,
            )
        else:
            fill_red, fill_green, fill_blue = ImageColor.getrgb(fill_colour)
            self.__cr.ellipse(
                points,
                fill=(fill_red, fill_green, fill_blue),
                outline=(outline_red, outline_green, outline_blue),
                width=outline_width,
            )

    def draw_dot(self, x: int, y: int, colour: str) -> None:
        """Draw a dot"""
        r, g, b = ImageColor.getrgb(colour)
        self.__cr.point((x, y), fill=(r, g, b))

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        line_colour: str,
        line_transparency: int,
        line_width: int,
        line_style: str = "solid",
    ) -> None:
        """Draw a line

        Args:
            x1 (int): Line begin X coordinate
            y1 (int): Line begin Y coordinate
            x2 (int): Line end X coordinate
            y2 (int): Line end Y coordinate
            line_colour (str): Line colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            line_transparency (int): Line transparency. 0 is opaque and 255 is transparent
            line_width (int): Line width
            line_style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """
        lines = super().draw_line(x1, y1, x2, y2, line_colour, line_width, line_style)

        r, g, b = ImageColor.getrgb(line_colour)

        for line in lines:
            if len(lines) > 1:
                self.__cr.line(
                    line, width=line_width, fill=(r, g, b, int(255 * line_transparency))
                )
            else:
                self.__cr.line(line, width=line_width, fill=(r, g, b))

    def draw_text(
        self, x: int, y: int, text: str, font: str, font_size: int, font_colour: str
    ) -> None:
        """Draw text

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            text (str): Text to draw/display
        """
        self.__cr.text(
            (x, y),
            text,
            font=ImageFont.truetype(self.get_font_path(font), font_size),
            anchor="la",
            fill=(font_colour),
        )

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        left, top, right, bottom = super().set_surface_size(width, height)
        self.__surface = self.__surface.crop((left, top, right, bottom))

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        if self.__surface is not None:
            length_x, width_y = self.__surface.size
            factor = min(1, float(1024.0 / length_x))

            factor = 1
            size = int(factor * length_x), int(factor * width_y)
            image_resize = self.__surface.resize(size, resample=Image.LANCZOS)
            image_resize.save(filename, dpi=(1200, 1200), optimize=False)


class SVGPainter(Painter):
    """A wrapper class for DrawSVG library"""

    def __init__(self, width: int = 500, height: int = 500) -> None:
        """Initialise the painter"""
        super().__init__(width, height)

        self.__cr = None
        self.elements = []

    def draw_box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_fill_colour: str,
        box_outline_colour: str = "",
        box_outline_width: int = 0,
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        shape = super().draw_box(x, y, width, height)
        if box_outline_colour:
            rectangle = dw.Rectangle(
                x,
                y,
                width,
                height,
                fill=box_fill_colour,
                stroke=box_outline_colour,
                stroke_width=box_outline_width,
            )
        else:
            rectangle = dw.Rectangle(x, y, width, height, fill=box_fill_colour)

        self.elements.append(rectangle)

    def draw_rounded_box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_fill_colour: str,
        box_outline_colour: str,
        box_outline_width: int,
    ) -> None:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        radius, shape = super().draw_rounded_box(x, y, width, height)
        rectangle = dw.Rectangle(
            x,
            y,
            width,
            height,
            rx=radius,
            ry=radius,
            fill=box_fill_colour,
            stroke=box_outline_colour,
            stroke_width=box_outline_width,
        )

        self.elements.append(rectangle)

    def draw_box_with_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: int,
        box_outline_colour: str,
        box_outline_width: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> list:
        display_lines = super().draw_box_with_text(
            box_x=box_x,
            box_y=box_y,
            box_width=box_width,
            box_height=box_height,
            box_fill_colour=box_fill_colour,
            box_outline_colour=box_outline_colour,
            box_outline_width=box_outline_width,
            text=text,
            text_alignment=text_alignment,
            text_font=text_font,
            text_font_size=text_font_size,
            text_font_colour=text_font_colour,
            style=style,
        )

        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        for x, y, line in display_lines:
            # self.__cr.text((x, y), line, fill=text_font_colour, anchor="la", font=font)
            txt = dw.Text(
                line,
                x=x,
                y=y,
                font_size=text_font_size,
                stroke=text_font_colour,
                text_anchor="start",
                dominant_baseline="hanging",
                font_family=text_font,
            )
            self.elements.append(txt)

    def draw_box_with_vertical_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: str,
        box_outline_colour: str,
        box_outline_width: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> None:
        """Draw a box with vertical text"""

        display_lines = super().draw_box_with_vertical_text(
            box_x=box_x,
            box_y=box_y,
            box_width=box_width,
            box_height=box_height,
            box_fill_colour=box_fill_colour,
            box_outline_colour=box_outline_colour,
            box_outline_width=box_outline_width,
            text=text,
            text_alignment=text_alignment,
            text_font=text_font,
            text_font_size=text_font_size,
            text_font_colour=text_font_colour,
            style=style,
        )

        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        # Rotate text
        for x, y, font_width, font_height, line in display_lines:
            # rotated_img = Image.new("RGBA", (font_width, font_height))
            # rotated_draw = ImageDraw.Draw(rotated_img)
            # rotated_draw.text((0, 0), line, font=font, fill=(text_font_colour))
            # rotated_img = rotated_img.rotate(90, expand=1)
            # self.__surface.paste(rotated_img, (int(x), int(y)), rotated_img)

            _, char_width, _, _ = self.get_char_width(line, text_font, text_font_size)

            vertical_path = dw.Path()
            vertical_path.M(x, y + char_width).V(50)
            txt = dw.Text(
                line,
                # x=x,
                # y=y,
                font_size=text_font_size,
                stroke=text_font_colour,
                text_anchor="Start",
                dominant_baseline="Hanging",
                font_family=text_font,
                # transform=f"rotate(270, {x}, {y})",
                path=vertical_path,
            )
            # txt.rotate(90, x, y)
            self.elements.append(txt)

    def draw_polygon(
        self,
        points: list,
        outline_colour: str = "",
        outline_width: int = 1,
        fill_colour: str = "",
    ):
        # self.__cr.polygon(
        #     points, fill=fill_colour, outline=outline_colour, width=outline_width
        # )

        coordinates = [val for tup in points for val in tup]

        lines = dw.Lines(
            *coordinates,
            fill=fill_colour,
            stroke=outline_colour,
            stroke_width=outline_width,
            close="true",
        )
        self.elements.append(lines)

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: float,
        outline_colour: str,
        outline_width: int = 1,
        fill_colour: str = "",
    ) -> None:
        """Draw a circle"""

        if not fill_colour:
            # If no fill colour is specified, use the outline colour as the fill colour.
            fill_colour = outline_colour
            circle = dw.Circle(
                x,
                y,
                radius,
                fill=fill_colour,
                stroke=outline_colour,
                stroke_width=outline_width,
            )
        elif fill_colour == "transparent":
            circle = dw.Circle(
                x,
                y,
                radius,
                fill="none",
                stroke=outline_colour,
                stroke_width=outline_width,
            )
        else:
            circle = dw.Circle(
                x,
                y,
                radius,
                fill=fill_colour,
                stroke=outline_colour,
                stroke_width=outline_width,
            )

        self.elements.append(circle)

    def draw_dot(self, x: int, y: int, colour: str) -> None:
        """Draw a dot"""
        r, g, b = ImageColor.getrgb(colour)
        # self.__cr.point((x, y), fill=(r, g, b))
        dot = dw.Circle(x, y, 1, fill=colour)
        self.elements.append(dot)

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        line_colour: str,
        line_transparency: int,
        line_width: int,
        line_style: str = "solid",
    ) -> None:
        """Draw a line

        Args:
            x1 (int): Line begin X coordinate
            y1 (int): Line begin Y coordinate
            x2 (int): Line end X coordinate
            y2 (int): Line end Y coordinate
            line_colour (str): Line colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            line_transparency (int): Line transparency. 0 is opaque and 255 is transparent
            line_width (int): Line width
            line_style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """
        lines = super().draw_line(x1, y1, x2, y2, line_colour, line_width, line_style)

        for line_point in lines:
            if len(lines) > 1:
                line = dw.Lines(
                    *line_point,
                    # stroke=(r, g, b, int(255 * line_transparency)),
                    stroke=line_colour,
                    stroke_width=line_width,
                )
            else:
                (src_x, src_y), (tgt_x, tgt_y) = line_point

                line = dw.Line(
                    src_x,
                    src_y,
                    tgt_x,
                    tgt_y,
                    stroke=line_colour,
                    stroke_width=1,
                )

            self.elements.append(line)

    def draw_text(
        self, x: int, y: int, text: str, font: str, font_size: int, font_colour: str
    ) -> None:
        """Draw text

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            text (str): Text to draw/display
        """
        # self.__cr.text(
        #     (x, y),
        #     text,
        #     font=ImageFont.truetype(self.get_font_path(font), font_size),
        #     anchor="la",
        #     fill=(font_colour),
        # )
        txt = dw.Text(
            text,
            x=x,
            y=y,
            font_size=font_size,
            text_anchor="start",
            dominant_baseline="Hanging",
            font_family=font,
            stroke=font_colour,
        )
        self.elements.append(txt)

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        left, top, right, bottom = super().set_surface_size(width, height)

        self.__cr = dw.Drawing(right, bottom)
        for element in self.elements:
            self.__cr.append(element)

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        # self.__cr.append(dw.Line(0, 0, 100, 100, stroke="black"))
        if self.__cr is not None:
            self.__cr.save_svg(filename)


class PainterFactory:
    """A factory class to create painter objects"""

    def __init__(self):
        self._painters = {}

    def get_painter(self, painter_name, width, height):
        if painter_name not in self._painters:
            self._painters[painter_name] = self._create_painter(
                painter_name, width, height
            )
        return self._painters[painter_name]

    def _create_painter(self, painter_name, width, height):
        return globals()[f"{painter_name.upper()}Painter"](width, height)
