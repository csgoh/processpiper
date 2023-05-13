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
        painter.draw_circle(self.x, self.y, self.radius - 2, self.fill_colour)
        painter.draw_circle(self.x, self.y, self.radius - 4, "black")
        painter.draw_circle(self.x, self.y, self.radius - 6, self.fill_colour)
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
        painter.draw_circle(self.x, self.y, self.radius - 2, self.fill_colour)
        painter.draw_circle(self.x, self.y, self.radius - 4, "black")
        painter.draw_circle(self.x, self.y, self.radius - 6, self.fill_colour)


class Message(Event):
    """Message event class for representing message event in a process."""

    def draw(self, painter: Painter):
        """Draw message event"""
        super().draw(painter)

        envelope_width = self.radius * 1.2
        envelope_height = self.radius * 0.9
        circle_center = (self.x, self.y)
        envelope_top_left = (
            circle_center[0] - envelope_width // 2,
            circle_center[1] - envelope_height // 2,
        )
        envelope_bottom_right = (
            circle_center[0] + envelope_width // 2,
            circle_center[1] + envelope_height // 2,
        )

        painter.draw_box_with_outline(
            envelope_top_left[0],
            envelope_top_left[1],
            envelope_width,
            envelope_height,
            box_outline_colour="black",
            box_outline_transparency=1,
            box_outline_width=2,
            box_fill_colour=painter.element_fill_colour,
        )

        painter.draw_line(
            ### +1 to x1, y1 is to offset the distortion caused by outline thickness
            envelope_top_left[0] + 1,
            envelope_top_left[1] + 1,
            circle_center[0],
            circle_center[1],
            "black",
            1,
            2,
            "solid",
        )
        painter.draw_line(
            ### adding -2 and +2 to x2, y2 is to offset the distortion caused by outline thickness
            envelope_top_left[0] + envelope_width - 2,
            envelope_top_left[1] + 2,
            circle_center[0],
            circle_center[1],
            "black",
            1,
            2,
            "solid",
        )


class Signal(Event):
    def draw(self, painter: Painter):
        """Draw message event"""
        super().draw(painter)
        # Draw a triangle
        triangle_radius = self.radius * 0.6
        vertices = [
            (self.x, self.y - triangle_radius),
            (
                self.x - triangle_radius * math.sin(math.pi / 3),
                self.y + triangle_radius * math.cos(math.pi / 3),
            ),
            (
                self.x + triangle_radius * math.sin(math.pi / 3),
                self.y + triangle_radius * math.cos(math.pi / 3),
            ),
        ]
        print(f"vertices {vertices}")
        painter.draw_polygon(
            vertices,
            outline_colour="black",
            fill_colour=painter.element_fill_colour,
            outline_width=2,
        )


class Conditional(Event):
    def draw(self, painter: Painter):
        """Draw message event"""
        super().draw(painter)

        # painter.draw_circle(self.x, self.y, self.radius, "black")
        # painter.draw_circle(self.x, self.y, self.radius - 3, self.fill_colour)

        rectangle_radius = self.radius
        rectangle_width = rectangle_radius * math.sqrt(0.8)
        rectangle_height = rectangle_radius * 0.9
        rectangle_vertices = [
            (self.x - rectangle_width / 2, self.y - rectangle_height / 2),
            (self.x + rectangle_width / 2, self.y + rectangle_height / 2),
        ]
        painter.draw_polygon(
            rectangle_vertices,
            outline_colour="red",
            fill_colour=painter.element_fill_colour,
            outline_width=2,
        )
        painter.draw_box_with_outline(
            self.x - rectangle_width / 2,
            self.y - rectangle_height / 2,
            rectangle_width,
            rectangle_height,
            box_fill_colour=painter.element_fill_colour,
            box_outline_colour="black",
            box_outline_transparency=1,
            box_outline_width=1,
        )

        num_lines = 5
        line_spacing = rectangle_height / (num_lines + 1)

        ### Draw the horizontal lines inside the rectangle
        for i in range(num_lines):
            line_y = self.y - rectangle_height / 2 + line_spacing * (i + 1)
            painter.draw_line(
                self.x - rectangle_width / 2 + 2,
                line_y,
                self.x + rectangle_width / 2 - 2,
                line_y,
                line_colour="black",
                line_width=1,
                line_style="solid",
                line_transparency=1,
            )


class Link(Event):
    def draw(self, painter: Painter):
        """Draw message event"""
        super().draw(painter)

        painter.draw_circle(self.x, self.y, self.radius, "black")
        painter.draw_circle(self.x, self.y, self.radius - 2, self.fill_colour)
        painter.draw_circle(self.x, self.y, self.radius - 4, "black")
        painter.draw_circle(self.x, self.y, self.radius - 6, self.fill_colour)

        arrow_radius = self.radius
        arrow_width = arrow_radius * 0.4
        arrow_height = arrow_radius * 0.6
        arrow_neck_width = 4

        # (self.x - arrow_width / 2, self.y - arrow_height / 2),  # Top point
        #     (self.x + arrow_width / 2, self.y),  # Middle point
        #     (self.x - arrow_width / 2, self.y + arrow_height / 2),  # Bottom point
        #     (self.x - arrow_width / 2, self.y + arrow_neck_width),
        #     (self.x - (arrow_width * 1.5), self.y + arrow_neck_width),
        #     (self.x - (arrow_width * 1.5), self.y - arrow_neck_width),
        #     (self.x - arrow_width / 2, self.y - arrow_neck_width),
        pointy_x = self.x + (arrow_width * 0.3)
        arrow_vertices = [
            (pointy_x, self.y - arrow_height / 1.5),  # Top point
            (self.x + (arrow_width * 1.4), self.y),  # Middle point
            (pointy_x, self.y + arrow_height / 1.5),  # Bottom point
            (pointy_x, self.y + arrow_neck_width),
            (self.x - (arrow_width * 1.2), self.y + arrow_neck_width),
            (self.x - (arrow_width * 1.2), self.y - arrow_neck_width),
            (pointy_x, self.y - arrow_neck_width),
        ]
        painter.draw_polygon(
            arrow_vertices,
            outline_colour="black",
            fill_colour=painter.element_fill_colour,
            outline_width=1,
        )
