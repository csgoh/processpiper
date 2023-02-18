import math
from processmapper.shape import Circle
from processmapper.painter import Painter


class Event(Circle):
    ...


class Start(Event):
    ...


class End(Event):
    def draw(self, painter: Painter):
        super().draw(painter)
        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 3, "grey")


class Timer(Event):
    def draw_clock(self, painter: Painter):
        margin = 8
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(0)),
            self.y + (self.radius - margin) * math.sin(math.radians(0)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(45)),
            self.y + (self.radius - margin) * math.sin(math.radians(45)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(90)),
            self.y + (self.radius - margin) * math.sin(math.radians(90)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(135)),
            self.y + (self.radius - margin) * math.sin(math.radians(135)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(180)),
            self.y + (self.radius - margin) * math.sin(math.radians(180)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(225)),
            self.y + (self.radius - margin) * math.sin(math.radians(225)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(270)),
            self.y + (self.radius - margin) * math.sin(math.radians(270)),
            1,
            "black",
        )
        painter.draw_circle(
            self.x + (self.radius - margin) * math.cos(math.radians(315)),
            self.y + (self.radius - margin) * math.sin(math.radians(315)),
            1,
            "black",
        )

    def draw(self, painter: Painter):
        super().draw(painter)
        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 2, "grey")
        painter.draw_circle(self.x, self.y, self.radius - 4, "black")
        painter.draw_circle(self.x, self.y, self.radius - 6, "grey")
        # draw clock
        self.draw_clock(painter)
        pos = 15
        painter.draw_line(
            self.x, self.y, self.x, self.y - pos + 3, "black", 1, 1, "solid"
        )
        painter.draw_line(
            self.x, self.y, self.x + pos - 3, self.y, "black", 1, 1, "solid"
        )


class Intermediate(Event):
    def draw(self, painter: Painter):
        super().draw(painter)
        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 3, "grey")
        painter.draw_circle(self.x, self.y, self.radius - 6, "black")
        painter.draw_circle(self.x, self.y, self.radius - 9, "grey")
