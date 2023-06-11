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
import math
from itertools import count
from .painter import Painter
from .helper import Helper
from .constants import Configs


from typing import TypeVar


### This is to allow the connect method to return the same type of shape
TShape = TypeVar("TShape", bound="Shape")


@dataclass
class Connection:
    """Connection class for connecting shapes together."""

    source: TShape = field(init=True)
    target: TShape = field(init=True)
    label: str = field(init=True)
    connection_type: str = field(init=True)


@dataclass
class Shape:
    """Base class for all shapes"""

    id: int = field(init=False, default_factory=count().__next__)
    name: str = field(init=True, default="")
    lane_id: int = field(init=True, default=0)
    pool_name: str = field(init=True, default="")
    font: str = field(init=False, default=None)
    font_size: int = field(init=False, default=None)
    font_colour: str = field(init=False, default=None)
    fill_colour: str = field(init=False, default=None)
    text_alignment: str = field(init=False, default=None)

    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    origin_x: int = field(init=False, default=0)
    origin_y: int = field(init=False, default=0)
    points: dict = field(init=False, default_factory=dict)
    incoming_points: list = field(init=False, default_factory=list)
    outgoing_points: list = field(init=False, default_factory=list)
    draw_position_set: bool = field(init=False, default=False)
    x_pos_traversed: bool = field(init=False, default=False)
    y_pos_traversed: bool = field(init=False, default=False)
    grid_traversed: bool = field(init=False, default=False)

    connection_from: list = field(init=False, default_factory=list)
    connection_to: list = field(init=False, default_factory=list)

    def connect(
        self: TShape,
        target: TShape,
        label: str = "",
        connection_type: str = "sequence",
    ) -> TShape:
        """Connect two shapes

        Args:
            source (TShape): Source shape
            target (TShape): Target shape
            label (str, optional): Label for the connection. Defaults to "".
            connection_type (str, optional): Type of connection. Defaults to "sequence".

        Returns:
            TShape: Target shape

        """

        connection = Connection(self, target, label, connection_type)
        self.connection_to.append(connection)
        target.connection_from.append(self)
        return target

    def get_distance(self, source, target):
        """
        Return euclidean distance between points source and target
        assuming both to have the same number of dimensions
        """
        x1, y1 = source
        x2, y2 = target
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def find_nearest_points(self, points_source, points_target):
        """Find nearest connection points between two sets of shapes

        Args:
            points_source (dict): connection points of source shapes
            points_target (dict): connection points of target shapes

        Returns:
            (tuple), (tuple): Nearest connection points between two sets of shapes
        """
        # match (direction):
        #     case "horizontal":
        #         source_connection_points = self.get_left_right_points(points_source)
        #         target_connection_points = self.get_left_right_points(points_target)
        #     case "down":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_top_bottom_points(points_target)
        #     case "down_right":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_left_right_points(points_target)
        #     case "down_left":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_top_bottom_points(points_target)
        #     case "up":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_top_bottom_points(points_target)
        #     case "up_right":
        #         source_connection_points = self.get_left_right_points(points_source)
        #         target_connection_points = self.get_left_right_points(points_target)
        #     case "up_left":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_left_right_points(points_target)

        shortest_distance: int = float("inf")

        for source_name, source_points in points_source.items():
            for target_name, target_points in points_target.items():
                distance = self.get_distance(source_points, target_points)

                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_points = {
                        "source_name": source_name,
                        "source_points": source_points,
                        "target_name": target_name,
                        "target_points": target_points,
                        "distance": distance,
                    }

        ### remove points from source and target shapes once they are used
        del points_source[nearest_points["source_name"]]
        del points_target[nearest_points["target_name"]]

        Helper.printc(f"        Nearest : {nearest_points}")
        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def find_nearest_points_diff_pools(self, points_source, points_target):
        ...

    def get_top_bottom_points(self, points):
        """Get top and bottom points from a set of points

        Args:
            points (dict): Set of points

        Returns:
            dict: Top and bottom points
        """
        target_points = {}
        for name, point in points.items():
            if name.startswith("top") or name.startswith("bottom"):
                target_points[name] = point

        return target_points

    def get_left_right_points(self, points):
        """Get left and right points from a set of points

        Args:
            points (dict): Set of points

        Returns:
            dict: Top and bottom points
        """
        target_points = {}
        for name, point in points.items():
            if name.startswith("left") or name.startswith("right"):
                target_points[name] = point

        return target_points

    def find_nearest_points_same_pool_diff_lanes(
        self, points_source, points_target, direction: str
    ):
        """Find nearest connection points between two sets of shapes
        where source and target shapes are in the same pool but different lanes"""

        shortest_distance: int = float("inf")
        nearest_points = {}
        match (direction):
            case "down":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "down_right":
                source_connection_points = self.get_left_right_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "down_left":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "up":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "up_right":
                # source_connection_points = self.get_top_bottom_points(points_source)
                # target_connection_points = self.get_left_right_points(points_target)
                source_connection_points = points_source
                target_connection_points = points_target

            case "up_left":
                # source_connection_points = self.get_top_bottom_points(points_source)
                # target_connection_points = self.get_left_right_points(points_target)
                source_connection_points = points_source
                target_connection_points = points_target
            case "horizontal":
                source_connection_points = self.get_left_right_points(points_source)
                target_connection_points = self.get_left_right_points(points_target)

        if len(target_connection_points) == 0:
            target_connection_points = self.get_top_bottom_points(points_target)

        for source_name, source_points in source_connection_points.items():
            for target_name, target_points in target_connection_points.items():
                distance = self.get_distance(source_points, target_points)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_points = {
                        "source_name": source_name,
                        "source_points": source_points,
                        "target_name": target_name,
                        "target_points": target_points,
                        "distance": distance,
                    }

        ### remove points from source and target shapes once they are used
        del points_source[nearest_points["source_name"]]
        del points_target[nearest_points["target_name"]]

        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def find_nearest_points_diff_pool(
        self, points_source, points_target, direction: str
    ):
        """Find nearest connection points between two sets of shapes
        where source and target shapes are in the same pool but different lanes"""

        shortest_distance: int = float("inf")
        nearest_points = {}

        source_connection_points = {}
        target_connection_points = {}
        Helper.printc(f"        >>>>{direction=}")
        match (direction):
            case "down":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "down_right":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_left_right_points(points_target)
            case "down_left":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "up":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "up_right":
                source_connection_points = self.get_left_right_points(points_source)
                target_connection_points = self.get_left_right_points(points_target)
            case "up_left":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_left_right_points(points_target)
            case "horizontal":
                source_connection_points = self.get_left_right_points(points_source)
                target_connection_points = self.get_left_right_points(points_target)

        if len(target_connection_points) == 0:
            target_connection_points = self.get_top_bottom_points(points_target)

        for source_name, source_points in source_connection_points.items():
            for target_name, target_points in target_connection_points.items():
                distance = self.get_distance(source_points, target_points)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_points = {
                        "source_name": source_name,
                        "source_points": source_points,
                        "target_name": target_name,
                        "target_points": target_points,
                        "distance": distance,
                    }

        ### remove points from source and target shapes once they are used
        del points_source[nearest_points["source_name"]]
        del points_target[nearest_points["target_name"]]

        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def draw(self, painter: Painter):
        """Draw shape

        Args:
            painter (Painter): Painter object

        Returns:
            None
        """
        # for point in self.points.values():
        #     painter.draw_circle(point[0], point[1], 2, "red")

    def is_same_lane(self, source: TShape, target: TShape):
        """Check if source and target shapes are in the same lane

        Args:
            source (Shape): Source shape
            target (Shape): Target shape

        Returns:
            bool: True if source and target shapes are in the same lane
        """
        return source.lane_id == target.lane_id

    def is_same_pool(self, source: TShape, target: TShape):
        """Check if source and target shapes are in the same pool

        Args:
            source (Shape): Source shape
            target (Shape): Target shape

        Returns:
            bool: True if source and target shapes are in the same pool
        """
        return source.pool_name == target.pool_name

    def get_connection_direction(self, target: TShape):
        """Get connection direction

        Args:
            target (Shape): Target shape

        Returns:
            str: Connection direction
        """
        if self.origin_y == target.origin_y:
            return "horizontal"
        elif self.origin_y < target.origin_y:
            if self.origin_x == target.origin_x:
                return "down"
            elif self.origin_x < target.origin_x:
                return "down_right"
            else:
                return "down_left"
        else:
            if self.origin_x == target.origin_x:
                return "up"
            elif self.origin_x < target.origin_x:
                return "up_right"
            else:
                return "up_left"

    def draw_connection(self, painter: Painter):
        """Draw connection between shapes"""

        source_points = self.points
        Helper.printc(f"Draw connection for shape: [{self.name}]", 36)
        if self.connection_to:
            connection_style = "solid"
            for connection in self.connection_to:
                target_points = connection.target.points
                direction = self.get_connection_direction(connection.target)

                if self.is_same_lane(self, connection.target):
                    Helper.printc(
                        f"Same lane: Connection between [{self.name}] and [{connection.target.name}], {direction=}",
                        31,
                    )
                    (
                        point_from,
                        point_face_from,
                        point_to,
                        point_face_to,
                    ) = self.find_nearest_points(source_points, target_points)
                elif self.is_same_pool(self, connection.target):
                    Helper.printc(
                        f"Same Pool: Connection between [{self.name}] and [{connection.target.name}], {direction=}",
                        32,
                    )
                    (
                        point_from,
                        point_face_from,
                        point_to,
                        point_face_to,
                    ) = self.find_nearest_points_same_pool_diff_lanes(
                        source_points, target_points, direction
                    )
                else:  ### different pool
                    Helper.printc(
                        f"Diff Pool: Connection between [{self.name}] and [{connection.target.name}]",
                        33,
                    )
                    (
                        point_from,
                        point_face_from,
                        point_to,
                        point_face_to,
                    ) = self.find_nearest_points_diff_pool(
                        source_points, target_points, direction
                    )
                    connection_style = "dashed"

                self.outgoing_points.append(point_from)
                connection.target.incoming_points.append(point_to)
                painter.draw_line_and_arrow(
                    point_from[0],
                    point_from[1],
                    point_face_from,
                    point_to[0],
                    point_to[1],
                    point_face_to,
                    connection.label,
                    connection_style,
                    painter.connector_font,
                    painter.connector_font_size,
                    painter.connector_font_colour,
                    painter.connector_line_width,
                    painter.connector_line_colour,
                    painter.connector_arrow_colour,
                    painter.connector_arrow_size,
                )


@dataclass
class Box(Shape):
    """Box shape"""

    def __post_init__(self):
        self.width = Configs.BOX_WIDTH
        self.height = Configs.BOX_HEIGHT

    def set_draw_position(self, painter: Painter) -> tuple:
        """Set draw position of box

        Args:
            x (int): x position
            y (int): y position
            painter (Painter): Painter object

        Returns:
            tuple: x, y position
        """
        self.origin_x = self.x
        self.origin_y = self.y
        # self.x = x
        # self.y = y
        # self.width = BOX_WIDTH
        # self.height = BOX_HEIGHT
        self.points = {
            ### Uncomment the following if we need more connection points
            # "top_left": (self.x, self.y),
            # "top_right": (self.x + self.width, self.y),
            # "bottom_left": (self.x, self.y + self.height),
            # "bottom_right": (self.x + self.width, self.y + self.height),
            "left_middle": (self.x, self.y + self.height / 2),
            "top_middle": (self.x + self.width / 2, self.y),
            "right_middle": (self.x + self.width, self.y + self.height / 2),
            "bottom_middle": (self.x + self.width / 2, self.y + self.height),
            # "top_1": (self.x + self.width / 4, self.y),
            # "top_middle": (self.x + self.width / 2, self.y),
            # "top_3": (self.x + self.width / 4 * 3, self.y),
            # "bottom_1": (self.x + self.width / 4, self.y + self.height),
            # "bottom_middle": (self.x + self.width / 2, self.y + self.height),
            # "bottom_3": (self.x + self.width / 4 * 3, self.y + self.height),
            # "left_1": (self.x, self.y + self.height / 4),
            # "left_middle": (self.x, self.y + self.height / 2),
            # "left_3": (self.x, self.y + self.height / 4 * 3),
            # "right_1": (self.x + self.width, self.y + self.height / 4),
            # "right_middle": (self.x + self.width, self.y + self.height / 2),
            # "right_3": (self.x + self.width, self.y + self.height / 4 * 3),
        }
        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter):
        """Draw box"""
        painter.draw_box_with_text(
            self.x,
            self.y,
            self.width,
            self.height,
            self.fill_colour,
            self.name,
            text_alignment=self.text_alignment,
            text_font=self.font,
            text_font_size=self.font_size,
            text_font_colour=self.font_colour,
        )

        super().draw(painter)


@dataclass
class Circle(Shape):
    """Circle shape"""

    text_x: int = field(init=False)
    text_y: int = field(init=False)
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def __post_init__(self):
        self.radius = Configs.CIRCLE_RADIUS
        self.text_x: int = 0
        self.text_y: int = 0
        self.text_width: int = 0
        self.text_height: int = 0

    def set_draw_position(self, painter: Painter) -> tuple:
        """Set draw position of circle"""
        ### Circle x position starts from the circle centre, so add radius to x.
        ### But we want to cater for cases when circle and box aligned vertically.
        # self.x = int(self.x + CIRCLE_RADIUS + (BOX_WIDTH / 2) - (CIRCLE_RADIUS))
        # self.x = int(self.x + CIRCLE_RADIUS)
        # self.x = int(self.x + (BOX_WIDTH / 2) - (CIRCLE_RADIUS))
        # self.x = int(self.x - (CIRCLE_RADIUS))
        self.origin_x = self.x
        self.origin_y = self.y
        self.x = self.x + Configs.BOX_WIDTH / 2
        self.y = int(self.y + (Configs.BOX_HEIGHT / 2))
        # self.y = self.y + (BOX_HEIGHT / 2)
        self.radius = Configs.CIRCLE_RADIUS
        Helper.printc(f"<<<<{self.x=}, {self.y=}, {self.radius=}")
        self.points = {
            "right": (
                self.x + self.radius * math.cos(math.radians(0)),
                self.y + self.radius * math.sin(math.radians(0)),
            ),
            "bottom": (
                self.x + self.radius * math.cos(math.radians(90)),
                self.y + self.radius * math.sin(math.radians(90)),
            ),
            "left": (
                self.x + self.radius * math.cos(math.radians(180)),
                self.y + self.radius * math.sin(math.radians(180)),
            ),
            "top": (
                self.x + self.radius * math.cos(math.radians(270)),
                self.y + self.radius * math.sin(math.radians(270)),
            ),
        }
        self.text_width, self.text_height = painter.get_text_dimension(
            self.name, self.font, self.font_size
        )
        self.text_x = self.x + (self.width / 2) - (self.text_width / 2)
        self.text_y = self.y + self.radius

        return self.x, self.y, self.radius, self.radius

    def draw(self, painter: Painter):
        """Draw circle"""
        painter.draw_circle(self.x, self.y, self.radius, self.fill_colour)
        painter.draw_text(
            self.text_x,
            self.text_y,
            self.name,
            self.font,
            self.font_size,
            self.font_colour,
        )
        super().draw(painter)
        # painter.draw_circle(self.points["left"][0], self.points["left"][1], 2, "red")
        # painter.draw_circle(self.points["right"][0], self.points["right"][1], 2, "red")


@dataclass
class Diamond(Shape):
    """Diamond shape"""

    text_x: int = field(init=False)
    text_y: int = field(init=False)
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def __post_init__(self):
        self.text_x: int = 0
        self.text_y: int = 0
        self.text_width: int = 0
        self.text_height: int = 0
        self.width = Configs.DIAMOND_WIDTH
        self.height = Configs.DIAMOND_HEIGHT

    def set_draw_position(self, painter: Painter) -> tuple:
        """Set draw position of diamond"""

        self.origin_x = self.x
        self.origin_y = self.y
        # self.x = self.x + (BOX_WIDTH / 2) - (DIAMOND_WIDTH / 2)
        self.x = self.x + Configs.BOX_WIDTH / 2 - (Configs.DIAMOND_WIDTH / 2)
        self.y = self.y + (Configs.BOX_HEIGHT / 2) - (Configs.DIAMOND_HEIGHT / 2)

        # self.width = DIAMOND_WIDTH
        # self.height = DIAMOND_HEIGHT
        self.points = {
            "top_middle": (self.x + self.width / 2, self.y),
            "right_middle": (self.x + self.width, self.y + self.height / 2),
            "bottom_middle": (self.x + self.width / 2, self.y + self.height),
            "left_middle": (self.x, self.y + self.height / 2),
        }
        self.text_width, self.text_height = painter.get_text_dimension(
            self.name, self.font, self.font_size
        )
        self.text_x = self.x + (self.width / 2) - (self.text_width / 2)
        self.text_y = self.y + self.height

        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter):
        """Draw diamond"""
        # Helper.printc(
        #     f"draw <{self.text}>, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}"
        # )
        painter.draw_diamond(
            self.x, self.y, self.width, self.height, fill_colour=self.fill_colour
        )
        painter.draw_text(
            self.text_x,
            self.text_y,
            self.name,
            self.font,
            self.font_size,
            font_colour=self.font_colour,
        )

        super().draw(painter)
