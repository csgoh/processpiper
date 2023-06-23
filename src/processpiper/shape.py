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

    painter: Painter = field(init=False, default=None)

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

    def find_nearest_points(self, target_shape, direction: str, all_shapes: list):
        """Find nearest connection points between two sets of shapes

        Args:
            points_source (dict): connection points of source shapes
            points_target (dict): connection points of target shapes

        Returns:
            (tuple), (tuple): Nearest connection points between two sets of shapes
        """
        points_source = self.points
        points_target = target_shape.points
        shortest_distance: int = float("inf")

        Helper.printc(
            f"        >>>> {points_source=}", 35, show_level="draw_connection"
        )
        Helper.printc(
            f"        >>>> {points_target=}", 35, show_level="draw_connection"
        )

        nearest_points = {}
        (
            source_connection_points,
            target_connection_points,
        ) = self.get_same_lanes_connection_points(
            direction, points_source, points_target
        )

        ### Remove points that are colliding with other shapes
        collision_names = []
        for source_name, source_points in source_connection_points.items():
            for target_name, target_points in target_connection_points.items():
                nearest_points = {
                    "source_name": source_name,
                    "source_points": source_points,
                    "target_name": target_name,
                    "target_points": target_points,
                    "distance": 0,
                }
                Helper.printc(
                    f"        >>>># {nearest_points=}", 35, show_level="draw_connection"
                )
                points = self.painter.get_points(nearest_points)
                # loop through points, skip one point at a time
                self.get_collision_names(
                    target_shape,
                    all_shapes,
                    collision_names,
                    source_name,
                    target_name,
                    points,
                )

        for source_name, source_points in points_source.items():
            for target_name, target_points in points_target.items():
                if direction == "right" and (
                    (
                        source_name.startswith("top")
                        and target_name.startswith("top") is False
                    )
                    or (
                        source_name.startswith("bottom")
                        and target_name.startswith("bottom") is False
                    )
                ):
                    continue
                distance = self.get_distance(source_points, target_points)

                for col_source_name, col_target_name in collision_names:
                    if (
                        source_name == col_source_name
                        and target_name == col_target_name
                    ):
                        ### If collision found, set distance to infinity so that it will not be selected
                        distance = float("inf")

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

        Helper.printc(
            f"        ### Nearest : {nearest_points}", show_level="draw_connection"
        )
        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def get_top_bottom_points(self, points):
        # sourcery skip: dict-comprehension, inline-immediately-returned-variable
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
        # sourcery skip: dict-comprehension, inline-immediately-returned-variable
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

    def check_line_collision(self, line1_start, line1_end, line2_start, line2_end):
        """
        This function checks if two lines intersect and returns True if they do.

        Args:
          line1_start: The starting point of the first line segment.
          line1_end: The end point of the first line segment.
          line2_start: The starting point of the second line segment.
          line2_end: The end point of the second line segment.

        Returns:
          a boolean value indicating whether or not two lines intersect.
        """

        # calculate the direction of the lines
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end

        if ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)) == 0:
            return False
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (
            (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        )
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (
            (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        )

        # if uA and uB are between 0-1, lines are colliding
        if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
            # optionally, draw a circle where the lines meet
            intersection_x = x1 + (uA * (x2 - x1))
            intersection_y = y1 + (uA * (y2 - y1))
            ### self.painter.draw_circle(intersectionX, intersectionY, 5, "red")
            Helper.printc(
                f"        >>>> intersection ({intersection_x}, {intersection_y})",
                35,
                show_level="draw_connection",
            )

            return True
        return False

    def check_shape_collision(self, line_start, line_end, shape: TShape):
        """
        This function checks if a line collides with any of the sides of a given shape.

        Args:
          line_start: The starting point of a line segment, represented as a tuple of x and y
        coordinates.
          line_end: The end point of a line segment that is being checked for collision with a shape.
          shape (TShape): TShape is a custom class or data structure that represents a shape in a Tetris
        game. It contains information about the shape's position (x, y), its origin point (origin_x,
        origin_y), width, height, and the blocks that make up the shape. The function is checking for

        Returns:
          a boolean value indicating whether there is a collision between the given line segment and any
        of the four sides of the given shape.
        """
        if shape.x == shape.origin_x and shape.y == shape.origin_y:
            rx, ry = shape.x, shape.y
            rw, rh = shape.width, shape.height
        else:
            rx, ry = shape.origin_x, shape.origin_y
            rw, rh = Configs.BOX_WIDTH, Configs.BOX_HEIGHT

        left_line_start = (rx, ry)
        left_line_end = (rx, ry + rh)
        left = self.check_line_collision(
            line_start, line_end, left_line_start, left_line_end
        )

        right_line_start = (rx + rw, ry)
        right_line_end = (rx + rw, ry + rh)
        right = self.check_line_collision(
            line_start, line_end, right_line_start, right_line_end
        )

        top_line_start = (rx, ry)
        top_line_end = (rx + rw, ry)
        top = self.check_line_collision(
            line_start, line_end, top_line_start, top_line_end
        )

        bottom_line_start = (rx, ry + rh)
        bottom_line_end = (rx + rw, ry + rh)
        bottom = self.check_line_collision(
            line_start, line_end, bottom_line_start, bottom_line_end
        )
        return left or right or top or bottom

    def check_collision(self, line_start, line_end, shapes: list, target_shape: TShape):
        """
        This function checks for collisions between a line and a list of shapes, excluding the current
        shape and a target shape.

        Args:
          line_start: The starting point of a line segment used to check for collisions with shapes.
          line_end: The end point of a line segment used to check for collisions with shapes in a list.
          shapes (list): a list of shapes that are being checked for collision with the line segment
        defined by line_start and line_end.
          target_shape (TShape): TShape is likely a custom class or data type used in the code. It is
        not clear from the given code what properties or methods this class has. However, it is being
        used as a parameter in the check_collision method to identify a specific shape that is being
        targeted for collision detection.

        Returns:
          a boolean value indicating whether a collision was found or not.
        """
        # Helper.printc(f"        >>>>@ {len(shapes)=}", 34)
        collision_found = False
        for shape in shapes:
            if self == shape or target_shape == shape:
                ...
            elif self.check_shape_collision(line_start, line_end, shape):
                Helper.printc(
                    f"        >>>> Colliding with [{shape.name}]",
                    31,
                    show_level="draw_connection",
                )
                collision_found = True
        return collision_found

    def find_nearest_points_same_pool_diff_lanes(
        self, target_shape, direction: str, all_shapes: list
    ):
        """Find nearest connection points between two sets of shapes
        where source and target shapes are in the same pool but different lanes"""
        points_source = self.points
        points_target = target_shape.points
        shortest_distance: int = float("inf")
        nearest_points = {}
        (
            source_connection_points,
            target_connection_points,
        ) = self.get_diff_lanes_connection_points(
            direction, points_source, points_target
        )

        ### Remove points that are colliding with other shapes
        collision_names = []
        for source_name, source_points in source_connection_points.items():
            for target_name, target_points in target_connection_points.items():
                nearest_points = {
                    "source_name": source_name,
                    "source_points": source_points,
                    "target_name": target_name,
                    "target_points": target_points,
                    "distance": 0,
                }
                Helper.printc(
                    f"        >>>># {nearest_points=}", 35, show_level="draw_connection"
                )
                points = self.painter.get_points(nearest_points)
                # loop through points, skip one point at a time
                self.get_collision_names(
                    target_shape,
                    all_shapes,
                    collision_names,
                    source_name,
                    target_name,
                    points,
                )

        ### Find nearest points
        for source_name, source_points in source_connection_points.items():
            for target_name, target_points in target_connection_points.items():
                distance = self.get_distance(source_points, target_points)
                for col_source_name, col_target_name in collision_names:
                    if (
                        source_name == col_source_name
                        and target_name == col_target_name
                    ):
                        ### If collision found, set distance to infinity so that it will not be selected
                        distance = float("inf")

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

        Helper.printc(nearest_points, 35, show_level="draw_connection")
        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def get_collision_names(
        self,
        target_shape,
        all_shapes,
        collision_names,
        source_name,
        target_name,
        points,
    ):
        collision_found = False
        for i in range(0, len(points) - 1, 2):
            Helper.printc(
                f"        >>>> Line {i=}, {points[i]}->{points[i+1]}",
                35,
                show_level="draw_connection",
            )
            collision_found = self.check_collision(
                points[i], points[i + 1], all_shapes, target_shape
            )
            if collision_found:
                Helper.printc(
                    f"        >>>> COLLISION FOUND: {source_name}->{target_name}",
                    31,
                    show_level="draw_connection",
                )
                break
        if collision_found:
            # Helper.printc(
            #     f"        >>>> {collision_found=}, [{source_name} {target_name})]",
            #     31,
            # )
            collision_names.append((source_name, target_name))

    def get_same_lanes_connection_points(self, direction, points_source, points_target):
        # match (direction):
        #     case "down":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_top_bottom_points(points_target)
        #     case "down_right":
        #         source_connection_points = points_source
        #         target_connection_points = points_target
        #     case "down_left":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_top_bottom_points(points_target)
        #     case "up":
        #         source_connection_points = self.get_top_bottom_points(points_source)
        #         target_connection_points = self.get_top_bottom_points(points_target)
        #     case "up_right":
        #         source_connection_points = points_source
        #         target_connection_points = points_target
        #         Helper.printc(
        #             f"        >>>>{direction=} {source_connection_points=} {target_connection_points=}",
        #             show_level="draw_connection",
        #         )

        #     case "up_left":
        #         source_connection_points = points_source
        #         target_connection_points = points_target
        #     case "left" | "right":
        #         source_connection_points = self.get_left_right_points(points_source)
        #         # target_connection_points = self.get_left_right_points(points_target)
        #         target_connection_points = points_target

        # if len(source_connection_points) == 0:
        #     source_connection_points = points_source

        # if len(target_connection_points) == 0:
        #     target_connection_points = self.get_top_bottom_points(points_target)

        source_connection_points = points_source
        target_connection_points = points_target

        Helper.printc(
            f"        >>>>{direction=} {source_connection_points=} {target_connection_points=}",
            show_level="draw_connection",
        )

        return source_connection_points, target_connection_points

    def get_diff_lanes_connection_points(self, direction, points_source, points_target):
        match (direction):
            case "down":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "down_right":
                source_connection_points = points_source
                target_connection_points = points_target
            case "down_left":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "up":
                source_connection_points = self.get_top_bottom_points(points_source)
                target_connection_points = self.get_top_bottom_points(points_target)
            case "up_right":
                source_connection_points = points_source
                target_connection_points = points_target
                Helper.printc(
                    f"        >>>>{direction=} {source_connection_points=} {target_connection_points=}",
                    show_level="draw_connection",
                )

            case "up_left":
                source_connection_points = points_source
                target_connection_points = points_target
            case "left" | "right":
                source_connection_points = self.get_left_right_points(points_source)
                target_connection_points = self.get_left_right_points(points_target)

        if len(target_connection_points) == 0:
            target_connection_points = self.get_top_bottom_points(points_target)

        return source_connection_points, target_connection_points

    def find_nearest_points_diff_pool(
        self, target_shape, direction: str, all_shapes_points: list
    ):
        """Find nearest connection points between two sets of shapes
        where source and target shapes are in the same pool but different lanes"""

        points_source = self.points
        points_target = target_shape.points
        shortest_distance: int = float("inf")
        nearest_points = {}

        source_connection_points = {}
        target_connection_points = {}
        Helper.printc(f"        >>>> {direction=}", show_level="draw_connection")
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
            case "left" | "right":
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
        # sourcery skip: assign-if-exp, merge-else-if-into-elif
        """Get connection direction

        Args:
            target (Shape): Target shape

        Returns:
            str: Connection direction
        """
        if self.origin_y == target.origin_y:
            if self.origin_x < target.origin_x:
                return "right"
            else:
                return "left"
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

    def draw_connection(self, painter: Painter, all_shapes: list):
        """Draw connection between shapes"""
        self.painter = painter

        Helper.printc(
            f"Draw connection for shape: [{self.name}]",
            36,
            show_level="draw_connection",
        )
        if self.connection_to:
            connection_style = "solid"
            for connection in self.connection_to:
                direction = self.get_connection_direction(connection.target)

                if self.is_same_lane(self, connection.target):
                    Helper.printc(
                        f"Same lane: Connection between [{self.name}] and [{connection.target.name}], {direction=}",
                        31,
                        show_level="draw_connection",
                    )
                    (
                        point_from,
                        point_face_from,
                        point_to,
                        point_face_to,
                    ) = self.find_nearest_points(
                        connection.target, direction, all_shapes
                    )
                elif self.is_same_pool(self, connection.target):
                    Helper.printc(
                        f"Same Pool: Connection between [{self.name}] and [{connection.target.name}], {direction=}",
                        32,
                        show_level="draw_connection",
                    )
                    (
                        point_from,
                        point_face_from,
                        point_to,
                        point_face_to,
                    ) = self.find_nearest_points_same_pool_diff_lanes(
                        connection.target, direction, all_shapes
                    )
                else:  ### different pool
                    Helper.printc(
                        f"Diff Pool: Connection between [{self.name}] and [{connection.target.name}]",
                        33,
                        show_level="draw_connection",
                    )
                    (
                        point_from,
                        point_face_from,
                        point_to,
                        point_face_to,
                    ) = self.find_nearest_points_diff_pool(
                        connection.target, direction, all_shapes
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
        # self.width = Configs.BOX_WIDTH
        # self.height = Configs.BOX_HEIGHT
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
        self.width = Configs.CIRCLE_RADIUS * 2
        self.height = Configs.CIRCLE_RADIUS * 2

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
        Helper.printc(
            f"<<<<{self.x=}, {self.y=}, {self.radius=}", show_level="draw_position"
        )
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
