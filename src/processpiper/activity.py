# MIT License

# Copyright (c) 2022 CS Goh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from .shape import Box
from .painter import Painter


class Activity(Box):
    """Represents an activity types in a process flow diagram."""

    ...


class Task(Activity):
    """A task is a special type of activity that is represented by a box."""

    ...


class Subprocess(Activity):
    """A subprocess is a special type of activity that is represented by a box with a plus sign in it."""

    def draw(self, painter: Painter):
        super().draw(painter)

        ### Draw a plus sign in a box
        subprocess_width, subprocess_height = painter.get_text_dimension(
            "[+]", painter.element_font, 14
        )
        subprocess_x_pos = self.x + ((self.width - subprocess_width) / 2)
        painter.draw_text(
            subprocess_x_pos,
            self.y + self.height - subprocess_height,
            "[+]",
            painter.element_font,
            14,
            painter.element_font_colour,
        )


class ServiceTask(Activity):
    def draw(self, painter: Painter):
        super().draw(painter)

        raise NotImplementedError("ServiceTask is not implemented yet.")


### To implement: User Task,Script Task,Business Rule Task, Manual Task, Received Task,Send Task, Receive Task
