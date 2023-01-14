from processmapper.shape import Shape


class Data(Shape):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.points = {
            "top_left": (x, y),
            "top_right": (x + width, y),
            "bottom_left": (x, y + height),
            "bottom_right": (x + width, y + height),
        }
