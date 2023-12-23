class Side(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5


class Coordinate:
    x_pos: int
    y_pos: int
    # declare enum variable
    side: Side

    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.side = Side.NONE

    def __repr__(self) -> str:
        return f"pos: ({self.x_pos},{self.y_pos}), side: {self.side}"

    def get_xy(self) -> (int, int):
        return (self.x_pos, self.y_pos)