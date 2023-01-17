from processmapper.shape import Diamond


class Gateway(Diamond):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "gateway"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name


class Exclusive(Gateway):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "exclusive"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name


class Parallel(Gateway):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "parallel"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name


class Inclusive(Gateway):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "inclusive"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name
