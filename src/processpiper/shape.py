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
from .coordinate import Coordinate, Side


from typing import TypeVar


# -- This is to allow the connect method to return the same type of shape
TShape = TypeVar("TShape", bound="Shape")


class TooManyConnectionsException(Exception):
    pass


@dataclass
class Connection:
    """Connection class for connecting shapes together."""

    source: TShape = field(init=True)
    target: TShape = field(init=True)
    label: str = field(init=True)
    connection_type: str = field(init=True)
    source_connection_side: Side = field(init=True)
    target_connection_side: Side = field(init=True)


@dataclass
class Shape:
    """Base class for all shapes"""

    id: int = field(init=False, default_factory=count().__next__)
    name: str = field(init=True, default="")
    lane_id: int = field(init=True, default=0)
    pool_name: str = field(init=True, default="")

    font: str = field(init=False)
    font_size: int = field(init=False)
    font_colour: str = field(init=False)
    fill_colour: str = field(init=False)
    text_alignment: str = field(init=False)

    coord: Coordinate = field(init=True, default=Coordinate())
    origin_coord: Coordinate = field(init=True, default=Coordinate())
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)

    top_middle: Coordinate = field(init=False)
    right_middle: Coordinate = field(init=False)
    bottom_middle: Coordinate = field(init=False)
    left_middle: Coordinate = field(init=False)

    points: dict = field(init=False, default_factory=dict)
    incoming_points: list = field(init=False, default_factory=list)
    outgoing_points: list = field(init=False, default_factory=list)
    draw_position_set: bool = field(init=False, default=False)
    x_pos_traversed: bool = field(init=False, default=False)
    y_pos_traversed: bool = field(init=False, default=False)
    grid_traversed: bool = field(init=False, default=False)
    connection_traversed: bool = field(init=False, default=False)

    connection_from: list = field(init=False, default_factory=list)
    connection_to: list = field(init=False, default_factory=list)

    painter: Painter = field(init=False, default=None)

    def __post_init__(self):
        self.top_middle = Coordinate()
        self.top_middle.side = Side.TOP
        self.right_middle = Coordinate()
        self.right_middle.side = Side.RIGHT
        self.bottom_middle = Coordinate()
        self.bottom_middle.side = Side.BOTTOM
        self.left_middle = Coordinate()
        self.left_middle.side = Side.LEFT

    def connectX(
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

        # --Perform connection count validation
        self_connection_count = len(self.connection_to) + len(self.connection_from)
        if self_connection_count > 4:
            raise TooManyConnectionsException(
                f"Element '{self.name}' has exceeded 4 incoming and outgoing connections.\n"
                + "An element can only have a maximum of 4 incoming and outgoing connections combined.\n"
                + "Please use gateway to combine connections before connecting to this element."
            )

        target_connection_count = len(target.connection_to) + len(
            target.connection_from
        )
        if target_connection_count > 4:
            raise TooManyConnectionsException(
                f"Element '{target.name}' has exceeded 4 incoming and outgoing connections.\n"
                + "An element can only have a maximum of 4 incoming and outgoing connections combined.\n"
                + "Please use gateway to combine connections before connecting to this element."
            )

        return target

    def connect(
        self: TShape,
        target: TShape,
        label: str = "",
        connection_type: str = "sequence",
        source_connection_side: Side = Side.NONE,
        target_connection_side: Side = Side.NONE,
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

        connection = Connection(
            self,
            target,
            label,
            connection_type,
            source_connection_side,
            target_connection_side,
        )
        self.connection_to.append(connection)
        target.connection_from.append(self)

        # --Perform connection count validation
        self_connection_count = len(self.connection_to) + len(self.connection_from)
        if self_connection_count > 4:
            raise TooManyConnectionsException(
                f"Element '{self.name}' has exceeded 4 incoming and outgoing connections.\n"
                + "An element can only have a maximum of 4 incoming and outgoing connections combined.\n"
                + "Please use gateway to combine connections before connecting to this element."
            )

        target_connection_count = len(target.connection_to) + len(
            target.connection_from
        )
        if target_connection_count > 4:
            raise TooManyConnectionsException(
                f"Element '{target.name}' has exceeded 4 incoming and outgoing connections.\n"
                + "An element can only have a maximum of 4 incoming and outgoing connections combined.\n"
                + "Please use gateway to combine connections before connecting to this element."
            )

        return target

    def get_distance(self, source, target):
        """
        Return euclidean distance between points source and target
        assuming both to have the same number of dimensions
        """
        x1, y1 = source
        x2, y2 = target
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def find_nearest_pointsX(self, target_shape, direction: str, all_shapes: list):
        """Find nearest connection points between two sets of shapes

        Args:
            points_source (dict): connection points of source shapes
            points_target (dict): connection points of target shapes

        Returns:
            (tuple), (tuple): Nearest connection points between two sets of shapes
        """

        points_source = {}
        if self.left_middle.connected is False:
            points_source["left_middle"] = self.left_middle.get_xy()
        if self.right_middle.connected is False:
            points_source["right_middle"] = self.right_middle.get_xy()
        if self.top_middle.connected is False:
            points_source["top_middle"] = self.top_middle.get_xy()
        if self.bottom_middle.connected is False:
            points_source["bottom_middle"] = self.bottom_middle.get_xy()

        points_target = {}
        if target_shape.left_middle.connected is False:
            points_target["left_middle"] = target_shape.left_middle.get_xy()
        if target_shape.right_middle.connected is False:
            points_target["right_middle"] = target_shape.right_middle.get_xy()
        if target_shape.top_middle.connected is False:
            points_target["top_middle"] = target_shape.top_middle.get_xy()
        if target_shape.bottom_middle.connected is False:
            points_target["bottom_middle"] = target_shape.bottom_middle.get_xy()

        shortest_distance: int = float("inf")

        # Print just the keys of points_source
        Helper.printc(
            f"        >>>> source: {points_source.keys()}", show_level="draw_connection"
        )
        Helper.printc(
            f"        >>>> target: {points_target.keys()}", show_level="draw_connection"
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
                    f"              > source: [green]{nearest_points['source_name']}[/green], target: [cyan]{nearest_points['target_name']}[/cyan]",
                    35,
                    show_level="draw_connection",
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

        # --mark points from source and target shapes once they are used
        match nearest_points["source_name"]:
            case "right_middle":
                self.right_middle.connected = True
            case "left_middle":
                self.left_middle.connected = True
            case "top_middle":
                self.top_middle.connected = True
            case "bottom_middle":
                self.bottom_middle.connected = True

        match nearest_points["target_name"]:
            case "right_middle":
                target_shape.right_middle.connected = True
            case "left_middle":
                target_shape.left_middle.connected = True
            case "top_middle":
                target_shape.top_middle.connected = True
            case "bottom_middle":
                target_shape.bottom_middle.connected = True

        Helper.printc(
            f"***** AFTER SRC: {len(points_source)}", show_level="draw_connection"
        )
        Helper.printc(
            f"***** AFTER TGT: {len(points_source)}", show_level="draw_connection"
        )

        Helper.printc(
            f"        >>>> FINAL Nearest : [green]{nearest_points['source_name']}[/green], [cyan]{nearest_points['target_name']}[/cyan]",
            show_level="draw_connection",
        )
        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def find_nearest_points(
        self,
        target: TShape,
        source_side: Side = Side.NONE,
        target_side: Side = Side.NONE,
        all_shapes: list = [],
    ):
        """
        Draws a connection between two shapes
        """

        source_attributes = dir(self)
        target_attributes = dir(target)

        source_middle_attributes = [
            attribute for attribute in source_attributes if "middle" in attribute
        ]
        target_middle_attributes = [
            attribute for attribute in target_attributes if "middle" in attribute
        ]

        Helper.printc(
            f"        Specified Sides: [yellow]({source_side}) => ({target_side})[/yellow]",
            show_level="draw_connection",
        )
        # Helper.printc(
        #     f"        >>>> source: {source_middle_attributes}",
        #     show_level="draw_connection",
        # )
        # Helper.printc(
        #     f"        >>>> target: {target_middle_attributes}",
        #     show_level="draw_connection",
        # )
        if source_side is Side.NONE and target_side is Side.NONE:
            print(f"        >>>> Searching nearest points")

            shortest_duration = float("inf")

            shortest_source_coord: Coordinate
            shortest_target_coord: Coordinate

            points = ()
            for source_point in source_middle_attributes:
                source_point_coord = getattr(self, source_point)
                if source_point_coord.connected is True:
                    continue
                for target_point in target_middle_attributes:
                    target_point_coord = getattr(target, target_point)
                    if target_point_coord.connected is True:
                        continue

                    Helper.printc(
                        f"              > source: [green]{source_point_coord.side}[/green], target: [cyan]{target_point_coord.side}[/cyan]",
                        35,
                        show_level="draw_connection",
                    )
                    # -- check for collision
                    points = self.determine_right_angle_points(
                        source_point_coord, target_point_coord
                    )
                    if self.is_collision(points, target, all_shapes):
                        continue

                    distance = self.get_distance(
                        source_point_coord.get_xy(),
                        target_point_coord.get_xy(),
                    )
                    if distance < shortest_duration:
                        shortest_duration = int(distance)
                        shortest_source_coord = source_point_coord
                        shortest_target_coord = target_point_coord

                        # print(
                        #     f"      {shortest_duration=} between source.{shortest_source_coord.side} and target.{shortest_target_coord.side}"
                        # )

            shortest_source_coord.connected = True
            shortest_target_coord.connected = True

            points = self.determine_right_angle_points(
                shortest_source_coord, shortest_target_coord
            )

            Helper.printc(
                f"        >>>> FINAL Nearest : [green]{shortest_source_coord.side}[/green], [cyan]{shortest_target_coord.side}[/cyan]",
                show_level="draw_connection",
            )

            # draw_connection(image, points, source.name + "->" + target.name)
        else:
            Helper.printc(
                f"        >>>> Getting coordinates for specified sides [yellow]{source_side} -> {target_side}[/yellow]",
                show_level="draw_connection",
            )
            if any(source_side.name.lower() in s for s in source_middle_attributes):
                source_coord = getattr(self, source_side.name.lower() + "_middle")
            if any(target_side.name.lower() in s for s in target_middle_attributes):
                target_coord = getattr(target, target_side.name.lower() + "_middle")

            source_coord.connected = True
            target_coord.connected = True

            points = self.determine_right_angle_points(source_coord, target_coord)
            # draw_connection(image, points, source.name + "->" + target.name)

        return points

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
            # Helper.printc(
            #     f"        >>>> intersection ({intersection_x}, {intersection_y})",
            #     35,
            #     show_level="draw_connection",
            # )

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
        game. It contains information about the shape's position (x, y), its origin point (origin_coord.x_pos,
        origin_coord.y_pos), width, height, and the blocks that make up the shape. The function is checking for

        Returns:
          a boolean value indicating whether there is a collision between the given line segment and any
        of the four sides of the given shape.
        """
        if (
            shape.coord.x_pos == shape.origin_coord.x_pos
            and shape.coord.y_pos == shape.origin_coord.y_pos
        ):
            rx, ry = shape.coord.x_pos, shape.coord.y_pos
            rw, rh = shape.width, shape.height
        else:
            rx, ry = shape.origin_coord.x_pos, shape.origin_coord.y_pos
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
        collision_shape = ""
        for shape in shapes:
            if self == shape or target_shape == shape:
                ...
            elif self.check_shape_collision(line_start, line_end, shape):
                collision_found = True
                collision_shape = shape.name
                break
        return collision_found, collision_shape

    def find_nearest_points_same_pool_diff_lanes(
        self, target_shape, direction: str, all_shapes: list
    ):
        """Find nearest connection points between two sets of shapes
        where source and target shapes are in the same pool but different lanes"""
        points_source = {}
        if self.left_middle.connected is False:
            points_source["left_middle"] = self.left_middle.get_xy()
        if self.right_middle.connected is False:
            points_source["right_middle"] = self.right_middle.get_xy()
        if self.top_middle.connected is False:
            points_source["top_middle"] = self.top_middle.get_xy()
        if self.bottom_middle.connected is False:
            points_source["bottom_middle"] = self.bottom_middle.get_xy()

        points_target = {}
        if target_shape.left_middle.connected is False:
            points_target["left_middle"] = target_shape.left_middle.get_xy()
        if target_shape.right_middle.connected is False:
            points_target["right_middle"] = target_shape.right_middle.get_xy()
        if target_shape.top_middle.connected is False:
            points_target["top_middle"] = target_shape.top_middle.get_xy()
        if target_shape.bottom_middle.connected is False:
            points_target["bottom_middle"] = target_shape.bottom_middle.get_xy()
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

        # --mark points from source and target shapes once they are used
        match nearest_points["source_name"]:
            case "right_middle":
                self.right_middle.connected = True
            case "left_middle":
                self.left_middle.connected = True
            case "top_middle":
                self.top_middle.connected = True
            case "bottom_middle":
                self.bottom_middle.connected = True

        match nearest_points["target_name"]:
            case "right_middle":
                target_shape.right_middle.connected = True
            case "left_middle":
                target_shape.left_middle.connected = True
            case "top_middle":
                target_shape.top_middle.connected = True
            case "bottom_middle":
                target_shape.bottom_middle.connected = True

        Helper.printc(nearest_points, 35, show_level="draw_connection")
        return (
            nearest_points["source_points"],
            nearest_points["source_name"],
            nearest_points["target_points"],
            nearest_points["target_name"],
        )

    def is_collision(self, points, target_shape, all_shapes):
        collision_found = False
        for i in range(len(points) - 1):
            # Helper.printc(
            #     f"        >>>> Line {i=}, {points[i]}->{points[i+1]}",
            #     35,
            #     show_level="draw_connection",
            # )
            collision_found, collision_shape = self.check_collision(
                points[i], points[i + 1], all_shapes, target_shape
            )
            if collision_found:
                Helper.printc(
                    "\t" * 4
                    + f">>>> [red]***COLLISION FOUND***[/red] [orange4]{collision_shape}[/orange4]: [green]\[{source_name}][/green] -> [cyan]\[{target_name}][cyan]",
                    show_level="draw_connection",
                )
                break
        return collision_found

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
        for i in range(0, len(points) - 1, 1):
            # Helper.printc(
            #     f"        >>>> Line {i=}, {points[i]}->{points[i+1]}",
            #     35,
            #     show_level="draw_connection",
            # )
            collision_found, collision_shape = self.check_collision(
                points[i], points[i + 1], all_shapes, target_shape
            )
            if collision_found:
                Helper.printc(
                    "\t" * 4
                    + f">>>> [red]***COLLISION FOUND***[/red] [orange4]{collision_shape}[/orange4]: [green]\[{source_name}][/green] -> [cyan]\[{target_name}][cyan]",
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
        source_connection_points = points_source
        target_connection_points = points_target

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

        points_source = {}
        if self.left_middle.connected is False:
            points_source["left_middle"] = self.left_middle.get_xy()
        if self.right_middle.connected is False:
            points_source["right_middle"] = self.right_middle.get_xy()
        if self.top_middle.connected is False:
            points_source["top_middle"] = self.top_middle.get_xy()
        if self.bottom_middle.connected is False:
            points_source["bottom_middle"] = self.bottom_middle.get_xy()

        points_target = {}
        if target_shape.left_middle.connected is False:
            points_target["left_middle"] = target_shape.left_middle.get_xy()
        if target_shape.right_middle.connected is False:
            points_target["right_middle"] = target_shape.right_middle.get_xy()
        if target_shape.top_middle.connected is False:
            points_target["top_middle"] = target_shape.top_middle.get_xy()
        if target_shape.bottom_middle.connected is False:
            points_target["bottom_middle"] = target_shape.bottom_middle.get_xy()
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

        # --mark points from source and target shapes once they are used
        match nearest_points["source_name"]:
            case "right_middle":
                self.right_middle.connected = True
            case "left_middle":
                self.left_middle.connected = True
            case "top_middle":
                self.top_middle.connected = True
            case "bottom_middle":
                self.bottom_middle.connected = True

        match nearest_points["target_name"]:
            case "right_middle":
                target_shape.right_middle.connected = True
            case "left_middle":
                target_shape.left_middle.connected = True
            case "top_middle":
                target_shape.top_middle.connected = True
            case "bottom_middle":
                target_shape.bottom_middle.connected = True

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
        if self.origin_coord.y_pos == target.coord.y_pos:
            if self.origin_coord.x_pos < target.origin_coord.x_pos:
                return "right"
            else:
                return "left"
        elif self.origin_coord.y_pos < target.origin_coord.y_pos:
            if self.origin_coord.x_pos == target.origin_coord.x_pos:
                return "down"
            elif self.origin_coord.x_pos < target.origin_coord.x_pos:
                return "down_right"
            else:
                return "down_left"
        else:
            if self.origin_coord.x_pos == target.origin_coord.x_pos:
                return "up"
            elif self.origin_coord.x_pos < target.origin_coord.x_pos:
                return "up_right"
            else:
                return "up_left"

    def draw_connectionX(self, painter: Painter, all_shapes: list):
        """Draw connection between shapes"""
        if self.connection_traversed:
            Helper.printc(
                f"  [orange4]{self.name} is already traversed[/]",
                show_level="draw_connection",
            )
            return

        self.connection_traversed = True
        self.painter = painter

        Helper.printc(
            f"Draw connection for shape: [red]\[{self.name}][/red]",
            show_level="draw_connection",
        )
        if self.connection_to:
            connection_style = "solid"
            for connection in self.connection_to:
                direction = self.get_connection_direction(connection.target)

                if self.is_same_lane(self, connection.target):
                    Helper.printc(
                        f"  Same lane: [red]\[{self.name}] -> \[{connection.target.name}][/red], {direction=}",
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
                        f"  Same Pool: \[{self.name}] -> \[{connection.target.name}], {direction=}",
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
                        f"  Diff Pool: \[{self.name}] -> \[{connection.target.name}]",
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
                next_shape = connection.target
                next_shape.draw_connection(painter, all_shapes)

    def draw_connection(self, painter: Painter, all_shapes: list):
        """Draw connection between shapes"""
        if self.connection_traversed:
            Helper.printc(
                f"  [orange4]{self.name} is already traversed[/]",
                show_level="draw_connection",
            )
            return

        self.connection_traversed = True
        self.painter = painter

        Helper.printc(
            f"Draw connection for shape: [red]\[{self.name}][/red]",
            show_level="draw_connection",
        )
        if self.connection_to:
            connection_style = "solid"

            for connection in self.connection_to:
                if self.is_same_pool(self, connection.target):
                    Helper.printc(
                        f"  Same lane: [red]\[{self.name}] -> \[{connection.target.name}][/red]",
                        show_level="draw_connection",
                    )
                else:  ### different pool
                    Helper.printc(
                        f"  Diff Pool: \[{self.name}] -> \[{connection.target.name}]",
                        show_level="draw_connection",
                    )
                    connection_style = "dashed"

                connection_points = self.find_nearest_points(
                    connection.target,
                    connection.source_connection_side,
                    connection.target_connection_side,
                    all_shapes,
                )

                self.outgoing_points.append(connection_points[0])
                connection.target.incoming_points.append(connection_points[-1])
                painter.draw_connection(
                    connection_points,
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
                next_shape = connection.target
                next_shape.draw_connection(painter, all_shapes)

    def calc_right_angle_count(
        self, source_coord: Coordinate, target_coord: Coordinate
    ):
        """
        Return the number of right angle points to be drawn
        between source and target coordinates
        """

        source_side = source_coord.side
        target_side = target_coord.side

        right_angle_count = 0

        # -- RIGHT side treatment --
        if source_side == Side.RIGHT:
            if target_side == Side.LEFT:
                if (
                    source_coord.x_pos < target_coord.x_pos
                    and source_coord.y_pos == target_coord.y_pos
                ):
                    right_angle_count = 0
                elif source_coord.x_pos < target_coord.x_pos:
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.TOP:
                if (
                    source_coord.x_pos < target_coord.x_pos
                    and source_coord.y_pos < target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

            if target_side == Side.RIGHT:
                if (
                    source_coord.x_pos == target_coord.x_pos
                    and source_coord.y_pos != target_coord.y_pos
                ):
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.BOTTOM:
                if (
                    source_coord.x_pos < target_coord.x_pos
                    and source_coord.y_pos > target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

        # -- LEFT side treatment --
        if source_side == Side.LEFT:
            if target_side == Side.RIGHT:
                if (
                    source_coord.x_pos > target_coord.x_pos
                    and source_coord.y_pos == target_coord.y_pos
                ):
                    right_angle_count = 0
                elif source_coord.x_pos > target_coord.x_pos:
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.TOP:
                if (
                    source_coord.x_pos > target_coord.x_pos
                    and source_coord.y_pos < target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

            if target_side == Side.LEFT:
                if (
                    source_coord.x_pos
                    != target_coord.x_pos
                    # and source_coord.y_pos == target_coord.y_pos
                ):
                    right_angle_count = 4
                else:
                    right_angle_count = 2

            if target_side == Side.BOTTOM:
                if (
                    source_coord.x_pos > target_coord.x_pos
                    and source_coord.y_pos > target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

        # -- TOP side treatment --
        if source_side == Side.TOP:
            if target_side == Side.BOTTOM:
                if (
                    source_coord.x_pos == target_coord.x_pos
                    and source_coord.y_pos > target_coord.y_pos
                ):
                    right_angle_count = 0
                elif source_coord.y_pos > target_coord.y_pos:
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.RIGHT:
                if (
                    source_coord.x_pos > target_coord.x_pos
                    and source_coord.y_pos > target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

            if target_side == Side.TOP:
                if source_coord.y_pos == target_coord.y_pos:
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.LEFT:
                if (
                    source_coord.x_pos < target_coord.x_pos
                    and source_coord.y_pos > target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

        # -- BOTTOM side treatment --
        if source_side == Side.BOTTOM:
            if target_side == Side.TOP:
                if (
                    source_coord.x_pos == target_coord.x_pos
                    and source_coord.y_pos < target_coord.y_pos
                ):
                    right_angle_count = 0
                elif source_coord.y_pos < target_coord.y_pos:
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.RIGHT:
                if (
                    source_coord.x_pos > target_coord.x_pos
                    and source_coord.y_pos < target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

            if target_side == Side.BOTTOM:
                if (
                    source_coord.x_pos != target_coord.x_pos
                    and source_coord.y_pos == target_coord.y_pos
                ):
                    right_angle_count = 2
                else:
                    right_angle_count = 4

            if target_side == Side.LEFT:
                if (
                    source_coord.x_pos < target_coord.x_pos
                    and source_coord.y_pos < target_coord.y_pos
                ):
                    right_angle_count = 1
                else:
                    right_angle_count = 3

        # Helper.printc(
        #     f"                  > Right Angle Count: {right_angle_count}",
        #     show_level="draw_connection",
        # )

        return right_angle_count

    def determine_right_angle_points(
        self, source_coord: Coordinate, target_coord: Coordinate
    ):
        """Determine the points for a right angle connection"""

        right_angle_count = self.calc_right_angle_count(source_coord, target_coord)

        mid_point = []

        if right_angle_count == 0:
            return (source_coord.get_xy(), target_coord.get_xy())
        elif right_angle_count == 1:
            if source_coord.side == Side.RIGHT and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.append((target_coord.x_pos, source_coord.y_pos))
            if source_coord.side == Side.LEFT and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.append((target_coord.x_pos, source_coord.y_pos))
            if source_coord.side == Side.TOP and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.append((source_coord.x_pos, target_coord.y_pos))
            if source_coord.side == Side.BOTTOM and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.append((source_coord.x_pos, target_coord.y_pos))
            return (source_coord.get_xy(), mid_point[0], target_coord.get_xy())
        elif right_angle_count == 2:
            if source_coord.side == Side.RIGHT and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                if source_coord.x_pos == target_coord.x_pos:
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                source_coord.y_pos,
                            ),
                            (
                                source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos,
                            ),
                        )
                    )
                else:
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos
                                + (abs(target_coord.x_pos - source_coord.x_pos) / 2),
                                source_coord.y_pos,
                            ),
                            (
                                source_coord.x_pos
                                + (abs(target_coord.x_pos - source_coord.x_pos) / 2),
                                target_coord.y_pos,
                            ),
                        )
                    )
            if source_coord.side == Side.LEFT and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.extend(
                    (
                        (
                            source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            source_coord.y_pos,
                        ),
                        (
                            source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            target_coord.y_pos,
                        ),
                    )
                )
            if source_coord.side == Side.TOP and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                if source_coord.y_pos == target_coord.y_pos:
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos,
                                source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos,
                                source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                        )
                    )
                else:
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos,
                                target_coord.y_pos
                                + ((source_coord.y_pos - target_coord.y_pos) / 2),
                            ),
                            (
                                target_coord.x_pos,
                                target_coord.y_pos
                                + ((source_coord.y_pos - target_coord.y_pos) / 2),
                            ),
                        )
                    )
                # print(f"{mid_point=}")
            if source_coord.side == Side.BOTTOM and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.extend(
                    (
                        (
                            source_coord.x_pos,
                            source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        ),
                        (
                            target_coord.x_pos,
                            source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        ),
                    )
                )
            return (
                source_coord.get_xy(),
                mid_point[0],
                mid_point[1],
                target_coord.get_xy(),
            )
        elif right_angle_count == 3:
            # RIGHT, TOP/BOTTOM
            if source_coord.side == Side.RIGHT and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.append(
                    (
                        source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        source_coord.y_pos,
                    )
                )
                if target_coord.side == Side.TOP:
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos,
                                target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                        )
                    )
                else:  # BOTTOM
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos,
                                target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                        )
                    )
            # LEFT, TOM/BOTTOM
            if source_coord.side == Side.LEFT and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.append(
                    (
                        source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                        source_coord.y_pos,
                    )
                )
                if target_coord.side == Side.TOP:
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos,
                                target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                        )
                    )
                else:  # BOTTOM
                    mid_point.extend(
                        (
                            (
                                source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos,
                                target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                        )
                    )
            # TOP, RIGHT/LEFT
            if source_coord.side == Side.TOP and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.append(
                    (
                        source_coord.x_pos,
                        source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                    )
                )
                if target_coord.side == Side.LEFT:
                    mid_point.extend(
                        (
                            (
                                target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                                source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos,
                            ),
                        )
                    )
                else:  # RIGHT
                    mid_point.extend(
                        (
                            (
                                target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            ),
                            (
                                target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos,
                            ),
                        )
                    )
            # BOTTOM, RIGHT/LEFT
            if source_coord.side == Side.BOTTOM and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.append((source_coord.x_pos, source_coord.y_pos + 50))
                if target_coord.side == Side.LEFT:
                    mid_point.extend(
                        (
                            (
                                target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                                source_coord.y_pos + 50,
                            ),
                            (
                                target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos,
                            ),
                        )
                    )
                else:
                    mid_point.extend(
                        (
                            (
                                target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                source_coord.y_pos + 50,
                            ),
                            (
                                target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                                target_coord.y_pos,
                            ),
                        )
                    )
            return (
                source_coord.get_xy(),
                mid_point[0],
                mid_point[1],
                mid_point[2],
                target_coord.get_xy(),
            )
        elif right_angle_count == 4:
            # RIGHT, LEFT/RIGHT
            # ─┐ ◄─┐     ─┐  ┌─►
            #  └───┘      └──┘
            if source_coord.side == Side.RIGHT and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.append(
                    (
                        source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        source_coord.y_pos,
                    )
                )
                mid_point.append(
                    (
                        source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                    )
                )
                if target_coord.side == Side.LEFT:
                    mid_point.append(
                        (
                            target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                        )
                    )
                    mid_point.append(
                        (
                            target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                            target_coord.y_pos,
                        )
                    )
                else:  # RIGHT
                    mid_point.append(
                        (
                            target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                            source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                        )
                    )
                    mid_point.append(
                        (
                            target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                            target_coord.y_pos,
                        )
                    )

            # LEFT, RIGHT/LEFT
            # ┌─ ◄─┐     ┌─  ┌►
            # └────┘     └───┘
            if source_coord.side == Side.LEFT and target_coord.side in [
                Side.LEFT,
                Side.RIGHT,
            ]:
                mid_point.append(
                    (
                        (source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH),
                        source_coord.y_pos,
                    )
                )
                mid_point.append(
                    (
                        (source_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH),
                        source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                    )
                )
                if target_coord.side == Side.LEFT:
                    mid_point.append(
                        (
                            (target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH),
                            source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                        )
                    )
                    mid_point.append(
                        (
                            (target_coord.x_pos - Configs.RIGHT_ANGLE_LINE_LENGTH),
                            target_coord.y_pos,
                        )
                    )

                else:  # RIGHT
                    mid_point.append(
                        (
                            (target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH),
                            source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                        )
                    )
                    mid_point.append(
                        (
                            (target_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH),
                            target_coord.y_pos,
                        )
                    )

            # TOP, BOTTOM/TOP
            # ┌──┐      ┌──┐
            # ▲  │         │
            # └──┘      ┌──┘
            #           ▼
            if source_coord.side == Side.TOP and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.append(
                    (
                        source_coord.x_pos,
                        source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                    )
                )
                mid_point.append(
                    (
                        source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                        source_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                    )
                )
                if target_coord.side == Side.TOP:
                    mid_point.append(
                        (
                            source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                            target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )
                    mid_point.append(
                        (
                            target_coord.x_pos,
                            target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )
                else:  # BOTTOM
                    mid_point.append(
                        (
                            source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                            target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )
                    mid_point.append(
                        (
                            target_coord.x_pos,
                            target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )

            # BOTTOM, TOP/BOTTOM
            #           ▲
            # ┌──┐      └──┐
            # ▼  │         │
            # └──┘      └──┘

            if source_coord.side == Side.BOTTOM and target_coord.side in [
                Side.TOP,
                Side.BOTTOM,
            ]:
                mid_point.append(
                    (
                        source_coord.x_pos,
                        source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                    )
                )
                mid_point.append(
                    (
                        source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                        source_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                    )
                )
                if target_coord.side == Side.TOP:
                    mid_point.append(
                        (
                            source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                            target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )
                    mid_point.append(
                        (
                            target_coord.x_pos,
                            target_coord.y_pos - Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )
                else:  # BOTTOM
                    mid_point.append(
                        (
                            source_coord.x_pos + Configs.RIGHT_ANGLE_LINE_LENGTH * 2,
                            target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )
                    mid_point.append(
                        (
                            target_coord.x_pos,
                            target_coord.y_pos + Configs.RIGHT_ANGLE_LINE_LENGTH,
                        )
                    )

            return (
                source_coord.get_xy(),
                mid_point[0],
                mid_point[1],
                mid_point[2],
                mid_point[3],
                target_coord.get_xy(),
            )


@dataclass
class Box(Shape):
    """Box shape"""

    def __post_init__(self):
        super().__post_init__()
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
        self.origin_coord = self.coord

        # -- Calculate the connections coordinate --
        self.top_middle.x_pos = self.coord.x_pos + int(self.width / 2)
        self.top_middle.y_pos = self.coord.y_pos

        self.right_middle.x_pos = self.coord.x_pos + self.width
        self.right_middle.y_pos = self.coord.y_pos + int(self.height / 2)

        self.bottom_middle.x_pos = self.coord.x_pos + int(self.width / 2)
        self.bottom_middle.y_pos = self.coord.y_pos + self.height

        self.left_middle.x_pos = self.coord.x_pos
        self.left_middle.y_pos = self.coord.y_pos + int(self.height / 2)

        return self.coord.x_pos, self.coord.y_pos, self.width, self.height

    def draw(self, painter: Painter):
        """Draw box"""
        painter.draw_box_with_text(
            self.coord.x_pos,
            self.coord.y_pos,
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

    text_coord: Coordinate = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.radius = Configs.CIRCLE_RADIUS
        self.text_coord = Coordinate()
        self.text_coord.x_pos = 0
        self.text_coord.y_pos = 0
        self.text_width: int = 0
        self.text_height: int = 0
        self.width = Configs.CIRCLE_RADIUS * 2
        self.height = Configs.CIRCLE_RADIUS * 2

    def set_draw_position(self, painter: Painter) -> tuple:
        """Set draw position of circle"""
        self.origin_coord = self.coord
        self.coord.x_pos = self.coord.x_pos + (Configs.BOX_WIDTH / 2)
        self.coord.y_pos = self.coord.y_pos + (Configs.BOX_HEIGHT / 2)
        self.coord.y_pos = self.coord.y_pos

        self.radius = Configs.CIRCLE_RADIUS
        Helper.printc(
            f"<<<<{self.coord.x_pos=}, {self.coord.y_pos=}, {self.radius=}",
            show_level="draw_position",
        )

        # -- Calculate the connections coordinate --
        self.top_middle.x_pos = self.coord.x_pos + int(
            self.radius * math.cos(math.radians(270))
        )
        self.top_middle.y_pos = self.coord.y_pos + int(
            self.radius * math.sin(math.radians(270))
        )

        self.right_middle.x_pos = self.coord.x_pos + int(
            self.radius * math.cos(math.radians(0))
        )
        self.right_middle.y_pos = self.coord.y_pos + int(
            self.radius * math.sin(math.radians(0))
        )

        self.bottom_middle.x_pos = self.coord.x_pos + int(
            self.radius * math.cos(math.radians(90))
        )
        self.bottom_middle.y_pos = self.coord.y_pos + int(
            self.radius * math.sin(math.radians(90))
        )

        self.left_middle.x_pos = self.coord.x_pos + int(
            self.radius * math.cos(math.radians(180))
        )
        self.left_middle.y_pos = self.coord.y_pos + int(
            self.radius * math.sin(math.radians(180))
        )

        self.text_width, self.text_height = painter.get_text_dimension(
            self.name, self.font, self.font_size
        )
        self.text_coord.x_pos = (
            self.coord.x_pos + (self.width / 2) - (self.text_width / 2)
        )
        self.text_coord.y_pos = self.coord.y_pos + self.radius

        Helper.printc(
            f"        >>>> 1. Shape Text: {self.name}, {self.text_coord.get_xy()}",
            show_level="draw_position",
        )

        return self.coord.x_pos, self.coord.y_pos, self.radius, self.radius

    def draw(self, painter: Painter):
        """Draw circle"""
        painter.draw_circle(
            self.coord.x_pos,
            self.coord.y_pos,
            self.radius,
            outline_colour="black",
            fill_colour=self.fill_colour,
        )
        Helper.printc(
            f"        >>>> 2. Shape Text: {self.name}, {self.text_coord.get_xy()}",
            show_level="draw_position",
        )
        painter.draw_text(
            self.text_coord.x_pos,
            self.text_coord.y_pos,
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

    text_coord: Coordinate = field(init=True, default=Coordinate())
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.text_coord.x_pos = 0
        self.text_coord.y_pos = 0
        self.text_width: int = 0
        self.text_height: int = 0
        self.width = Configs.DIAMOND_WIDTH
        self.height = Configs.DIAMOND_HEIGHT

    def set_draw_position(self, painter: Painter) -> tuple:
        """Set draw position of diamond"""

        self.origin_coord.x_pos = self.coord.x_pos
        self.origin_coord.y_pos = self.coord.y_pos
        self.coord.x_pos = (
            self.coord.x_pos
            + int(Configs.BOX_WIDTH / 2)
            - int(Configs.DIAMOND_WIDTH / 2)
        )
        self.coord.y_pos = (
            self.coord.y_pos
            + int(Configs.BOX_HEIGHT / 2)
            - int(Configs.DIAMOND_HEIGHT / 2)
        )

        # -- Calculate the connections coordinate --
        self.top_middle.x_pos = self.coord.x_pos + int(self.width / 2)
        self.top_middle.y_pos = self.coord.y_pos

        self.right_middle.x_pos = self.coord.x_pos + self.width
        self.right_middle.y_pos = self.coord.y_pos + int(self.height / 2)

        self.bottom_middle.x_pos = self.coord.x_pos + int(self.width / 2)
        self.bottom_middle.y_pos = self.coord.y_pos + self.height

        self.left_middle.x_pos = self.coord.x_pos
        self.left_middle.y_pos = self.coord.y_pos + int(self.height / 2)

        self.text_width, self.text_height = painter.get_text_dimension(
            self.name, self.font, self.font_size
        )
        self.text_coord.x_pos = (
            self.coord.x_pos + (self.width / 2) - (self.text_width / 2)
        )
        self.text_coord.y_pos = self.coord.y_pos + self.height

        return self.coord.x_pos, self.coord.y_pos, self.width, self.height

    def draw(self, painter: Painter):
        """Draw diamond"""
        # Helper.printc(
        #     f"draw <{self.text}>, x: {self.coord.x_pos}, y: {self.coord.y_pos}, width: {self.width}, height: {self.height}"
        # )
        painter.draw_diamond(
            self.coord.x_pos,
            self.coord.y_pos,
            self.width,
            self.height,
            fill_colour=self.fill_colour,
        )
        painter.draw_text(
            self.text_coord.x_pos,
            self.text_coord.y_pos,
            self.name,
            self.font,
            self.font_size,
            font_colour=self.font_colour,
        )

        super().draw(painter)
