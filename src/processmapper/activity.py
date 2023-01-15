from processmapper.box import Box


class Activity(Box):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "activity"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name


class Task(Activity):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "task"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name


class Subprocess(Activity):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.shape_type = "subprocess"
        self.shape_color = "white"
        self.shape_text_color = "black"
        self.shape_text = name
