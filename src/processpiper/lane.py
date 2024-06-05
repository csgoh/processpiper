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
import uuid
from .shape import Shape
from .painter import Painter
from .constants import Configs
from .event import *
from .activity import *
from .gateway import *
from .helper import Helper
from .layout import Grid
from .coordinate import Coordinate


class EventType:
    """Event types"""

    START = "Start"
    END = "End"
    TIMER = "Timer"
    INTERMEDIATE = "Intermediate"
    MESSAGE = "Message"
    MESSAGE_INTERMEDIATE = "MessageIntermediate"
    MESSAGE_END = "MessageEnd"
    SIGNAL = "Signal"
    SIGNAL_INTERMEDIATE = "SignalIntermediate"
    SIGNAL_END = "SignalEnd"
    CONDITIONAL = "Conditional"
    CONDITIONAL_INTERMEDIATE = "ConditionalIntermediate"
    LINK = "Link"


class ActivityType:
    """Activity types"""

    TASK = "Task"
    SUBPROCESS = "Subprocess"


class GatewayType:
    """Gateway types"""

    EXCLUSIVE = "Exclusive"
    PARALLEL = "Parallel"
    INCLUSIVE = "Inclusive"
    EVENT = "EventGateway"


class ElementType(str, Enum):
    """Element types"""

    START = "Start"
    END = "End"
    TIMER = "Timer"
    INTERMEDIATE = "Intermediate"
    MESSAGE = "Message"
    MESSAGE_INTERMEDIATE = "MessageIntermediate"
    MESSAGE_END = "MessageEnd"
    SIGNAL = "Signal"
    SIGNAL_INTERMEDIATE = "SignalIntermediate"
    SIGNAL_END = "SignalEnd"
    CONDITIONAL = "Conditional"
    CONDITIONAL_INTERMEDIATE = "ConditionalIntermediate"
    LINK = "Link"
    TASK = "Task"
    SUBPROCESS = "Subprocess"
    EXCLUSIVE = "Exclusive"
    PARALLEL = "Parallel"
    INCLUSIVE = "Inclusive"
    EVENT = "Event"


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
    bpmn_id: str = field(init=False)
    shapes: list = field(init=False, default_factory=list)
    coord: Coordinate = field(init=False, default=None)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    next_shape_coord: Coordinate = field(init=False, default=None)
    shape_row_count: int = field(init=False, default=0)
    text_coord: Coordinate = field(init=False, default=None)
    text_width: int = field(init=False, default=0)
    text_height: int = field(init=False, default=0)

    def __post_init__(self):
        self.coord = Coordinate()
        self.next_shape_coord = Coordinate()
        self.text_coord = Coordinate()

    def add_element(
        self,
        name: str,
        type: EventType | ActivityType | GatewayType,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        outline_colour: str = "",
        outline_width: int = 0,
        text_alignment: str = "",
    ) -> Shape:
        font = font or self.painter.element_font
        font_size = font_size or self.painter.element_font_size
        font_colour = font_colour or self.painter.element_font_colour
        fill_colour = fill_colour or self.painter.element_fill_colour
        outline_colour = outline_colour or self.painter.element_outline_colour
        outline_width = outline_width or self.painter.element_outline_width
        text_alignment = text_alignment or self.painter.element_text_alignment

        event_class = globals()[type]
        element = event_class(name, self.name)
        element.lane_id = self.id
        element.pool_name = self.pool_text
        element.font = font
        element.font_size = font_size
        element.font_colour = font_colour
        element.fill_colour = fill_colour
        element.outline_colour = outline_colour
        element.outline_width = outline_width
        element.text_alignment = text_alignment
        element.bpmn_id = Helper.get_uuid()
        self.shapes.append(element)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def draw(self) -> None:
        """Draw the lane"""

        # --Draw the lane outline
        self.painter.draw_box(
            self.coord.x_pos,
            self.coord.y_pos,
            self.width,
            self.height,
            self.background_fill_colour,
        )
        #  --Draw the lane text box
        self.painter.draw_box_with_vertical_text(
            self.coord.x_pos,
            self.coord.y_pos,
            Configs.LANE_TEXT_WIDTH,
            self.height,
            self.fill_colour,
            "",
            0,
            self.name,
            text_alignment=self.text_alignment,
            text_font=self.font,
            text_font_size=self.font_size,
            text_font_colour=self.font_colour,
        )
        #  --Draw the lane text divider
        self.painter.draw_line(
            self.coord.x_pos + Configs.LANE_TEXT_WIDTH,
            self.coord.y_pos,
            self.coord.x_pos + Configs.LANE_TEXT_WIDTH,
            self.coord.y_pos + self.height,
            "white",
            0.5,
            5,
            "solid",
        )
        #  --Uncomment the following line to see the grid. Useful for debugging
        # self.painter.draw_grid()

    def draw_shape(self) -> None:
        """Draw the shapes in the lane"""
        if self.shapes:
            for shape in self.shapes:
                Helper.printc(
                    f"      Drawing shape: [bold][red][{shape.name}][/red][/bold], x={shape.coord.get_xy()}, w={shape.width}, h={shape.height}",
                    rich_type="text",
                    show_level="draw",
                )

                shape.draw(self.painter)

    def draw_connection(self, all_shapes: list) -> None:
        """Draw the connections in the lane"""

        Helper.printc(
            f"Lane: {self.name}", show_level="draw_connection", rich_type="panel"
        )
        if self.shapes:
            shape = self.shapes[0]
            shape.draw_connection(self.painter, all_shapes)

    def set_draw_position(
        self, x: int, y: int, layout_grid: Grid
    ) -> tuple[int, int, int, int]:
        """Set the draw position of the lane"""

        # --Determine the number of rows for the lane
        lane_row_count = layout_grid.get_lane_row_count(self.id)

        #  --Determine lane x and y position
        self.coord.x_pos = (
            x
            if x > 0
            else Configs.SURFACE_LEFT_MARGIN
            + Configs.POOL_TEXT_WIDTH
            + Configs.HSPACE_BETWEEN_POOL_AND_LANE
        )
        self.coord.y_pos = y if y > 0 else Configs.SURFACE_TOP_MARGIN

        #  --Determine lane width
        max_column_count = layout_grid.get_max_column_count()
        Helper.printc(
            f"~~~ max column count: {max_column_count}", show_level="pool_lane"
        )
        self.width = (
            (Configs.HSPACE_BETWEEN_SHAPES * max_column_count - 1)
            + (Configs.BOX_WIDTH * max_column_count)
            + (Configs.LANE_SHAPE_LEFT_MARGIN)
        )

        Helper.printc(
            f"~~~ Lane: [{self.name}] shape row count: {lane_row_count}",
            35,
            show_level="pool_lane",
        )

        # --Determine lane height
        self.height = (
            (lane_row_count * 60)
            + ((lane_row_count - 1) * Configs.VSPACE_BETWEEN_SHAPES)
            + Configs.LANE_SHAPE_TOP_MARGIN
            + Configs.LANE_SHAPE_BOTTOM_MARGIN
        )
        Helper.printc(
            f"~~~    [{self.name}] {self.coord.x_pos=}, {self.coord.y_pos=}, {self.width=}, {self.height=}",
            show_level="pool_lane",
        )
        y_pos = self.coord.y_pos + self.height + Configs.VSPACE_BETWEEN_LANES

        return self.coord.x_pos, y_pos, self.width, self.height
