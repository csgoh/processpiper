from processmapper.shape import Shape


class Circle(Shape):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.points = {
            "top_left": (x - radius, y - radius),
            "top_right": (x + radius, y - radius),
            "bottom_left": (x - radius, y + radius),
            "bottom_right": (x + radius, y + radius),
        }
