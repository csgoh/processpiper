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
    ...


class Intermediate(Event):
    ...
