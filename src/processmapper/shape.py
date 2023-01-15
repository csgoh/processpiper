from dataclasses import dataclass, field
from processmapper import Shape
from processmapper.painter import Painter


@dataclass
class Shape:
    x: int = field(init=False)
    y: int = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)
    points: dict = field(init=False)
    text: str = field(init=True)

    connection_from: list = field(init=False, default_factory=list)
    connection_to: list = field(init=False, default_factory=list)

    def connect(
        self,
        target: Shape,
        connection_type: str = "sequence",
    ) -> None:
        point_from, point_to = self.find_nearest_points(self.points, target.points)
        self.connection_to.append(point_to)
        target.connection_from.append(point_from)
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

    def draw(self) -> None:
        raise NotImplementedError


class Box(Shape):
    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        font_w, font_h = painter.get_text_dimensions(self.text)
        self.width = font_w + 20
        self.height = font_h + 10
        self.points = {
            "top_left": (self.x, self.y),
            "top_right": (self.x + self.width, self.y),
            "bottom_left": (self.x, self.y + self.height),
            "bottom_right": (self.x + self.width, self.y + self.height),
        }


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
        self.text_width, self.text_height = painter.get_text_dimensions(self.text)
        self.text_x = self.x - self.text_width / 2
        self.text_y = self.y - self.text_height / 2


class Triangle(Shape):
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
        self.text_width, self.text_height = painter.get_text_dimensions(self.text)
        self.text_x = self.x - self.text_width / 2
        self.text_y = self.y - self.text_height / 2
