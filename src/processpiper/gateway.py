from processpiper.shape import Diamond
from processpiper.painter import Painter

SYMBOL_SIZE = 23


class Gateway(Diamond):
    def draw_symbol(self, symbol: str, painter: Painter):
        symbol_w, symbol_h = painter.get_text_dimension(
            symbol, "arial.ttf", SYMBOL_SIZE
        )
        painter.draw_text(
            self.x + (self.width / 2) - (symbol_w / 2),
            self.y + (self.height / 2) - (symbol_h / 2),
            symbol,
            "arial.ttf",
            SYMBOL_SIZE,
            "black",
        )


class Exclusive(Gateway):
    def draw(self, painter: Painter):
        super().draw(painter)
        ### Overlay a cross on top of the diamond
        symbol = "X"
        super().draw_symbol(symbol, painter)


class Parallel(Gateway):
    def draw(self, painter: Painter):
        super().draw(painter)
        symbol = "+"
        super().draw_symbol(symbol, painter)


class Inclusive(Gateway):
    def draw(self, painter: Painter):
        super().draw(painter)
        symbol = "O"
        super().draw_symbol(symbol, painter)
