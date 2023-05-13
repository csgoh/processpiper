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
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter, ImageEnhance
import textwrap
from .colourtheme import ColourTheme
from .helper import Helper


class Painter:
    """Painter class to draw the diagram"""

    width: int
    height: int
    output_type: str

    ### Colour scheme attributes - Start
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
    ### Colour scheme attributes - End

    def __init__(self, width: int = 500, height: int = 500) -> None:
        """Initialise the painter"""
        self.output_type = "PNG"
        self.__surface = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        ### Set DPI
        # self.__surface.info["dpi"] = (1600, 1600)
        self.__cr = ImageDraw.Draw(self.__surface)

        self.width = width
        self.height = height

    def set_colour_theme(self, colour_theme: str) -> None:
        """Set colour palette

        Args:
            colour_palette (str): Name of the colour palette. Eg. OrangePeel
        """
        self.colour_theme = ColourTheme(colour_theme)
        (self.background_colour,) = self.colour_theme.get_colour_theme_settings(
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

    def get_font_path(self, font_name: str) -> str:
        """Get the path to the font file"""
        if sys.platform.startswith("win"):  # Windows
            return os.path.join("C:\\", "Windows", "Fonts", f"{font_name}.ttf")
        elif sys.platform.startswith("darwin"):  # macOS
            return os.path.join(
                "/", "System", "Library", "Fonts", "Supplemental", f"{font_name}.ttf"
            )
        elif sys.platform.startswith("linux"):  # Linux
            font_dir = f"/usr/share/fonts/truetype/msttcorefonts"

            if os.path.exists(os.path.join(font_dir, f"{font_name}.ttf")):
                return os.path.join(font_dir, f"{font_name}.ttf")
            else:
                ### This is cater for cases where msttcorefonts is not installed
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
            raise Exception("Unsupported operating system")

    def draw_grid(self):
        """Draw a grid of dots to help with alignment"""
        ### Set the dot size and spacing
        spacing = 10

        ### Draw the grid of dots
        for x in range(0, self.width, spacing):
            for y in range(0, self.height, spacing):
                if x > 0 and y > 0:
                    self.draw_dot(x, y, "grey")
                    if x % 50 == 0 or y % 50 == 0:
                        self.draw_dot(x, y, "blue")
                    if x % 100 == 0 or y % 100 == 0:
                        self.draw_dot(x, y, "red")

    def set_background_colour(self, colour) -> None:
        """Set the background colour"""
        self.__cr.rectangle((0, 0, self.width, self.height), fill=colour)

    def draw_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        shape = [(x, y), (x + width, y + height)]
        self.__cr.rectangle(shape, fill=box_fill_colour)

    def draw_box_with_outline(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_outline_colour: str,
        box_outline_transparency: int,
        box_outline_width: int,
        box_fill_colour: str,
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        shape = [(x, y), (x + width, y + height)]
        self.__cr.rectangle(
            shape,
            fill=box_fill_colour,
            outline=box_outline_colour,
            width=box_outline_width,
        )

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
        shape = [(x, y), (x + width, y + height)]
        radius = 20
        self.__cr.rounded_rectangle(shape, radius, fill=box_fill_colour)

    def draw_arrowhead_box(
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
        arrowhead_width = 10
        width = width - arrowhead_width
        shape = [(x, y), (x + width, y + height)]

        ### Draw the rectangle
        self.__cr.rectangle(shape, fill=box_fill_colour)

        ### Set the coordinates of the arrowhead
        vertical_midpoint = (height / 2) + y
        arrowhead_endpoint = x + width + arrowhead_width
        arrowhead = [
            (x + width, y),
            (arrowhead_endpoint, vertical_midpoint),
            (x + width, y + height),
        ]

        ### Draw the arrowhead
        self.__cr.polygon(arrowhead, fill=box_fill_colour)

    def draw_box_with_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: str,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> None:
        """Draw a box with text"""
        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        multi_lines = []
        wrap_lines = []

        ### Make '\n' work
        multi_lines = text.splitlines()

        left, _, right, bottom = font.getbbox("a")
        single_char_width = right - left

        ### wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, int(box_width / single_char_width)))

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
                )
            case "rounded":
                self.draw_rounded_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case "arrowhead":
                self.draw_arrowhead_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case _:
                raise ValueError("Invalid style")

        pad = 4
        line_count = len(wrap_lines)

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

            self.__cr.text((x, y), line, fill=text_font_colour, anchor="la", font=font)

    def draw_box_with_vertical_text(
        self,
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: str,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
        style: str = "rectangle",
    ) -> None:
        """Draw a box with vertical text"""
        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        multi_lines = []
        wrap_lines = []

        ### Make '\n' work
        multi_lines = text.splitlines()

        left, _, right, bottom = font.getbbox("a")
        single_char_width = right - left

        ### wrap text
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
                )
            case "rounded":
                self.draw_rounded_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case "arrowhead":
                self.draw_arrowhead_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case _:
                raise ValueError("Invalid style")

        pad = 5
        line_count = len(wrap_lines)

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

            ### Rotate text
            rotated_img = Image.new("RGBA", (font_width, font_height))
            rotated_draw = ImageDraw.Draw(rotated_img)
            rotated_draw.text((0, 0), line, font=font, fill=(text_font_colour))
            rotated_img = rotated_img.rotate(90, expand=1)
            self.__surface.paste(rotated_img, (int(x), int(y)), rotated_img)

    def draw_polygon(
        self,
        points: list,
        outline_colour: str = "",
        outline_width: int = 1,
        fill_colour: str = "",
    ):
        self.__cr.polygon(
            points, fill=fill_colour, outline=outline_colour, width=outline_width
        )

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

        ### Calculate the coordinates of the four points of the diamond.
        points = [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2),
        ]

        ### Use Pillow's ImageDraw module to draw a polygon with the given points and fill color.
        self.__cr.polygon(points, fill=fill_colour)

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
        if fill_colour == "":
            ### If no fill colour is specified, use the outline colour as the fill colour.
            outline_red, outline_green, outline_blue = ImageColor.getrgb(outline_colour)
            fill_red, fill_green, fill_blue = outline_red, outline_green, outline_blue
        else:
            outline_red, outline_green, outline_blue = ImageColor.getrgb(outline_colour)
            fill_red, fill_green, fill_blue = ImageColor.getrgb(fill_colour)
        self.__cr.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
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
        r, g, b = ImageColor.getrgb(line_colour)

        def linspace(start, stop, n):
            if n == 1:
                yield stop
                return
            h = (stop - start) / (n - 1)
            for i in range(n):
                yield start + h * i

        if line_style == "solid":
            self.__cr.line(
                ((x1, y1), (x2, y2)),
                width=line_width,
                fill=(r, g, b),
            )
        elif line_style == "dashed":
            ### given a line between x1, y1 and x2, y2, divide it into multiple shorter lines
            ### and draw them with a gap in between.

            ### Calculate the number of dashes
            gap_counts = int((y2 - y1) / 7)

            for i, (x, y) in enumerate(
                zip(
                    linspace(x1, x2, gap_counts),
                    linspace(y1, y2, gap_counts),
                )
            ):
                if i % 2 == 0:
                    self.__cr.line(
                        (x, y, x, y + 10),
                        width=line_width,
                        fill=(r, g, b, int(255 * line_transparency)),
                    )

    def draw_vertical_dashed_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        connector_line_width,
        connector_line_colour,
    ):
        """Draw a vertical dashed line"""
        gap_size = 10
        y1 = int(y1)
        y2 = int(y2)
        if y1 > y2:
            for i in range(y2, y1, gap_size):
                if i - 5 < y2:
                    new_y = y2
                else:
                    new_y = i - 5
                self.__cr.line(
                    (x1, i, x2, new_y),
                    fill=connector_line_colour,
                    width=connector_line_width,
                )
        else:
            for i in range(y1, y2, gap_size):
                if i + 5 > y2:
                    new_y = y2
                else:
                    new_y = i + 5
                self.__cr.line(
                    (x1, i, x2, new_y),
                    fill=connector_line_colour,
                    width=connector_line_width,
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
                # print(f">> {i}, {y1}, {x2}, {y2}")
                if i - 5 < x2:
                    new_x = x2
                else:
                    new_x = i - 5
                # print(f"x1 > x2    {i}, {y1}, {new_x}, {y2}")
                self.__cr.line((i, y1, new_x, y2), fill="black", width=1)
        else:
            for i in range(x1, x2, gap_size):
                if i + 5 > x2:
                    new_x = x2
                else:
                    new_x = i + 5
                # print(f"x2 < x1    {i}, {y1}, {new_x}, {y2}")
                self.__cr.line((i, y1, new_x, y2), fill="black", width=1)

        # for i in range(x1, x2, gap_size):
        #     print(f"    {i}, {y1}, {i + 5}, {y2}")
        #     self.__cr.line((i, y1, i + 5, y2), fill="black", width=1)

    def draw_right_angle_dot_line(self, x1: int, y1: int, x2: int, y2: int):
        if x1 < x2:
            if y1 < y2:
                right_angle_point = (x2, y1)
            else:
                right_angle_point = (x1, y2)
        else:
            if y1 < y2:
                right_angle_point = (x1, y2)
            else:
                right_angle_point = (x2, y1)

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
        Helper.printc(
            f"      x1: {x1}, y1: {y1}, face1: {face_source}, x2: {x2}, y2: {y2}, face2: {face_target}"
        )
        if x1 == x2 and y1 == y2:
            Helper.printc(
                f"   A: right_angle_line: x1 == x2 and y1 == y2: {x1}, {y1}, {x2}, {y2}"
            )
            points = [(x1, y1)]
            right_angle_point = (x1, y1)

        if x1 != x2 and y1 == y2:
            Helper.printc(
                f"   B: right_angle_line: x1 != x2 and y1 == y2: {x1}, {y1}, {x2}, {y2}"
            )
            points = [(x1, y1), (x2, y1)]
            right_angle_point = (x1, y1)

        if x1 == x2 and y1 != y2:
            Helper.printc(
                f"   C: right_angle_line: x1 == x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}"
            )
            points = [(x1, y1), (x1, y2)]
            right_angle_point = (x1, y1)

        if x1 != x2 and y1 != y2:
            # check if face1 string contained the word "right"
            if face_source.find("bottom") != -1:
                Helper.printc(
                    f"   D-bottom: right_angle_line: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}"
                )
                # if so, then the line should be drawn from the bottom side of the box
                points = [(x1, y1), (x1, y2), (x2, y2)]
                right_angle_point = (x1, y2)
            elif face_source.find("right") != -1:
                Helper.printc(
                    f"   D-right: right_angle_line: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}"
                )
                if face_target.find("left") != -1:
                    # points = [(x1, y1), (x1, y2), (x2, y2)]
                    elbow_height = 40
                    points = [
                        (x1, y1),
                        (x1 + elbow_height, y1),
                        (x1 + elbow_height, y2),
                        (x2, y2),
                    ]
                    right_angle_point = (x1 + elbow_height, y2)
                else:
                    points = [(x1, y1), (x2, y1), (x2, y2)]
                    right_angle_point = (x2, y1)
            elif face_source.find("top") != -1 and face_target.find("top") != -1:
                Helper.printc(
                    f"   D-top: right_angle_line: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}"
                )
                # draw 1 right angle line
                elbow_height = 40
                points = [
                    (x1, y1),
                    (x1, y1 - elbow_height),
                    (x2, y1 - elbow_height),
                    (x2, y2),
                ]
                right_angle_point = (x2, y2 - elbow_height)
            elif face_source.find("top") != -1 and face_target.find("bottom") != -1:
                Helper.printc(
                    f"   D-top/bottom: right_angle_line: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}"
                )
                # draw 1 right angle line
                elbow_height = 20
                points = [
                    (x1, y1),
                    (x1, y1 - elbow_height),
                    (x2, y1 - elbow_height),
                    (x2, y2),
                ]
                right_angle_point = (x2, y1 - elbow_height)
            else:
                Helper.printc(
                    f"   D-else: right_angle_line: x1 != x2 and y1 != y2: {x1}, {y1}, {x2}, {y2}"
                )
                # if so, then the line should be drawn from the bottom side of the box
                points = [(x1, y1), (x1, y2), (x2, y2)]
                right_angle_point = (x1, y2)
            # for point in points:
            #     self.draw_circle(point[0], point[1], 4, "yellow")

        if x1 > x2:
            if y1 <= y2:
                if abs(y1 - y2) == 10:
                    Helper.printc(
                        f"   E: right_angle_line: x1 > x2 and y1 <= y2: {x1}, {y1}, {x2}, {y2}"
                    )
                    elbow_height = 40
                    points = [
                        (x1, y1),
                        (x1, y1 - elbow_height),
                        (x2, y1 - elbow_height),
                        (x2, y2),
                    ]
                    right_angle_point = (x2, y1 - elbow_height)
                if abs(y1 - y2) >= 100:
                    if (
                        face_source.find("bottom") != -1
                        and face_target.find("right") != -1
                    ):
                        Helper.printc(
                            f"   F1: right_angle_line: x1 > x2 and y1 <= y2: {x1}, {y1}, {x2}, {y2}"
                        )
                        elbow_height = 40
                        points = [
                            (x1, y1),
                            (x1, y2),
                            (x2, y2),
                        ]
                        right_angle_point = (x1, y2)
                    else:
                        Helper.printc(
                            f"   F2: right_angle_line: x1 > x2 and y1 <= y2: {x1}, {y1}, {x2}, {y2}"
                        )
                        elbow_height = 40
                        points = [
                            (x1, y1),
                            (x1, y1 + elbow_height),
                            (x2, y1 + elbow_height),
                            (x2, y2),
                        ]
                        right_angle_point = (x2, y1 - elbow_height)
            elif y1 > y2:
                if len(points) == 0:
                    Helper.printc(
                        f"   G: right_angle_line: x1 > x2 and y1 > y2: {x1}, {y1}, {x2}, {y2}"
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
                    right_angle_point = (x2, y2 + elbow_height)

        if connection_style == "dashed":
            self.draw_dashed_line(points, connector_line_width, connector_line_colour)
        else:
            self.__cr.line(
                points, fill=(connector_line_colour), width=connector_line_width
            )
        return right_angle_point

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

        right_angle_point = self.draw_right_angle_line(
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

        label_x_pos, label_y_pos = right_angle_point

        label_w, label_h = self.get_multitext_dimension(label, connector_font, 12)
        if label_x_pos == x1 and label_y_pos == y1:
            ### There is no right angle point
            label_x_pos = max(x1 + 5, x1 + (((x2 - x1) - label_w) / 2))
            label_y_pos = y1 - label_h - 3
        else:
            label_x_pos += 5
            label_y_pos = label_y_pos - label_h - 3

        self.draw_text(
            label_x_pos,
            label_y_pos,
            label,
            connector_font,
            connector_font_size,
            connector_font_color,
        )

        if connection_style == "dashed":
            ### Draw round circle at the beginning of the line
            self.draw_circle(x1, y1, 6, connector_arrow_colour, "white")

            ### Draw white arrow head at the end of the line

            self.draw_arrow_head(
                right_angle_point[0],
                right_angle_point[1],
                x2,
                y2,
                connector_arrow_colour,
                connector_arrow_size,
                "white",
            )
        else:
            self.draw_arrow_head(
                right_angle_point[0],
                right_angle_point[1],
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

        ### normalized direction vector components
        normalised_dx = dx / vector_length
        normalised_dy = dy / vector_length

        ### perpendicular vector
        perpendicular_vector_x = -normalised_dy
        perpendicular_vector_y = normalised_dx

        ### points forming arrowhead
        ### with length L and half-width H
        ### arrowend = end
        length = connector_arrow_size
        height = connector_arrow_size - 5
        left_x = x2 - length * normalised_dx + height * perpendicular_vector_x
        left_y = y2 - length * normalised_dy + height * perpendicular_vector_y

        right_x = x2 - length * normalised_dx - height * perpendicular_vector_x
        right_y = y2 - length * normalised_dy - height * perpendicular_vector_y

        shape = [(x2, y2), (left_x, left_y), (right_x, right_y), (x2, y2)]
        if connector_arrow_fill_colour == "":
            outline_colour = connector_arrow_outline_colour
            fill_colour = outline_colour
        else:
            outline_colour = connector_arrow_outline_colour
            fill_colour = connector_arrow_fill_colour
        # self.__cr.polygon(shape, fill=connector_arrow_colour)
        self.__cr.polygon(shape, fill=fill_colour, outline=outline_colour, width=2)

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
        image_font = ImageFont.truetype(self.get_font_path(font), font_size)

        # ascent, descent = image_font.getmetrics()

        _, _, right, bottom = image_font.getbbox(text)
        font_width = right
        font_height = bottom

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
        image_font = ImageFont.truetype(self.get_font_path(text_font), text_font_size)

        multi_lines = []
        wrap_lines = []

        ### Make '\n' work
        multi_lines = text.splitlines()

        left, _, right, bottom = image_font.getbbox("a")
        single_char_width = right - left

        ### wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, 70))

        pad = 4
        line_count = len(wrap_lines)

        max_width = 0
        max_height = 0
        for i, line in enumerate(wrap_lines):
            font_width, font_height = self.get_text_dimension(
                line, text_font, text_font_size
            )
            max_width = max(max_width, font_width)
            max_height += font_height + pad

        return max_width, max_height

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        left, top, right, bottom = 0, 0, width, height

        self.__surface = self.__surface.crop((left, top, right, bottom))

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        if self.output_type == "PNG":
            if self.__surface is not None:
                # anti_alias_image = self.__surface.filter(ImageFilter.SMOOTH_MORE)
                # anti_alias_image.save(filename)
                # Set the DPI to 300
                # info = self.__surface.info.copy()
                # info["dpi"] = (600, 600)

                # Save the image with the new DPI
                # self.__surface.save(filename, **info)

                length_x, width_y = self.__surface.size
                factor = min(1, float(1024.0 / length_x))

                factor = 1
                size = int(factor * length_x), int(factor * width_y)
                image_resize = self.__surface.resize(size, Image.ANTIALIAS)
                image_resize.save(filename, dpi=(1200, 1200), optimize=False)

                # enhancer = ImageEnhance.Sharpness(self.__surface)
                # im_s_1 = enhancer.enhance(3)
                # im_s_1.save("sharp.png")
                # self.__surface.save(filename)
