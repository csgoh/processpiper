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
from .painter import Painter
from .coordinate import Coordinate


@dataclass
class Footer:
    """Footer class for drawing footer"""

    name: str = field(init=True)
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)

    coord: Coordinate = field(init=True, default=Coordinate())
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    painter: Painter = field(init=False)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        """Set the position of the footer to be drawn"""
        self.coord.x_pos = x
        self.coord.y_pos = y
        self.painter = painter
        self.width, self.height = painter.get_text_dimension(
            self.name, self.font, self.font_size
        )
        return self.coord.x_pos, self.coord.y_pos, self.width, self.height

    def draw(self, painter: Painter = None):
        """Draw the footer"""
        if painter is None:
            painter = self.painter

        painter.draw_text(
            self.coord.x_pos,
            self.coord.y_pos,
            self.name,
            self.font,
            self.font_size,
            self.font_colour,
        )
