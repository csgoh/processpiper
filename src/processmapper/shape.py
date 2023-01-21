from dataclasses import dataclass, field
import math
from processmapper.painter import Painter
from typing import TypeVar

TShape = TypeVar("TShape", bound="Shape")

BOX_WIDTH = 100
BOX_HEIGHT = 60
CIRCLE_RADIUS = 20
DIAMOND_WIDTH = 40
DIAMOND_HEIGHT = DIAMOND_WIDTH


@dataclass
class Shape:
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    points: dict = field(init=False, default_factory=dict)
    incoming_points: list = field(init=False, default_factory=list)
    outgoing_points: list = field(init=False, default_factory=list)
    text: str = field(init=True, default="")

    connection_from: list = field(init=False, default_factory=list)
    connection_to: list = field(init=False, default_factory=list)

    def connect(
        self: TShape,
        target: TShape,
        connection_type: str = "sequence",
    ) -> TShape:

        self.connection_to.append(target)
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
        shortest_distance: int = 9_999_999
        for source_name, source_points in points_source.items():
            for target_name, target_points in points_target.items():
                distance = self.get_distance(source_points, target_points)
                if (
                    distance
                    < shortest_distance
                    # and source_points not in self.incoming_points
                ):
                    shortest_distance = distance
                    nearest_points = {
                        "source_name": source_name,
                        "source_points": source_points,
                        "target_name": target_name,
                        "target_points": target_points,
                        "distance": distance,
                    }

        return (
            nearest_points["source_points"],
            nearest_points["target_points"],
        )

    def find_nearest_points_X(self, points_source, points_target):
        smallest_x = 9999
        smallest_y = 9999
        index = 0
        score = 9999
        nearest_points = {}
        source_points = []
        target_points = []
        for source_name, source_points in points_source.items():
            for target_name, target_points in points_target.items():
                source_x, source_y = source_points
                target_x, target_y = target_points
                if (abs(target_x - source_x)) < smallest_x or (
                    abs(target_y - source_y)
                ) <= smallest_y:
                    smallest_x = abs(target_x - source_x)
                    smallest_y = abs(target_y - source_y)

                    if score > smallest_x + smallest_y:
                        index = 0
                        nearest_points = {}
                        nearest_points[index] = {
                            "source_name": source_name,
                            "source_points": (source_x, source_y),
                            "target_name": target_name,
                            "target_points": (target_x, target_y),
                            "score": score,
                        }
                        score = smallest_x + smallest_y
                    elif score == smallest_x + smallest_y:
                        index += 1

                        nearest_points[index] = {
                            "source_name": source_name,
                            "source_points": (source_x, source_y),
                            "target_name": target_name,
                            "target_points": (target_x, target_y),
                            "score": score,
                        }
        # find source_name contain "middle" and target_name contain "middle" in nearest_points
        if len(nearest_points) <= 2:
            return (
                nearest_points[0]["source_points"],
                nearest_points[0]["target_points"],
            )
        if len(nearest_points) >= 3:
            for index, points in nearest_points.items():
                source_name = points["source_name"]
                target_name = points["target_name"]
                if "middle" in source_name:
                    source_points = points["source_points"]
                if "middle" in target_name:
                    target_points = points["target_points"]
            return source_points, target_points

    def draw(self, painter: Painter):

        # draw connection
        source_points = self.points
        if self.connection_to:
            for connection in self.connection_to:
                ### remove points from source_points is it exist in incoming_points
                for point_name, point in source_points.items():
                    if point in self.incoming_points:
                        del source_points[point_name]
                        break

                target_points = connection.points
                ### remove points from target_points is it exist in outgoing_points
                for point_name, point in target_points.items():
                    if point in connection.outgoing_points:
                        del target_points[point_name]
                        break

                point_from, point_to = self.find_nearest_points(
                    source_points, target_points
                )
                self.outgoing_points.append(point_from)
                connection.incoming_points.append(point_to)
                painter.draw_arrow(
                    point_from[0], point_from[1], point_to[0], point_to[1]
                )

        # painter.draw_line(
        #     self.x, self.y, self.x + self.width, self.y, "black", 0.5, 1, "solid"
        # )


class Box(Shape):
    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        self.width = BOX_WIDTH
        self.height = BOX_HEIGHT
        self.points = {
            # "top_left": (self.x, self.y),
            # "top_right": (self.x + self.width, self.y),
            # "bottom_left": (self.x, self.y + self.height),
            # "bottom_right": (self.x + self.width, self.y + self.height),
            "middle_left": (self.x, self.y + self.height / 2),
            "middle_top": (self.x + self.width / 2, self.y),
            "middle_right": (self.x + self.width, self.y + self.height / 2),
            "middle_bottom": (self.x + self.width / 2, self.y + self.height),
        }
        # print(
        #     f"({self.__class__.__name__}) self.x: {self.x}, self.y: {self.y}, self.width: {self.width}, self.height: {self.height}"
        # )
        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter):
        # print(f"draw [{self.text}], {self.x}, {self.y}, {self.width}, {self.height}")
        painter.draw_box_with_text(
            self.x,
            self.y,
            self.width,
            self.height,
            "darkgray",
            self.text,
            text_alignment="centre",
            text_font="arial.ttf",
            text_font_size=12,
            text_font_colour="black",
        )
        super().draw(painter)


class Circle(Shape):
    text_x: int = field(init=False)
    text_y: int = field(init=False)
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        # Circle x position starts from the circle centre, so add radius to x.
        # But we want to cater for cases when circle and box aligned vertically.
        self.x = int(x + CIRCLE_RADIUS + (BOX_WIDTH / 2) - (CIRCLE_RADIUS))
        self.y = int(y + (BOX_HEIGHT / 2))
        self.radius = CIRCLE_RADIUS
        self.points = {
            "0": (
                self.x + self.radius * math.cos(math.radians(0)),
                self.y + self.radius * math.sin(math.radians(0)),
            ),
            "90": (
                self.x + self.radius * math.cos(math.radians(90)),
                self.y + self.radius * math.sin(math.radians(90)),
            ),
            "180": (
                self.x + self.radius * math.cos(math.radians(180)),
                self.y + self.radius * math.sin(math.radians(180)),
            ),
            "270": (
                self.x + self.radius * math.cos(math.radians(270)),
                self.y + self.radius * math.sin(math.radians(270)),
            ),
        }
        self.text_width, self.text_height = painter.get_text_dimension(
            self.text, "arial.ttf", 10
        )
        self.text_x = self.x + (self.width / 2) - (self.text_width / 2)
        self.text_y = self.y + self.radius

        # print(
        #     f"({self.__class__.__name__}) self.x: {self.x}, self.y: {self.y}, self.radius: {self.radius}"
        # )
        return self.x, self.y, self.radius, self.radius

    def draw(self, painter: Painter):
        # print(f"draw ({self.text}), x: {self.x}, y: {self.y}, radius: {self.radius}")
        painter.draw_circle(self.x, self.y, self.radius, "darkgray")
        painter.draw_text(self.text_x, self.text_y, self.text, "arial.ttf", 10, "black")
        super().draw(painter)


class Diamond(Shape):
    text_x: int = field(init=False)
    text_y: int = field(init=False)
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x + (BOX_WIDTH / 2) - (DIAMOND_WIDTH / 2)
        self.y = y + (BOX_HEIGHT / 2) - (DIAMOND_HEIGHT / 2)
        self.width = DIAMOND_WIDTH
        self.height = DIAMOND_HEIGHT
        self.points = {
            "middle_top": (self.x + self.width / 2, self.y),
            "middle_right": (self.x + self.width, self.y + self.height / 2),
            "middle_bottom": (self.x + self.width / 2, self.y + self.height),
            "middle_left": (self.x, self.y + self.height / 2),
        }
        self.text_width, self.text_height = painter.get_text_dimension(
            self.text, "arial.ttf", 10
        )
        self.text_x = self.x + (self.width / 2) - (self.text_width / 2)
        self.text_y = self.y + self.height

        # print(
        #     f"({self.__class__.__name__}) self.x: {self.x}, self.y: {self.y}, self.width: {self.width}, self.height: {self.height}"
        # )
        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter):
        # print(
        #     f"draw <{self.text}>, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}"
        # )
        painter.draw_diamond(
            self.x, self.y, self.width, self.height, fill_colour="grey"
        )
        painter.draw_text(
            self.text_x, self.text_y, self.text, "arial.ttf", 10, font_colour="black"
        )

        super().draw(painter)
