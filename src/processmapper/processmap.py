from dataclasses import dataclass, field
from processmapper.lane import Lane


@dataclass
class ProcessMap:
    lanes: list = field(init=False)

    def __init__(self, name: str) -> None:
        self.name = name
        self.shapes = []

    def add_lane(self, lane_text: str) -> Lane:
        lane = Lane(lane_text)
        self.shapes.append(lane)
        return lane

    def draw(self) -> None:
        pass

    def save(self, filename: str) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def close(self) -> None:
        ...
