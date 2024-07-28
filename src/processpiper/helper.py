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
import logging
import uuid
from rich.console import Console
from rich.panel import Panel


class Helper:
    show_layout_grid = False
    show_pool_lane = False
    show_x_position = False
    show_y_position = False
    show_draw_position = False
    show_draw = False
    show_draw_connection = False
    show_export_to_bpmn = False
    show_general = False

    @staticmethod
    def printc(
        message: str,
        color: str = "30",
        reverse: bool = False,
        end: str = "\n",
        rich_type: str = "text",
        show_level: str = "general",
    ):
        """Print text in color"""

        root_logger = logging.getLogger()

        if root_logger.getEffectiveLevel() == logging.DEBUG and (
            (show_level == "layout_grid" and Helper.show_layout_grid)
            or (show_level == "pool_lane" and Helper.show_pool_lane)
            or (show_level == "x_position" and Helper.show_x_position)
            or (show_level == "y_position" and Helper.show_y_position)
            or (show_level == "draw_connection" and Helper.show_draw_connection)
            or (show_level == "draw_position" and Helper.show_draw_position)
            or (show_level == "draw" and Helper.show_draw)
            or (show_level == "export_to_bpmn" and Helper.show_export_to_bpmn)
            or (show_level == "general" and Helper.show_general)
        ):
            console = Console()
            if rich_type == "text":
                style_attribute = "reverse" if reverse else ""
                console.print(message, end=end, style=style_attribute)
            elif rich_type == "panel":
                console.print(Panel(message), style="blue")

    @staticmethod
    def print_info(message: str, color: str = "30", end: str = "\n"):
        """Print text in color"""

        root_logger = logging.getLogger()

        if root_logger.getEffectiveLevel() == logging.INFO:
            console = Console()
            console.print(f"\033[1;{color}m{message}\033[0m", end=end)

    @staticmethod
    def debug_log(message: str):
        """Log debug message"""
        logging.debug(message)

    @staticmethod
    def info_log(message: str):
        """Log info message"""
        logging.info(message)

    @staticmethod
    def get_uuid(prefix: str = "PIPER"):
        # replace uuid '-' with '_'
        uuid_str = str(uuid.uuid4()).replace("-", "_")
        # shorten to 8 chars
        uuid_str = uuid_str[:8]
        prefix = "".join(e for e in prefix if e.isalnum() or e == "_")
        return f"{prefix.upper()}_{uuid_str}"
