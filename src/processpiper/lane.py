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
from enum import Enum
from itertools import count
from .shape import Shape
from .painter import Painter
from .event import Event, Start, End, Timer, Intermediate
from .activity import Activity, Task, Subprocess
from .gateway import Gateway, Exclusive, Parallel, Inclusive
from .constants import Configs
from .helper import Helper


class EventType:
    """Event types"""

    START = "Start"
    END = "End"
    TIMER = "Timer"
    INTERMEDIATE = "Intermediate"


class ActivityType:
    """Activity types"""

    TASK = "Task"
    SUBPROCESS = "Subprocess"


class GatewayType:
    """Gateway types"""

    EXCLUSIVE = "Exclusive"
    PARALLEL = "Parallel"
    INCLUSIVE = "Inclusive"


class ElementType(str, Enum):
    """Element types"""

    START = "Start"
    END = "End"
    TIMER = "Timer"
    INTERMEDIATE = "Intermediate"
    TASK = "Task"
    SUBPROCESS = "Subprocess"
    EXCLUSIVE = "Exclusive"
    PARALLEL = "Parallel"
    INCLUSIVE = "Inclusive"


@dataclass
class Lane:
    """A lane is a container for elements in a process diagram."""

    name: str = field(init=True)
    pool_text: str = field(init=True, default="")
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)
    fill_colour: str = field(init=True, default=None)
    text_alignment: str = field(init=True, default=None)
    background_fill_colour: str = field(init=True, default=None)
    painter: Painter = field(init=True, default=None)

    id: int = field(init=False, default_factory=count().__next__)
    shapes: list = field(init=False, default_factory=list)
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    next_shape_x: int = field(init=False, default=0)
    next_shape_y: int = field(init=False, default=0)
    shape_row_count: int = field(init=False, default=0)
    text_x: int = field(init=False, default=0)
    text_y: int = field(init=False, default=0)
    text_width: int = field(init=False, default=0)
    text_height: int = field(init=False, default=0)

    def add_element(
        self,
        name: str,
        type: EventType | ActivityType | GatewayType,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        text_alignment: str = "",
    ) -> Shape:
        """Add an element to the lane"""
        if font == "":
            font = self.painter.element_font
        if font_size == 0:
            font_size = self.painter.element_font_size
        if font_colour == "":
            font_colour = self.painter.element_font_colour
        if fill_colour == "":
            fill_colour = self.painter.element_fill_colour
        if text_alignment == "":
            text_alignment = self.painter.element_text_alignment

        event_class = globals()[type]
        element = event_class(name, self.name)
        element.lane_id = self.id
        element.pool_name = self.pool_text
        element.font = font
        element.font_size = font_size
        element.font_colour = font_colour
        element.fill_colour = fill_colour
        element.text_alignment = text_alignment
        self.shapes.append(element)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def get_current_y_position(self) -> int:
        """Get the current y position of the lane"""
        if self.shape_row_count == 0:
            self.shape_row_count = 1
        if self.next_shape_y == 0:
            self.next_shape_y = self.y + Configs.LANE_SHAPE_TOP_MARGIN

        return self.next_shape_y

    def get_next_y_position(self) -> int:
        """Get the next y position of the lane"""
        if self.shape_row_count == 0:
            self.shape_row_count = 1

        if self.next_shape_y == 0:
            # self.next_shape_y = self.y + 60 + Configs.LANE_SHAPE_TOP_MARGIN
            self.next_shape_y = self.y + Configs.LANE_SHAPE_TOP_MARGIN
        else:
            self.next_shape_y += 60 + Configs.VSPACE_BETWEEN_SHAPES

        ### For every method call, increment the shape row count
        self.shape_row_count += 1
        return self.next_shape_y

    def draw(self) -> None:
        """Draw the lane"""

        ### Draw the lane outline
        self.painter.draw_box(
            self.x,
            self.y,
            self.width,
            self.height,
            self.background_fill_colour,
        )
        ### Draw the lane text box
        self.painter.draw_box_with_vertical_text(
            self.x,
            self.y,
            Configs.LANE_TEXT_WIDTH,
            self.height,
            self.fill_colour,
            self.name,
            text_alignment=self.text_alignment,
            text_font=self.font,
            text_font_size=self.font_size,
            text_font_colour=self.font_colour,
        )
        ### Draw the lane text divider
        self.painter.draw_line(
            self.x + Configs.LANE_TEXT_WIDTH,
            self.y,
            self.x + Configs.LANE_TEXT_WIDTH,
            self.y + self.height,
            "white",
            0.5,
            5,
            "solid",
        )
        ### Uncomment the following line to see the grid. Useful for debugging
        ####self.painter.draw_grid()

    def draw_shape(self) -> None:
        """Draw the shapes in the lane"""
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.painter)

    def draw_connection(self) -> None:
        """Draw the connections in the lane"""
        if self.shapes:
            for shape in self.shapes:
                shape.draw_connection(self.painter)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> None:
        """Set the draw position of the lane"""

        self.painter = painter

        ### Determine the x and y position of the lane
        ### If x and y are not specified, add the default margin
        self.x = x if x > 0 else Configs.SURFACE_LEFT_MARGIN + Configs.POOL_TEXT_WIDTH
        self.y = y if y > 0 else Configs.SURFACE_TOP_MARGIN

        if self.shapes:
            self.next_shape_x = (
                self.x
                + Configs.POOL_TEXT_WIDTH
                + Configs.LANE_TEXT_WIDTH
                + Configs.LANE_SHAPE_LEFT_MARGIN
            )

            shape_x, shape_y, shape_w, shape_h = self.set_shape_draw_position(
                self.next_shape_x, self.y, self.shapes[0], painter
            )

            self.width = max(self.width, shape_x + shape_w)
            self.height = max(
                self.height,
                shape_y + shape_h - self.y + Configs.LANE_SHAPE_BOTTOM_MARGIN,
            )

            self.next_shape_x = shape_x + shape_w + Configs.HSPACE_BETWEEN_SHAPES

        return self.x, self.y, self.width, self.height

    def set_shape_draw_position(
        self, x: int, y: int, shape: Shape, painter: Painter
    ) -> None:
        """Set the draw position of the shapes in the lane"""
        ### Set own shape position
        if shape.lane_name == self.name:
            shape_x, shape_y, shape_w, shape_h = shape.set_draw_position(
                x,
                (y + Configs.LANE_SHAPE_TOP_MARGIN),
                painter,
            )
            next_x = shape_x + shape_w + Configs.HSPACE_BETWEEN_SHAPES

            #### Mark for removal
            # shape.draw_position_set = True

            shape.x_pos_traversed = True

            ### Set next elements' position
            this_lane = self.name
            for index, next_shape in enumerate(shape.connection_to.target):

                ### Check whether the position has been set, if yes, skipped.
                ### This is needed to avoid infinite recursion
                if next_shape.traversed == True:
                    continue

                if index == 0:
                    next_shape_y = y
                else:
                    next_shape_y = (
                        y
                        + Configs.LANE_SHAPE_TOP_MARGIN
                        + Configs.HSPACE_BETWEEN_SHAPES
                        + shape_h
                    )

                ### Perform recursive call to set the position of the next element
                (
                    next_shape_x,
                    next_shape_y,
                    next_shape_w,
                    next_shape_h,
                ) = self.set_shape_draw_position(
                    self.next_shape_x, next_shape_y, next_shape, painter
                )

                shape_x, shape_y, shape_w, shape_h = (
                    max(shape_x, next_shape_x),
                    max(shape_y, next_shape_y),
                    max(shape_w, next_shape_w),
                    max(shape_h, next_shape_h),
                )
                self.next_shape_x = next_shape_x
        else:
            shape_x, shape_y, shape_w, shape_h = 0, 0, 0, 0

        return shape_x, shape_y, shape_w, shape_h
