from dataclasses import dataclass, field
from processmapper.painter import Painter


@dataclass(kw_only=True)
class Title:
    name: str = field(init=True, default="<Process Map Title>")
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)

    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    painter: Painter = field(init=False)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        self.painter = painter
        self.width, self.height = painter.get_text_dimension(
            self.name, self.font, self.font_size
        )
        return self.x, self.y, self.width, self.height

    def draw(self, painter: Painter = None):
        if painter is None:
            painter = self.painter
        painter.draw_text(
            self.x, self.y, self.name, self.font, self.font_size, self.font_colour
        )
