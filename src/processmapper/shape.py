from dataclasses import dataclass, field
from processmapper.painter import Painter
from typing import TypeVar

TShape = TypeVar("TShape", bound="Shape")


@dataclass
class Shape:
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    points: dict = field(init=False, default_factory=dict)
    text: str = field(init=True, default="")

    connection_from: list = field(init=False, default_factory=list)
    connection_to: list = field(init=False, default_factory=list)

    def connect(
        self: TShape,
        target: TShape,
        connection_type: str = "sequence",
    ) -> None:
        # point_from, point_to = self.find_nearest_points(self.points, target.points)
        self.connection_to.append(target)
        target.connection_from.append(self)
        return target

    def find_nearest_points(self, points_source, points_target):
        smallest_x = 9999
        smallest_y = 9999
        score = 9999
        nearest_points = {}
        index = 0
        for source_name, source_points in points_source.items():
            for target_name, target_points in points_target.items():
                source_x = source_points[0]
                source_y = source_points[1]
                target_x = target_points[0]
                target_y = target_points[1]
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
        if len(nearest_points) == 3:
            for index, points in nearest_points.items():
                source_name = points["source_name"]
                target_name = points["target_name"]
                if "middle" in source_name:
                    source_points = points["source_points"]
                if "middle" in target_name:
                    target_points = points["target_points"]
            return source_points, target_points

    # def draw(self) -> None:
    #     raise NotImplementedError


class Box(Shape):
    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        font_w, font_h = painter.get_text_dimension(self.text, "arial.ttf", 12)
        self.width = font_w + 20
        self.height = font_h + 10
        self.points = {
            "top_left": (self.x, self.y),
            "top_right": (self.x + self.width, self.y),
            "bottom_left": (self.x, self.y + self.height),
            "bottom_right": (self.x + self.width, self.y + self.height),
        }
        print(
            f"({self.__class__.__name__}) self.x: {self.x}, self.y: {self.y}, self.width: {self.width}, self.height: {self.height}"
        )
        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter):
        painter.draw_box(self.x, self.y, self.width, self.height, "gray")
        painter.draw_text(self.x, self.y, self.text, "arial.ttf", 12, "black")


class Circle(Shape):
    RADIUS = 20
    text_x: int = field(init=False)
    text_y: int = field(init=False)
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        self.radius = self.RADIUS
        self.points = {
            "top_left": (self.x - self.radius, self.y - self.radius),
            "top_right": (self.x + self.radius, self.y - self.radius),
            "bottom_left": (self.x - self.radius, self.y + self.radius),
            "bottom_right": (self.x + self.radius, self.y + self.radius),
        }
        self.text_width, self.text_height = painter.get_text_dimension(
            self.text, "arial.ttf", 12
        )
        self.text_x = self.x - self.text_width / 2
        self.text_y = self.y - self.text_height / 2

        print(
            f"({self.__class__.__name__}) self.x: {self.x}, self.y: {self.y}, self.radius: {self.radius}"
        )
        return self.x, self.y, self.radius, self.radius

    def draw(self, painter: Painter):
        painter.draw_circle(self.x, self.y, self.radius, "blue")
        painter.draw_text(self.text_x, self.text_y, self.text, "arial.ttf", 12, "blue")


class Diamond(Shape):
    text_x: int = field(init=False)
    text_y: int = field(init=False)
    text_width: int = field(init=False)
    text_height: int = field(init=False)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        self.points = [
            (self.x + self.width / 2, self.y),
            (self.x + self.width, self.y + self.height / 2),
            (self.x + self.width / 2, self.y + self.height),
            (self.x, self.y + self.height / 2),
        ]
        self.text_width, self.text_height = painter.get_text_dimension(
            self.text, "arial.ttf", 12
        )
        self.text_x = self.x - self.text_width / 2
        self.text_y = self.y - self.text_height / 2

        print(
            f"({self.__class__.__name__}) self.x: {self.x}, self.y: {self.y}, self.width: {self.width}, self.height: {self.height}"
        )
        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter):
        painter.draw_diamond(self.x, self.y, self.width, self.height)
        painter.draw_text(self.text_x, self.text_y, self.text, "arial.ttf", 12)
