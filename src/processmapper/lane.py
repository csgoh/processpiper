from dataclasses import dataclass, field
from processmapper.event import Event, Start, End
from processmapper.activity import Activity, Task, Subprocess
from processmapper.gateway import Gateway, Exclusive, Parallel, Inclusive
from processmapper.painter import Painter
from enum import Enum


class EventType(str, Enum):
    START = "Start"
    END = "End"
    TIMER = "Timer"
    INTERMEDIATE = "Intermediate"


class ActivityType(str, Enum):
    TASK = "Task"
    SUBPROCESS = "Subprocess"


class GatewayType(str, Enum):
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
    SURFACE_BOTTOM_MARGIN = 20
    SURFACE_LEFT_MARGIN = 20
    SURFACE_RIGHT_MARGIN = 20

    LANE_TEXT_SPACE = 40
    LANE_SHAPE_TOP_MARGIN = 20
    LANE_SHAPE_BOTTOM_MARGIN = 20
    LANE_SHAPE_LEFT_MARGIN = 20
    LANE_SHAPE_RIGHT_MARGIN = 20

    def start(self, text: str, type: EventType) -> Event:
        # start = Start(text)
        event_class = globals()[type]
        start = event_class(text)
        self.shapes.append(start)
        return start

    def activity(self, text: str, type: ActivityType) -> Activity:
        activity_class = globals()[type]
        activity = activity_class(text)
        self.shapes.append(activity)
        return activity

    def gateway(self, text: str, type: GatewayType) -> Gateway:
        gateway_class = globals()[type]
        gateway = gateway_class(text)
        self.shapes.append(gateway)
        return gateway

    def end(self, text: str, type: EventType) -> Event:
        event_class = globals()[type]
        end = event_class(text)
        self.shapes.append(end)
        return end

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def draw(self) -> None:
        self.painter.draw_box(self.x, self.y, self.width, self.height, "lightgreen")
        self.painter.draw_text(
            self.x + 10, self.y + 10, self.text, "arial", 12, "black"
        )
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.painter)

    def set_draw_position(self, x: int, y: int, painter: Painter) -> None:
        self.painter = painter
        ### Determine the x and y position of the lane
        self.x = x if x > 0 else self.SURFACE_LEFT_MARGIN
        self.y = y if y > 0 else self.SURFACE_TOP_MARGIN

        if self.shapes:
            for shape in self.shapes:
                x, y, w, h = shape.set_draw_position(
                    self.x + self.width, self.y, painter
                )
                self.width = max(self.width, x + w)
                self.height = max(self.height, y + h)

        print(f"lane: {self.x}, {self.y}, {self.width}, {self.height}")
        return self.x, self.y, self.width, self.height
