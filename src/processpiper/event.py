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
from .shape import Circle
from .painter import Painter


class Event(Circle):
    """Event class for representing events in a process."""

    ...


class Start(Event):
    """Start event class for representing start event in a process."""

    ...


class End(Event):
    """End event class for representing end event in a process."""

    def draw(self, painter: Painter):
        super().draw(painter)
        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 3, self.fill_colour)


class Timer(Event):
    """Timer event class for representing timer event in a process."""

    def draw_clock(self, painter: Painter):
        """Draw clock face"""
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
        """Draw timer event"""
        super().draw(painter)
        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 2, "grey")
        painter.draw_circle(self.x, self.y, self.radius - 4, "black")
        painter.draw_circle(self.x, self.y, self.radius - 6, "grey")
        ### draw clock
        self.draw_clock(painter)
        pos = 15
        painter.draw_line(
            self.x, self.y, self.x, self.y - pos + 3, "black", 1, 1, "solid"
        )
        painter.draw_line(
            self.x, self.y, self.x + pos - 3, self.y, "black", 1, 1, "solid"
        )


class Intermediate(Event):
    """Intermediate event class for representing intermediate event in a process."""

    def draw(self, painter: Painter):
        """Draw intermediate event"""
        super().draw(painter)
        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 3, "grey")
        painter.draw_circle(self.x, self.y, self.radius - 6, "black")
        painter.draw_circle(self.x, self.y, self.radius - 9, "grey")
