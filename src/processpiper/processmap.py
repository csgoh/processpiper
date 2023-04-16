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
from dataclasses import dataclass, field
from .lane import Lane
from .pool import Pool
from .painter import Painter
from .shape import Shape
from .title import Title
from .footer import Footer
from .constants import Configs
from .helper import Helper

import time
import logging


class UnconnectedElementException(Exception):
    pass


@dataclass
class ProcessMap:
    """Process Map Class"""

    title: str = field(init=True, default="<Process Map Title>")
    width: int = field(init=True, default=3200)
    height: int = field(init=True, default=3200)
    auto_size: bool = field(init=True, default=True)
    colour_theme: str = field(init=True, default="DEFAULT")

    _title: Title = field(init=False)
    _footer: Footer = field(init=False, default=None)
    _pools: list = field(init=False, default_factory=list)

    next_shape_x: int = field(init=False, default=0)

    lane_y_pos: int = field(init=False, default=0)
    lane_max_width: int = field(init=False, default=0)

    def __post_init__(self):
        """Initialise the Process Map Class"""
        logging.basicConfig(
            # filename="processpiper.log",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.start_time = time.time()
        self.__painter = Painter(self.width, self.height)
        self.__set_colour_theme(self.colour_theme)
        self.__painter.set_background_colour(self.__painter.background_colour)
        self._title = Title(
            self.title,
            self.__painter.title_font,
            self.__painter.title_font_size,
            self.__painter.title_font_colour,
        )

    def add_pool(
        self,
        pool_name: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        text_alignment: str = "centre",
    ) -> Pool:
        """Add a Pool to the Process Map"""
        if font == "":
            font = self.__painter.pool_font
        if font_size == 0:
            font_size = self.__painter.pool_font_size
        if font_colour == "":
            font_colour = self.__painter.pool_font_colour
        if fill_colour == "":
            fill_colour = self.__painter.pool_fill_colour

        pool = Pool(
            pool_name,
            font,
            font_size,
            font_colour,
            fill_colour,
            text_alignment,
            self.__painter,
        )
        self._pools.append(pool)
        return pool

    def add_lane(
        self,
        lane_name: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        text_alignment: str = "centre",
        background_fill_colour: str = "",
    ) -> Lane:
        """Add a Lane to the Process Map"""
        if font == "":
            font = self.__painter.lane_font
        if font_size == 0:
            font_size = self.__painter.lane_font_size
        if font_colour == "":
            font_colour = self.__painter.lane_font_colour
        if fill_colour == "":
            fill_colour = self.__painter.lane_fill_colour
        if text_alignment == "":
            text_alignment = self.__painter.lane_text_alignment
        if background_fill_colour == "":
            background_fill_colour = self.__painter.lane_background_fill_colour

        pool = self.add_pool("Default Pool")
        lane = pool.add_lane(
            lane_name,
            font,
            font_size,
            font_colour,
            fill_colour,
            text_alignment,
            background_fill_colour,
        )
        return lane

    def set_footer(
        self,
        footer_name: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
    ):
        """Set the footer text for the Process Map"""
        if font == "":
            font = self.__painter.footer_font
        if font_size == 0:
            font_size = self.__painter.footer_font_size
        if font_colour == "":
            font_colour = self.__painter.footer_font_colour

        self._footer = Footer(footer_name, font, font_size, font_colour)

    def get_current_x_position(self) -> int:
        """Get the current x position for the next shape to be added"""
        if self.next_shape_x == 0:
            self.next_shape_x = (
                Configs.SURFACE_LEFT_MARGIN
                + Configs.POOL_TEXT_WIDTH
                + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                + Configs.LANE_TEXT_WIDTH
                + Configs.LANE_SHAPE_LEFT_MARGIN
            )

        return self.next_shape_x

    def get_next_x_position(self) -> int:
        """Get the next x position for the next shape to be added"""
        if self.next_shape_x == 0:
            self.next_shape_x = (
                Configs.SURFACE_LEFT_MARGIN
                + Configs.POOL_TEXT_WIDTH
                + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                + Configs.LANE_TEXT_WIDTH
                + Configs.LANE_SHAPE_LEFT_MARGIN
            )
        else:
            self.next_shape_x += 100 + Configs.HSPACE_BETWEEN_SHAPES
        return self.next_shape_x

    def find_start_shape(self) -> Shape:
        """Find the start shape in the process map"""
        for pool in self._pools:
            for lane in pool._lanes:
                for shape in lane.shapes:
                    ### If the shape has no connection_from, it is the start shape
                    Helper.printc(f"{shape.name} - {len(shape.connection_from)}")
                    if len(shape.connection_from) == 0:
                        return shape
        return None

    def get_lane_by_id(self, id: int) -> Lane:
        """Get a lane by its id"""
        for pool in self._pools:
            for lane in pool._lanes:
                if lane.id == id:
                    return lane
        return None

    def get_pool_by_name(self, name: str) -> Pool:
        """Get a pool by its name"""
        for pool in self._pools:
            if pool.name == name:
                return pool
        return None

    def set_shape_x_position(
        self,
        previous_shape: Shape,
        current_shape: Shape,
        index: int = 0,
        x_pos: int = 0,
    ):
        """Set the x position for the shape"""
        current_lane = self.get_lane_by_id(current_shape.lane_id)
        Helper.printc(
            f"set_shape_x_position: {current_lane.name}, {current_shape.name}", "34"
        )
        if index == 0:
            current_pool = self.get_pool_by_name(current_shape.pool_name)
            if previous_shape is not None:
                if previous_shape.pool_name == current_shape.pool_name:
                    if previous_shape.lane_id == current_shape.lane_id:
                        current_shape.x = self.get_next_x_position()
                        Helper.printc(f"          same pool same lane")
                    else:
                        current_shape.x = self.get_next_x_position()
                        Helper.printc(f"          same pool diff lane")
                else:
                    previous_pool = self.get_pool_by_name(previous_shape.pool_name)
                    current_shape.x = self.get_next_x_position()
                    Helper.printc(f"          diff pool")
            else:
                current_shape.x = self.get_next_x_position()
                Helper.printc(f"          previous = none")
        else:
            ### If previous shape is connecting to multiple shapes,
            ### the x position of the shape is the same as the previous shape
            current_shape.x = x_pos
        current_lane.width = max(current_lane.width, current_shape.x + 100)
        Helper.printc(
            f"          x={current_shape.x}, y={current_shape.y}, w={current_shape.width}, [{current_lane.name}]"
        )

        self.lane_max_width = max(self.lane_max_width, current_lane.width)
        current_shape.x_pos_traversed = True

        preserved_x_pos = 0
        for index, next_connection in enumerate(current_shape.connection_to):
            next_shape = next_connection.target
            if next_shape.x_pos_traversed is True:
                continue
            Helper.printc(f"    |{index}| - <{next_shape.name}>")
            if index == 0:
                preserved_x_pos = self.set_shape_x_position(
                    current_shape, next_shape, index, preserved_x_pos
                )
            else:
                self.set_shape_x_position(
                    current_shape, next_shape, index, preserved_x_pos
                )

        return current_shape.x

    def set_shape_y_position(self, shape: Shape, index: int = 0):
        """Set the y position for the shape"""
        lane = self.get_lane_by_id(shape.lane_id)
        Helper.printc(
            f">>>>set_shape_y_position: {lane.name}, {shape.name}, {index}", "34"
        )
        if index == 0:
            ### If previous shape is connecting to one shape,
            ### the y position of the shape is the same as the previous shape
            Helper.printc(
                f"    get_current_y_position()-Before: {lane.shape_row_count}", "32"
            )
            shape.y = lane.get_current_y_position()
            Helper.printc(
                f"    get_current_y_position()-After: {lane.shape_row_count}", "32"
            )
        else:
            ### Otherwise, the y position of the shape is the next y position
            Helper.printc(
                f"    get_next_y_position()-Before: {lane.shape_row_count}", "32"
            )
            shape.y = lane.get_next_y_position()
            Helper.printc(
                f"    get_next_y_position()-After: {lane.shape_row_count}", "32"
            )

        shape.set_draw_position(self.__painter)

        shape.y_pos_traversed = True

        # for shape in lane.shapes:
        for index, connection in enumerate(shape.connection_to):
            next_shape = connection.target
            if next_shape.y_pos_traversed is True:
                continue

            self.set_shape_y_position(next_shape, index)

    def set_draw_position(self, painter: Painter) -> tuple:
        """Set the draw position for the process map"""
        ### Set process map title
        self._title.set_draw_position(
            Configs.SURFACE_LEFT_MARGIN, Configs.SURFACE_TOP_MARGIN, painter
        )

        Helper.printc("*** Setting elements' x position...")
        start_shape = self.find_start_shape()

        self.set_shape_x_position(None, start_shape, 0, 0)

        Helper.printc(f"*** Setting elements' y position...")
        self.set_shape_y_position(start_shape)

        Helper.printc(f"*** Calculating pool and lane width and height...")
        x, y = (
            0,
            self._title.y + self._title.height + Configs.VSPACE_BETWEEN_TITLE_AND_POOL,
        )
        for pool in self._pools:
            for lane in pool._lanes:
                lane.painter = painter
                lane.x = (
                    x
                    if x > 0
                    else Configs.SURFACE_LEFT_MARGIN
                    + Configs.POOL_TEXT_WIDTH
                    + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                )
                lane.y = y if y > 0 else Configs.SURFACE_TOP_MARGIN
                lane.width = self.lane_max_width

                # lane.shape_row_count = self.check_lane_row_count(lane)
                Helper.printc(
                    f"*** {lane.name} shape row count: {lane.shape_row_count}", 35
                )
                lane.height = (
                    (lane.shape_row_count * 60)
                    + ((lane.shape_row_count - 1) * Configs.VSPACE_BETWEEN_SHAPES)
                    + Configs.LANE_SHAPE_TOP_MARGIN
                    + Configs.LANE_SHAPE_BOTTOM_MARGIN
                )
                Helper.printc(
                    f"{lane.name}, height: {lane.height} = ({lane.shape_row_count} * 60) + ({lane.shape_row_count} - 1) * {Configs.VSPACE_BETWEEN_SHAPES} + {Configs.LANE_SHAPE_TOP_MARGIN} + {Configs.LANE_SHAPE_BOTTOM_MARGIN}"
                )
                y = lane.y + lane.height + Configs.VSPACE_BETWEEN_LANES

            y += Configs.VSPACE_BETWEEN_POOLS

            first_lane_y = pool._lanes[0].y

            pool.set_draw_position(Configs.SURFACE_LEFT_MARGIN, first_lane_y, painter)

        ### Reset traversed flags
        self.reset_traversed_flags()

        ### Set shape y position one more time, so that it aligns with the lane y position
        self.set_shape_y_position(start_shape)

        ### Set process map footer
        if self._footer != None:
            self._footer.set_draw_position(
                Configs.SURFACE_LEFT_MARGIN,
                y + Configs.VSPACE_BETWEEN_POOL_AND_FOOTER,
                painter,
            )
            self.height = (
                self._footer.y + self._footer.height + Configs.SURFACE_BOTTOM_MARGIN
            )
        else:
            self.height = (
                y
                + Configs.VSPACE_BETWEEN_POOL_AND_FOOTER
                + Configs.SURFACE_BOTTOM_MARGIN
            )

        self.width = (
            Configs.SURFACE_LEFT_MARGIN
            + Configs.POOL_TEXT_WIDTH
            + self.lane_max_width
            + Configs.SURFACE_LEFT_MARGIN
        )

    def reset_traversed_flags(self):
        """Reset the traversed flags for all shapes in the process map"""
        for pool in self._pools:
            for lane in pool._lanes:
                lane.next_shape_y = 0
                lane.shape_row_count = 0
                for shape in lane.shapes:
                    shape.y_pos_traversed = False

    def get_orphan_elements(self) -> list:
        orphan_elements = []
        for pool in self._pools:
            for lane in pool._lanes:
                for shape in lane.shapes:
                    if (
                        len(shape.connection_to) == 0
                        and len(shape.connection_from) == 0
                    ):
                        orphan_elements.append(shape.name)

        return orphan_elements

    def draw(self) -> None:
        """Draw the process map"""
        orphan_elements = self.get_orphan_elements()
        if len(orphan_elements) > 0:
            raise UnconnectedElementException(
                f"The following element(s) are defined but not connected to other element(s): \n{orphan_elements}"
            )

        self.set_draw_position(self.__painter)

        self._title.draw()

        if self._pools:
            for pool in self._pools:
                ### Draw the pools first
                pool.draw()
                if pool._lanes:
                    ### Draw the lanes second
                    for lane in pool._lanes:
                        lane.draw()

            for pool in self._pools:
                if pool._lanes:
                    ### Then draw the shapes in the lanes
                    for lane in pool._lanes:
                        lane.draw_shape()

                    ### Finally draw the connections between the shapes
                    for lane in pool._lanes:
                        lane.draw_connection()

        if self._footer != None:
            self._footer.draw()

        if self.auto_size == True:
            self.__painter.set_surface_size(self.width, self.height)

    def __set_colour_theme(self, palette: str) -> None:
        """This method sets the colour palette"""
        self.__painter.set_colour_theme(palette)

    def save(self, filename: str) -> None:
        """This method saves the process map to a file"""
        self.__painter.save_surface(filename)

        elapsed_time = (time.time() - self.start_time) * 1000
        Helper.info_log(f"Took [{elapsed_time:.2f}ms] to generate '{filename}' diagram")

    def __enter__(self):
        """This method is called when the 'with' statement is used"""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """This method is called when the 'with' statement is used"""
        pass
