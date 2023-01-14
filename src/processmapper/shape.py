from dataclasses import dataclass, field
from processmapper import Shape


@dataclass
class Shape:
    x: int = field(init=False)
    y: int = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)
    points: dict = field(init=False)

    def connect(
        self,
        target: Shape,
        connection_type: str = "sequence",
    ) -> None:
        point_A, point_B = self.find_nearest_points(self.points, target.points)
        self.draw_line(
            point_A[0], point_A[1], point_B[0], point_B[1], "black", 0.1, 1, "solid"
        )
        self.draw_arrow(point_A[0], point_A[1], point_B[0], point_B[1])
        return target

    def draw(self) -> None:
        raise NotImplementedError
