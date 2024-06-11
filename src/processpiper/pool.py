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
from itertools import count
from .painter import Painter
from .lane import Lane
from .constants import Configs
from .coordinate import Coordinate
from .helper import Helper


@dataclass
class Pool:
    """A pool is a collection of lanes."""

    id: int = field(init=False, default_factory=count().__next__)
    name: str = field(init=True)
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)
    fill_colour: str = field(init=True, default=None)
    text_alignment: str = field(init=True, default=None)
    painter: Painter = field(init=True, default=None)

    bpmn_id: str = field(init=False)
    coord: Coordinate = field(init=False, default=None)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)

    next_shape_x: int = field(init=False, default=0)

    lanes: list = field(init=False, default_factory=list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None: ...

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        """Set the position of the pool and return the position of the next shape to be drawn"""
        self.coord = Coordinate()
        self.coord.x_pos = x
        self.coord.y_pos = y
        self.painter = painter
        last_lane_y = self.lanes[-1].coord.y_pos
        last_lane_height = self.lanes[-1].height

        self.width, self.height = (
            Configs.POOL_TEXT_WIDTH,
            last_lane_y + last_lane_height - self.coord.y_pos,
        )
        return self.coord.x_pos, self.coord.y_pos, self.width, self.height

    def draw(self):
        """Draw the pool and the lanes in the pool"""
        if self.name != "Default Pool":
            # --Draw the pool text box--
            self.painter.draw_box_with_vertical_text(
                self.coord.x_pos,
                self.coord.y_pos,
                Configs.POOL_TEXT_WIDTH,
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

    def add_lane(
        self,
        lane_name: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        text_alignment: str = "",
        background_fill_colour: str = "",
    ) -> Lane:
        """Add a lane to the pool

        Args:
            lane_name (str): name of the lane
            font (str, optional): lane text font. Defaults to "".
            font_size (int, optional): lane text font size. Defaults to 0.
            font_colour (str, optional): lane text font colour. Defaults to "".
            fill_colour (str, optional): lane fill colour. Defaults to "".
            text_alignment (str, optional): _lane text alignement. Defaults to "".
            background_fill_colour (str, optional): land background fill colour. Defaults to "".

        Returns:
            Lane: Lane object
        """

        font = font or self.painter.lane_font
        font_size = font_size or self.painter.lane_font_size
        font_colour = font_colour or self.painter.lane_font_colour
        fill_colour = fill_colour or self.painter.lane_fill_colour
        text_alignment = text_alignment or self.painter.lane_text_alignment
        background_fill_colour = (
            background_fill_colour or self.painter.lane_background_fill_colour
        )

        lane = Lane(
            lane_name,
            self.name,
            font,
            font_size,
            font_colour,
            fill_colour,
            text_alignment,
            background_fill_colour,
            self.painter,
        )
        lane.bpmn_id = Helper.get_uuid()
        self.lanes.append(lane)
        return lane
