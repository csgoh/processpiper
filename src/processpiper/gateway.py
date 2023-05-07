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
from .shape import Diamond
from .painter import Painter

SYMBOL_SIZE = 23


class Gateway(Diamond):
    """A gateway is a diamond shape with a symbol in the middle"""

    def draw_symbol(self, symbol: str, painter: Painter):
        """Draw a symbol in the middle of the gateway"""
        symbol_w, symbol_h = painter.get_text_dimension(symbol, painter.element_font, SYMBOL_SIZE)
        painter.draw_text(
            self.x + (self.width / 2) - (symbol_w / 2),
            self.y + (self.height / 2) - (symbol_h / 2),
            symbol,
            painter.element_font,
            SYMBOL_SIZE,
            painter.element_font_colour,
        )


class Exclusive(Gateway):
    """An exclusive gateway is a diamond shape with a cross in the middle"""

    def draw(self, painter: Painter):
        """Draw the gateway and the symbol in the middle of the gateway"""
        super().draw(painter)
        ### Overlay a cross on top of the diamond
        symbol = "X"
        super().draw_symbol(symbol, painter)


class Parallel(Gateway):
    """A parallel gateway is a diamond shape with a plus in the middle"""

    def draw(self, painter: Painter):
        """Draw the gateway and the symbol in the middle of the gateway"""
        super().draw(painter)
        symbol = "+"
        super().draw_symbol(symbol, painter)


class Inclusive(Gateway):
    """An inclusive gateway is a diamond shape with a circle in the middle"""

    def draw(self, painter: Painter):
        """Draw the gateway and the symbol in the middle of the gateway"""
        super().draw(painter)
        symbol = "O"
        super().draw_symbol(symbol, painter)
