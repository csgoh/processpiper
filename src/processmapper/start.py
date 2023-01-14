from processmapper.circle import Circle


class Signal(Circle):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name)
        self.shape_type = "signal"
        self.shape_color = "red"
        self.shape_text_color = "white"
        self.shape_text = name
