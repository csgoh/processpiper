from processmapper.circle import Circle


class Terminate(Circle):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "terminate"
        self.shape_color = "red"
        self.shape_text_color = "white"
        self.shape_text = name
