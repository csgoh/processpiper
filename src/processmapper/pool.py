from dataclasses import dataclass, field
from processmapper.painter import Painter
from processmapper.lane import Lane
import processmapper.constants as Configs
import processmapper.helper as Helper


@dataclass
class Pool:
    name: str = field(init=True)
    # font: str = field(init=True, default=None)
    # font_size: int = field(init=True, default=None)
    # font_colour: str = field(init=True, default=None)

    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    painter: Painter = field(init=False)
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
            self.painter.draw_box(
                self.x,
                self.y,
                self.width,
                self.height,
                "#d9d9d9",
            )
            ### Draw the lane text box
            self.painter.draw_box_with_vertical_text(
                self.x,
                self.y,
                Configs.POOL_TEXT_WIDTH,
                self.height,
                "#1F1F1F",
                self.name,
                text_alignment="centre",
                text_font="arial",
                text_font_size=12,
                text_font_colour="white",
            )

    def add_lane(self, lane_name: str) -> Lane:
        lane = Lane(lane_name, self.name)
        self._lanes.append(lane)
        return lane
