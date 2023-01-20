from dataclasses import dataclass, field
from enum import Enum
from processmapper.shape import Shape
from processmapper.event import Event, Start, End
from processmapper.activity import Activity, Task, Subprocess
from processmapper.gateway import Gateway, Exclusive, Parallel, Inclusive
from processmapper.painter import Painter


# class EventType:
#     START = "Start"
#     END = "End"
#     TIMER = "Timer"
#     INTERMEDIATE = "Intermediate"


# class ActivityType:
#     TASK = "Task"
#     SUBPROCESS = "Subprocess"


# class GatewayType:
#     EXCLUSIVE = "Exclusive"
#     PARALLEL = "Parallel"
#     INCLUSIVE = "Inclusive"


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

    LANE_TEXT_WIDTH = 60
    LANE_TEXT_HEIGHT = 20
    LANE_SHAPE_TOP_MARGIN = 30
    LANE_SHAPE_BOTTOM_MARGIN = LANE_SHAPE_TOP_MARGIN
    LANE_SHAPE_LEFT_MARGIN = LANE_SHAPE_TOP_MARGIN
    LANE_SHAPE_RIGHT_MARGIN = LANE_SHAPE_TOP_MARGIN

    SPACE_BETWEEN_SHAPES = 40

    def add_element(self, text: str, type: ElementType) -> Shape:
        event_class = globals()[type]
        start = event_class(text)
        self.shapes.append(start)
        return start

    # def start(self, text: str, type: EventType) -> Event:
    #     event_class = globals()[type]
    #     start = event_class(text)
    #     self.shapes.append(start)
    #     return start

    # def activity(self, text: str, type: ActivityType) -> Activity:
    #     activity_class = globals()[type]
    #     activity = activity_class(text)
    #     self.shapes.append(activity)
    #     return activity

    # def gateway(self, text: str, type: GatewayType) -> Gateway:
    #     gateway_class = globals()[type]
    #     gateway = gateway_class(text)
    #     self.shapes.append(gateway)
    #     return gateway

    # def end(self, text: str, type: EventType) -> Event:
    #     event_class = globals()[type]
    #     end = event_class(text)
    #     self.shapes.append(end)
    #     return end

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def draw(self) -> None:
        print(f"draw lane: {self.x}, {self.y}, {self.width}, {self.height}")
        # self.painter.draw_box(self.x, self.y, self.width, self.height, "lightgrey")
        # self.painter.draw_text(
        #     self.x + 10, self.y + 10, self.text, "arial", 12, "black"
        # )
        self.painter.draw_box_with_text(
            self.x,
            self.y,
            self.width,
            self.height,
            "lightgrey",
            self.text,
            text_alignment="left",
            text_font="arial",
            text_font_size=12,
            text_font_colour="black",
        )
        self.painter.draw_grid()
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.painter)
                

    def set_draw_position(self, x: int, y: int, painter: Painter) -> None:
        self.painter = painter
        print(f"***[SETTINGS START]***")
        print(
            f"SURFACE MARGINS: {self.SURFACE_TOP_MARGIN}, {self.SURFACE_BOTTOM_MARGIN}, {self.SURFACE_LEFT_MARGIN}, {self.SURFACE_RIGHT_MARGIN}"
        )
        print(
            f"+LANE MARGINS: {self.SURFACE_TOP_MARGIN+self.LANE_SHAPE_TOP_MARGIN}, {self.SURFACE_BOTTOM_MARGIN+self.LANE_SHAPE_BOTTOM_MARGIN}, {self.SURFACE_LEFT_MARGIN+self.LANE_SHAPE_LEFT_MARGIN}, {self.SURFACE_RIGHT_MARGIN+self.LANE_SHAPE_RIGHT_MARGIN}"
        )
        print(f"LANE TEXT: {self.LANE_TEXT_WIDTH}, {self.LANE_TEXT_HEIGHT}")
        print(f"***[SETTINGS END]***")
        ### Determine the x and y position of the lane
        self.x = x if x > 0 else self.SURFACE_LEFT_MARGIN
        self.y = y if y > 0 else self.SURFACE_TOP_MARGIN

        if self.shapes:
            next_x = self.x + self.LANE_TEXT_WIDTH + self.LANE_SHAPE_LEFT_MARGIN
            print(
                f"next_x: {next_x} = {self.x} + {self.LANE_TEXT_WIDTH} + {self.LANE_SHAPE_LEFT_MARGIN}"
            )
            for i, shape in enumerate(self.shapes):
                shape_x, shape_y, shape_w, shape_h = shape.set_draw_position(
                    (next_x),
                    (self.y + self.LANE_SHAPE_TOP_MARGIN),
                    painter,
                )
                # print(f"shape: {x}, {y}, {w}, {h}")
                self.width = max(self.width, shape_x + shape_w)
                self.height = max(self.height, shape_y + shape_h)
                next_x = shape_x + shape_w + self.SPACE_BETWEEN_SHAPES
                print(
                    f"next_x: {next_x} = {shape_x} + {shape_w} + {self.SPACE_BETWEEN_SHAPES}"
                )

        print(f"lane: {self.x}, {self.y}, {self.width}, {self.height}")
        return self.x, self.y, self.width, self.height
