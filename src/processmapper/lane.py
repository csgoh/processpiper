from dataclasses import dataclass, field
from enum import Enum
from itertools import count
from processmapper.shape import Shape
from processmapper.event import Event, Start, End, Timer, Intermediate
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
    id: int = field(init=False, default_factory=count().__next__)
    shapes: list = field(init=False, default_factory=list)
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    text: str = field(init=True)
    pool_text: str = field(init=True, default="")
    painter: Painter = field(init=False)

    next_shape_x: int = field(init=False, default=0)
    next_shape_y: int = field(init=False, default=0)

    shape_row_count: int = field(init=False, default=0)

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
    LANE_SHAPE_TOP_MARGIN = 50
    LANE_SHAPE_BOTTOM_MARGIN = 50
    LANE_SHAPE_LEFT_MARGIN = 30
    LANE_SHAPE_RIGHT_MARGIN = 30

    HSPACE_BETWEEN_SHAPES = 50
    VSPACE_BETWEEN_SHAPES = 40

    VSPACE_BETWEEN_LANES = 5

    def add_element(
        self, text: str, type: EventType | ActivityType | GatewayType
    ) -> Shape:
        event_class = globals()[type]
        start = event_class(text, self.text)
        start.lane_id = self.id
        self.shapes.append(start)
        return start

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def get_current_x_position(self) -> int:
        if self.next_shape_x == 0:
            self.next_shape_x = (
                self.x + self.LANE_TEXT_WIDTH + self.LANE_SHAPE_LEFT_MARGIN
            )

        return self.next_shape_x

    def get_next_x_position(self) -> int:
        if self.next_shape_x == 0:
            self.next_shape_x = (
                self.x + self.LANE_TEXT_WIDTH + self.LANE_SHAPE_LEFT_MARGIN
            )
        else:
            self.next_shape_x += 100 + self.HSPACE_BETWEEN_SHAPES
        return self.next_shape_x

    def get_current_y_position(self) -> int:
        if self.next_shape_y == 0:
            self.next_shape_y = self.y + self.LANE_SHAPE_TOP_MARGIN

        return self.next_shape_y

    def get_next_y_position(self) -> int:
        if self.next_shape_y == 0:
            self.next_shape_y = self.y + 60 + self.LANE_SHAPE_TOP_MARGIN
        else:
            self.next_shape_y += 60 + self.VSPACE_BETWEEN_SHAPES
        return self.next_shape_y

    def draw(self) -> None:
        # print(f"draw lane {self.text}: {self.x}, {self.y}, {self.width}, {self.height}")
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
        self.painter.draw_grid()

    def draw_shape(self) -> None:
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.painter)

    def draw_connection(self) -> None:
        if self.shapes:
            for shape in self.shapes:
                shape.draw_connection(self.painter)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> None:
        print("Set draw position...")
        self.painter = painter
        ### Determine the x and y position of the lane
        self.x = x if x > 0 else self.SURFACE_LEFT_MARGIN
        self.y = y if y > 0 else self.SURFACE_TOP_MARGIN
        print(f"[{self.text}]: x={self.x}, y={self.y}")

        if self.shapes:
            self.next_shape_x = (
                self.x + self.LANE_TEXT_WIDTH + self.LANE_SHAPE_LEFT_MARGIN
            )

            ### Loop through all shapes within the lane (Method 1)
            # for shape in self.shapes:
            #     shape_x, shape_y, shape_w, shape_h = self.set_shape_draw_position(
            #         self.next_shape_x, self.y, shape, painter
            #     )
            #     self.width = max(self.width, shape_x + shape_w)
            #     self.height = max(
            #         self.height,
            #         shape_y + shape_h - self.y + self.LANE_SHAPE_BOTTOM_MARGIN,
            #     )
            #     self.next_shape_x = shape_x + shape_w + self.HSPACE_BETWEEN_SHAPES

            ### Start with the first shape (Method 2)
            shape_x, shape_y, shape_w, shape_h = self.set_shape_draw_position(
                self.next_shape_x, self.y, self.shapes[0], painter
            )

            self.width = max(self.width, shape_x + shape_w)
            self.height = max(
                self.height,
                shape_y + shape_h - self.y + self.LANE_SHAPE_BOTTOM_MARGIN,
            )

            self.next_shape_x = shape_x + shape_w + self.HSPACE_BETWEEN_SHAPES

        return self.x, self.y, self.width, self.height

    def set_shape_draw_position(
        self, x: int, y: int, shape: Shape, painter: Painter
    ) -> None:
        ### Set own shape position

        print(f"      <{shape.text}>: {x}, {(y + self.LANE_SHAPE_TOP_MARGIN)}")

        if shape.lane_name == self.text:
            shape_x, shape_y, shape_w, shape_h = shape.set_draw_position(
                x,
                (y + self.LANE_SHAPE_TOP_MARGIN),
                painter,
            )
            next_x = shape_x + shape_w + self.HSPACE_BETWEEN_SHAPES
            shape.draw_position_set = True

            shape.x_pos_traversed = True
            print(
                f"       <<{shape.text}>>: {shape.draw_position_set}, {shape.x_pos_traversed}"
            )

            ### Set next elements' position
            this_lane = self.text
            for index, next_shape in enumerate(shape.connection_to):
                print(
                    f"          {shape.text}({index}): next: {next_shape.text}, {next_x}, {y}, {next_shape.draw_position_set}, {shape.x_pos_traversed}"
                )

                ### Check whether thhe position has been set, if yes, skipped.
                ## or next_shape.lane_name != this_lane
                if next_shape.traversed == True:
                    print(f"            Skipped")
                    continue

                if index == 0:
                    next_shape_y = y
                else:
                    next_shape_y = (
                        y
                        + self.LANE_SHAPE_TOP_MARGIN
                        + self.HSPACE_BETWEEN_SHAPES
                        + shape_h
                    )

                (
                    next_shape_x,
                    next_shape_y,
                    next_shape_w,
                    next_shape_h,
                ) = self.set_shape_draw_position(
                    self.next_shape_x, next_shape_y, next_shape, painter
                )

                shape_x, shape_y, shape_w, shape_h = (
                    max(shape_x, next_shape_x),
                    max(shape_y, next_shape_y),
                    max(shape_w, next_shape_w),
                    max(shape_h, next_shape_h),
                )
                self.next_shape_x = next_shape_x
        else:
            shape_x, shape_y, shape_w, shape_h = 0, 0, 0, 0
            print(f"            Skipped")

        return shape_x, shape_y, shape_w, shape_h

    def get_outward_connection_count(self, shape: object) -> int:
        count = 0
        count += len(shape.connection_to)
        print(f"{shape.text}, get_reference_link_count: {count}")
        return count
