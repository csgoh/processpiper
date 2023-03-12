import math
from PIL import Image, ImageDraw, ImageFont, ImageColor
import textwrap
from processmapper.colourtheme import ColourTheme


class Painter:

    width: int
    height: int
    output_type: str

    # Colour scheme
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

    def __init__(self, width: int = 500, height: int = 500) -> None:
        self.output_type = "PNG"
        self.__surface = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self.__cr = ImageDraw.Draw(self.__surface)
        self.width = width
        self.height = height
        self.set_background_colour("white")
        # self.draw_grid()

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

    def draw_grid(self):
        # Set the dot size and spacing
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

    def set_background_colour(self, colour) -> None:
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

        # Draw the rectangle
        self.__cr.rectangle(shape, fill=box_fill_colour)

        # Set the coordinates of the arrowhead
        vertical_midpoint = (height / 2) + y
        arrowhead_endpoint = x + width + arrowhead_width
        arrowhead = [
            (x + width, y),
            (arrowhead_endpoint, vertical_midpoint),
            (x + width, y + height),
        ]

        # Draw the arrowhead
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
        font = ImageFont.truetype(text_font, size=text_font_size)

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
        font = ImageFont.truetype(text_font, size=text_font_size)

        # print(f"box {box_x} {box_y} {box_width} {box_height}")

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
            # print(f"   line {i} '{line}' {font_width} {font_height}")

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

            # print(
            #     f"    x {x} = {box_x1} + (({box_width} - {font_width}) / 2) + (({font_height} * {i}) + ({pad} * {i}))"
            # )

            # single_line_height = font_height

            y = box_y1 + ((box_height - font_width) / 2)

            # self.__cr.text((x, y), line, fill=text_font_colour, anchor="la", font=font)

            ### Rotate text
            rotated_img = Image.new("RGBA", (font_width, font_height))
            rotated_draw = ImageDraw.Draw(rotated_img)
            print(f"text_font_colour = {text_font_colour}")
            rotated_draw.text((0, 0), line, font=font, fill=(text_font_colour))
            rotated_img = rotated_img.rotate(90, expand=1)
            # print(f"    rotated {rotated_img.size}, {x}, {y}")
            self.__surface.paste(rotated_img, (int(x), int(y)), rotated_img)

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
        points = [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2),
        ]

        # Use Pillow's ImageDraw module to draw a polygon with the given points and fill color.
        self.__cr.polygon(points, fill=fill_colour)

    def draw_circle(self, x: int, y: int, radius: float, colour: str) -> None:
        r, g, b = ImageColor.getrgb(colour)
        self.__cr.ellipse(
            (x - radius, y - radius, x + radius, y + radius), fill=(r, g, b)
        )

    def draw_dot(self, x: int, y: int, colour: str) -> None:
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
            # given a line between x1, y1 and x2, y2, divide it into multiple shorter lines
            # and draw them with a gap in between.

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
        gap_size = 10
        x1 = int(x1)
        x2 = int(x2)
        for i in range(x1, x2, gap_size):
            self.__cr.line((i, y1, i + 5, y2), fill="black", width=1)

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

        print(
            f"x1={x1}, y1={y1}, x2={x2}, y2={y2}, right_angle_point={right_angle_point}"
        )

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
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            print(f"Points {points}")
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
        x2: int,
        y2: int,
        connection_style: str,
        connector_line_width: int = 0,
        connector_line_colour: str = "",
    ):
        if x1 == x2 and y1 == y2:
            points = [(x1, y1)]
            right_angle_point = (x1, y1)

        if x1 != x2 and y1 == y2:
            points = [(x1, y1), (x2, y1)]
            right_angle_point = (x1, y1)

        if x1 == x2 and y1 != y2:
            points = [(x1, y1), (x1, y2)]
            right_angle_point = (x1, y1)

        if x1 != x2 and y1 != y2:
            # print(x1, y1, x2, y2)
            points = [(x1, y1), (x1, y2), (x2, y2)]
            right_angle_point = (x1, y2)
            # for point in points:
            #     self.draw_circle(point[0], point[1], 4, "yellow")

        if x1 > x2:
            if y1 <= y2:
                if abs(y1 - y2) == 10:
                    elbow_height = 40
                    points = [
                        (x1, y1),
                        (x1, y1 - elbow_height),
                        (x2, y1 - elbow_height),
                        (x2, y2),
                    ]
                    # for point in points:
                    #     self.draw_circle(point[0], point[1], 2, "magenta")
                    right_angle_point = (x2, y1 - elbow_height)
                if abs(y1 - y2) >= 100:
                    elbow_height = 40
                    points = [
                        (x1, y1),
                        (x1, y1 + elbow_height),
                        (x2, y1 + elbow_height),
                        (x2, y2),
                    ]
                    # for point in points:
                    #     self.draw_circle(point[0], point[1], 2, "orange")
                    right_angle_point = (x2, y1 - elbow_height)
            elif y1 > y2:
                if len(points) == 0:
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

    def draw_arrow(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
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
        right_angle_point = self.draw_right_angle_line(
            x1,
            y1,
            x2,
            y2,
            connection_style,
            connector_line_width,
            connector_line_colour,
        )
        label_x_pos, label_y_pos = right_angle_point

        label_w, label_h = self.get_multitext_dimension(label, "arial.ttf", 12)
        if label_x_pos == x1 and label_y_pos == y1:
            ### There is no right angle point
            label_x_pos = max(x1 + 5, x1 + (((x2 - x1) - label_w) / 2))
            label_y_pos = y1 - label_h - 3
        else:
            label_x_pos += 5
            label_y_pos = label_y_pos - label_h - 3

        # print(
        #     f"drawing [{label}] at {label_x_pos}, {label_y_pos}, {label_w}, {label_h}"
        # )
        self.draw_text(
            label_x_pos,
            label_y_pos,
            label,
            connector_font,
            connector_font_size,
            connector_font_color,
        )
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
        connector_arrow_colour: str,
        connector_arrow_size: int,
    ):
        # self.set_colour("black")

        dx = x2 - x1
        dy = y2 - y1

        # vector length
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
        self.__cr.polygon(shape, fill=connector_arrow_colour)

    def get_box_connection_points(self, x, y, width, height):
        ### get the connection points for the corners of the box

        return [
            (x, y),  # top left
            (x + width, y),  # top right
            (x + width, y + height),  # bottom right
            (x, y + height),  # bottom left
            (x, y + height / 2),  # middle left
            (x + width / 2, y),  # middle top
            (x + width, y + height / 2),  # middle right
            (x + width / 2, y + height),  # middle bottom
        ]

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
            font=ImageFont.truetype(font, font_size),
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
        image_font = ImageFont.truetype(font, font_size)

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
        image_font = ImageFont.truetype(text_font, text_font_size)

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

    def get_display_text_position(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        alignment: str,
        text_font: str,
        text_font_size: int,
    ) -> tuple:
        """Get text position relative to the rectangle box

        Args:
            x (int): Rectangle X coordinate
            y (int): Rectangle Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            text (str): Text used to calculate position
            alignment (str): Text alignment. Eg. left, centre, right

        Returns:
            (text_x (int), text_y (int)): Text x and y coordinates
        """
        text_width, text_height = self.get_text_dimension(
            text, text_font, text_font_size
        )

        if alignment == "centre":
            text_x_pos = (width / 2) - (text_width / 2)
        elif alignment == "right":
            text_x_pos = width - text_width - 5
        elif alignment == "left":
            text_x_pos = 0 + 5

        text_y_pos = (height / 2) + (text_height / 2)

        return x + text_x_pos, y + text_y_pos

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        # height += self.bottom_margin
        left, top, right, bottom = 0, 0, width, height
        # print(
        #     f"resize surface > left: {left}, top: {top}, right: {right}, bottom: {bottom}"
        # )
        # extend the surface to fit the text

        self.__surface = self.__surface.crop((left, top, right, bottom))

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        if self.output_type == "PNG":
            if self.__surface is not None:
                self.__surface.save(filename)
