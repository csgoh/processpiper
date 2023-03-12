from dataclasses import dataclass, field
from processmapper.painter import Painter
from processmapper.lane import Lane
import processmapper.constants as Configs
import processmapper.helper as Helper


@dataclass
class Pool:
    name: str = field(init=True)
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)
    fill_colour: str = field(init=True, default=None)
    text_alignment: str = field(init=True, default=None)
    painter: Painter = field(init=True, default=None)

    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)

    next_shape_x: int = field(init=False, default=0)

    _lanes: list = field(init=False, default_factory=list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...

    def get_current_x_position(self) -> int:
        if self.next_shape_x == 0:
            self.next_shape_x = (
                self.x
                + Configs.POOL_TEXT_WIDTH
                + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                + Configs.LANE_TEXT_WIDTH
                + Configs.LANE_SHAPE_LEFT_MARGIN
            )

        return self.next_shape_x

    def get_next_x_position(self) -> int:
        if self.next_shape_x == 0:
            self.next_shape_x = (
                self.x
                + Configs.POOL_TEXT_WIDTH
                + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                + Configs.LANE_TEXT_WIDTH
                + Configs.LANE_SHAPE_LEFT_MARGIN
            )
        else:
            self.next_shape_x += 100 + Configs.HSPACE_BETWEEN_SHAPES
        return self.next_shape_x

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        self.painter = painter
        last_lane_y = self._lanes[-1].y
        last_lane_height = self._lanes[-1].height

        self.width, self.height = (
            Configs.POOL_TEXT_WIDTH,
            last_lane_y + last_lane_height - self.y,
        )
        # print(
        #     f"({self.name}) x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}"
        # )
        return self.x, self.y, self.width, self.height

    def draw(self):
        if self.name != "Default Pool":
            Helper.printc(f"Drawing pool: {self.name}", "34")
            # self.painter.draw_box(
            #     self.x,
            #     self.y,
            #     self.width,
            #     self.height,
            #     self.fill_colour,
            # )
            print(
                f"Drawing pool: {self.name}, {self.font}, {self.font_size}, {self.font_colour}, {self.fill_colour}, {self.text_alignment}"
            )
            ### Draw the pool text box
            self.painter.draw_box_with_vertical_text(
                self.x,
                self.y,
                Configs.POOL_TEXT_WIDTH,
                self.height,
                # "#1F1F1F",
                self.fill_colour,
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

        if font == "":
            font = self.painter.lane_font
        if font_size == 0:
            font_size = self.painter.lane_font_size
        if font_colour == "":
            font_colour = self.painter.lane_font_colour
        if fill_colour == "":
            fill_colour = self.painter.lane_fill_colour
        if text_alignment == "":
            text_alignment = self.painter.lane_text_alignment
        if background_fill_colour == "":
            background_fill_colour = self.painter.lane_background_fill_colour

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
        self._lanes.append(lane)
        return lane
