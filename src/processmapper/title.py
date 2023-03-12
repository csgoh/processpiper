from dataclasses import dataclass, field
from processmapper.painter import Painter


@dataclass
class Title:
    name: str = field(init=True, default="<Process Map Title>")
    font: str = field(init=True, default="arial.ttf")
    font_size: int = field(init=True, default=28)
    font_colour: str = field(init=True, default="black")

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

    def draw(self):
        print(
            f"{self.name} x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, font: {self.font}, font_size: {self.font_size}, font_colour: {self.font_colour}"
        )
        self.painter.draw_text(
            self.x, self.y, self.name, self.font, self.font_size, self.font_colour
        )
