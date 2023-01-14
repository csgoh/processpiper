from dataclasses import dataclass, field
from processmapper.start import Start


@dataclass
class Lane:
    shapes: list = field(init=False, default_factory=list)
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    text = field(init=True)

    def start(self, text: str) -> Start:
        start = Start(text)
        self.shapes.append(start)
        return start

    def activity(self, text: str) -> None:
        pass

    def end(self, text: str) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.set_draw_position()
        pass

    def set_draw_position(self) -> None:
        ### Determine the x and y position of the lane
        ### Determine the width and height of the lane
        pass
