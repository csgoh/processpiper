from dataclasses import dataclass, field
from processmapper.event import Event
from processmapper.activity import Activity
from processmapper.gateway import Gateway
from processmapper.painter import Painter
from processmapper.processmap import EventType, ActivityType, GatewayType


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

    LANE_TEXT_SPACE = 40

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

    def draw(self, x: int, y: int) -> None:
        self.painter.draw_rectangle(
            self.x, self.y, self.width, self.height, "black", "white"
        )
        self.painter.draw_text(self.x + 10, self.y + 10, self.text, "black", "white")

    def set_draw_position(self, x: int, y: int) -> None:
        ### Determine the x and y position of the lane
        self.x, self.y = x, y

        if self.shapes:
            for shape in self.shapes:
                x, y, w, h = shape.set_draw_position(x, y, self.painter)
                self.width = max(self.width, x + w)
                self.height = max(self.height, y + h)

        ### Determine the width and height of the lane
        pass
