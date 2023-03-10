from processmapper.shape import Box
from processmapper.painter import Painter


class Activity(Box):
    ...


class Task(Activity):
    ...


class Subprocess(Activity):
    def draw(self, painter: Painter):
        super().draw(painter)
        # Draw a plus sign in a box

        subprocess_width, subprocess_height = painter.get_text_dimension(
            "[+]", "arial.ttf", 14
        )
        subprocess_x_pos = self.x + ((self.width - subprocess_width) / 2)
        painter.draw_text(
            subprocess_x_pos,
            self.y + self.height - subprocess_height,
            "[+]",
            "arial.ttf",
            14,
            "black",
        )
