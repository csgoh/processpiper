from processmapper.shape import Circle


class Event(Circle):
    def draw_event(self) -> None:
        ### draw common event shape and text
        self.painter.draw_circle(
            self.x, self.y, self.radius, self.shape_color, self.shape_text_color
        )
        self.painter.draw_text(
            self.x, self.y, self.shape_text, self.shape_text_color, self.shape_color
        )

    def get_next_shape_position(self) -> tuple:
        SPACE_BETWEEN_SHAPES = 20

        return self.x + self.width + SPACE_BETWEEN_SHAPES, self.y


class Start(Event):
    def draw_event(self) -> None:
        ### Draw start event (inner ring)
        self.painter.draw_circle(self.x, self.y, self.radius, self.shape_color)

        ### Then draw the common event shape and text
        return super().draw_event()


class End(Event):
    ...


class Timer(Event):
    ...


class Intermediate(Event):
    ...
