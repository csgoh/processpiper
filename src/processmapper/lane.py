from dataclasses import dataclass, field
from enum import Enum
from processmapper.shape import Shape
from processmapper.event import Event, Start, End
from processmapper.activity import Activity, Task, Subprocess
from processmapper.gateway import Gateway, Exclusive, Parallel, Inclusive
from processmapper.painter import Painter


class EventType:
    START = "Start"
    END = "End"
    TIMER = "Timer"
    INTERMEDIATE = "Intermediate"


class ActivityType:
    TASK = "Task"
    SUBPROCESS = "Subprocess"


class GatewayType:
    EXCLUSIVE = "Exclusive"
    PARALLEL = "Parallel"
    INCLUSIVE = "Inclusive"


class ElementType(str, Enum):
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
    shapes: list = field(init=False, default_factory=list)
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    text: str = field(init=True)
    painter: Painter = field(init=False)

    text_x: int = field(init=False, default=0)
    text_y: int = field(init=False, default=0)
    text_width: int = field(init=False, default=0)
    text_height: int = field(init=False, default=0)

    SURFACE_TOP_MARGIN = 20
    SURFACE_BOTTOM_MARGIN = SURFACE_TOP_MARGIN
    SURFACE_LEFT_MARGIN = SURFACE_TOP_MARGIN
    SURFACE_RIGHT_MARGIN = SURFACE_TOP_MARGIN

    LANE_TEXT_WIDTH = 100
    LANE_TEXT_HEIGHT = 20
    LANE_SHAPE_TOP_MARGIN = 30
    LANE_SHAPE_BOTTOM_MARGIN = LANE_SHAPE_TOP_MARGIN
    LANE_SHAPE_LEFT_MARGIN = LANE_SHAPE_TOP_MARGIN
    LANE_SHAPE_RIGHT_MARGIN = LANE_SHAPE_TOP_MARGIN

    SPACE_BETWEEN_SHAPES = 40

    def add_element(
        self, text: str, type: EventType | ActivityType | GatewayType
    ) -> Shape:
        event_class = globals()[type]
        start = event_class(text)
        self.shapes.append(start)
        return start

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def draw(self) -> None:
        print(f"draw lane: {self.x}, {self.y}, {self.width}, {self.height}")
        ### Draw the lane outline
        self.painter.draw_box(
            self.x,
            self.y,
            self.width,
            self.height,
            "#d9d9d9",
        )
        ### Draw the lane text box
        self.painter.draw_box_with_text(
            self.x,
            self.y,
            self.LANE_TEXT_WIDTH,
            self.height,
            "#333333",
            self.text,
            text_alignment="left",
            text_font="arial",
            text_font_size=12,
            text_font_colour="white",
        )
        ### Draw the lane text divider
        self.painter.draw_line(
            self.x + self.LANE_TEXT_WIDTH,
            self.y,
            self.x + self.LANE_TEXT_WIDTH,
            self.y + self.height,
            "white",
            0.5,
            5,
            "solid",
        )
        # self.painter.draw_grid()
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.painter)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> None:
        self.painter = painter
        ### Determine the x and y position of the lane
        self.x = x if x > 0 else self.SURFACE_LEFT_MARGIN
        self.y = y if y > 0 else self.SURFACE_TOP_MARGIN

        if self.shapes:
            next_x = self.x + self.LANE_TEXT_WIDTH + self.LANE_SHAPE_LEFT_MARGIN

            ### Set first shape position. The first one is always 'Start' Event
            shape_x, shape_y, shape_w, shape_h = self.set_shape_draw_position(
                next_x, self.y, self.shapes[0], painter
            )

            self.width = max(self.width, shape_x + shape_w)
            self.height = max(self.height, shape_y + shape_h)

        # print(f"lane: {self.x}, {self.y}, {self.width}, {self.height}")
        return self.x, self.y, self.width, self.height

    def set_shape_draw_position(
        self, next_x: int, next_y: int, shape: Shape, painter: Painter
    ) -> None:
        ### Set own shape position

        print(
            f">>>Shape Begin: {shape.text}, {next_x}, {(next_y + self.LANE_SHAPE_TOP_MARGIN)}"
        )

        shape_x, shape_y, shape_w, shape_h = shape.set_draw_position(
            (next_x),
            (next_y + self.LANE_SHAPE_TOP_MARGIN),
            painter,
        )
        next_x = shape_x + shape_w + self.SPACE_BETWEEN_SHAPES

        ### Set next elements' position
        for index, next_shape in enumerate(shape.connection_to):
            print(
                f"index: {index}, next_shape: {next_shape.text}, next_shape_x: {next_x}"
            )

            ### Check whether thhe position has been set, if yes, skipped.
            if next_shape.x > 0:
                print(f"Skipped")
                continue

            if index == 0:
                next_shape_y = next_y
            else:
                next_shape_y = (
                    next_y
                    + self.LANE_SHAPE_TOP_MARGIN
                    + self.SPACE_BETWEEN_SHAPES
                    + shape_h
                )
                print(
                    f"next_shape_y: {next_shape_y}= {next_y} + {self.SPACE_BETWEEN_SHAPES} + {shape_h}"
                )

            next_shape_x = next_x

            (
                next_shape_x,
                next_shape_y,
                next_shape_w,
                next_shape_h,
            ) = self.set_shape_draw_position(
                next_shape_x, next_shape_y, next_shape, painter
            )
            shape_x, shape_y, shape_w, shape_h = (
                next_shape_x,
                next_shape_y,
                next_shape_w,
                next_shape_h,
            )

        print(f">>>Shape End: {shape.text}, {shape_x}, {shape_y}, {shape_w}, {shape_h}")
        return shape_x, shape_y, shape_w, shape_h

    def get_outward_connection_count(self, shape: object) -> int:
        count = 0
        count += len(shape.connection_to)
        print(f"{shape.text}, get_reference_link_count: {count}")
        return count
