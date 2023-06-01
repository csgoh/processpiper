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
import time
from .event import *
from .lane import Lane, ElementType, EventType
from .pool import Pool
from .painter import Painter
from .shape import *
from .title import Title
from .footer import Footer
from .constants import Configs
from .helper import Helper
from .layout import Grid

import logging


class UnconnectedElementException(Exception):
    pass


class EmptyProcessMapException(Exception):
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

    layout_grid: list = field(init=False, default_factory=list)

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

        font = font or self.__painter.pool_font
        font_size = font_size or self.__painter.pool_font_size
        font_colour = font_colour or self.__painter.pool_font_colour
        fill_colour = fill_colour or self.__painter.pool_fill_colour

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

        font = font or self.__painter.lane_font
        font_size = font_size or self.__painter.lane_font_size
        font_colour = font_colour or self.__painter.lane_font_colour
        fill_colour = fill_colour or self.__painter.lane_fill_colour
        text_alignment = text_alignment or self.__painter.lane_text_alignment
        background_fill_colour = (
            background_fill_colour or self.__painter.lane_background_fill_colour
        )

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

    def _get_current_x_position(self) -> int:
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

    def _get_next_x_position(self, previous_shape_width: str) -> int:
        """Get the next x position for the next shape to be added"""
        if self.next_shape_x == 0:
            self.next_shape_x = (
                Configs.SURFACE_LEFT_MARGIN
                + Configs.POOL_TEXT_WIDTH
                + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                + Configs.LANE_TEXT_WIDTH
                + Configs.LANE_SHAPE_LEFT_MARGIN
            )
            Helper.printc(f"            [0]get_next_x_position: {self.next_shape_x}")
        else:
            self.next_shape_x += previous_shape_width + Configs.VSPACE_BETWEEN_SHAPES
            Helper.printc(f"            [1]get_next_x_position: {self.next_shape_x}")
        return self.next_shape_x

    def _find_start_shape(self) -> Shape:
        """Find the start shape in the process map"""
        for pool in self._pools:
            for lane in pool.lanes:
                for shape in lane.shapes:
                    ### If the shape has no connection_from, it is the start shape
                    Helper.printc(f"{shape.name} - {len(shape.connection_from)}")
                    if len(shape.connection_from) == 0:
                        return shape
        return None

    def _get_lane_by_id(self, lane_id: int) -> Lane:
        """Get a lane by its id"""
        for pool in self._pools:
            for lane in pool.lanes:
                if lane.id == lane_id:
                    return lane
        return None

    def _get_pool_by_name(self, name: str) -> Pool:
        """Get a pool by its name"""
        for pool in self._pools:
            if pool.name == name:
                return pool
        return None

    def _set_shape_x_position(
        self,
        previous_shape: Shape,
        current_shape: Shape,
        index: int = 0,
        x_pos: int = 0,
    ):
        """Set the x position for the shape"""
        current_lane = self._get_lane_by_id(current_shape.lane_id)
        Helper.printc(
            f"set_shape_x_position: {current_lane.name}, {current_shape.name}", "34"
        )
        if index == 0:
            if previous_shape is not None:
                if previous_shape.pool_name == current_shape.pool_name:
                    if previous_shape.lane_id == current_shape.lane_id:
                        current_shape.x = self._get_next_x_position(
                            previous_shape.width
                        )
                        Helper.printc("          same pool same lane", 31)
                    else:
                        current_shape.x = self._get_next_x_position(
                            previous_shape.width
                        )
                        Helper.printc("          same pool diff lane", 32)
                else:
                    # current_shape.x = self._get_next_x_position(previous_shape.width)
                    current_shape.x = self._get_current_x_position()
                    Helper.printc("          diff pool", 33)
                    Helper.printc(f"          {self.next_shape_x=}", 36)
                    self.next_shape_x += (
                        current_shape.width + Configs.VSPACE_BETWEEN_SHAPES
                    )
                    Helper.printc(f"          {self.next_shape_x=}", 37)
            else:
                current_shape.x = self._get_next_x_position(0)
                Helper.printc("          previous = none", 35)
        else:
            ### If previous shape is connecting to multiple shapes,
            ### the x position of the shape is the same as the previous shape
            current_shape.x = x_pos
        current_lane.width = max(current_lane.width, current_shape.x + 100)
        Helper.printc(
            f"          {current_shape.x=}, {current_shape.y=}, {current_shape.width=}, [{current_lane.name=}]"
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
                preserved_x_pos = self._set_shape_x_position(
                    current_shape, next_shape, index, preserved_x_pos
                )
            else:
                self._set_shape_x_position(
                    current_shape, next_shape, index, preserved_x_pos
                )

        return current_shape.x

    def _set_shape_y_position(self, shape: Shape, index: int = 0):
        """Set the y position for the shape"""
        lane = self._get_lane_by_id(shape.lane_id)
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
        Helper.printc(f"         {shape.name} looping..", "32")
        for index, connection in enumerate(shape.connection_to):
            next_shape = connection.target
            Helper.printc(
                f"             {next_shape.name}, {next_shape.y_pos_traversed}", "32"
            )
            if next_shape.y_pos_traversed is True:
                continue

            self._set_shape_y_position(next_shape, index)

    def _set_draw_position(self, painter: Painter) -> tuple:
        """Set the draw position for the process map"""
        ### Set process map title
        self._title.set_draw_position(
            Configs.SURFACE_LEFT_MARGIN, Configs.SURFACE_TOP_MARGIN, painter
        )

        ### Test Grid
        test_grid = Grid(self._pools)
        test_grid.print_grid()
        return None

        Helper.printc("*** Setting elements' x position...")
        start_shape = self._find_start_shape()

        self._set_shape_x_position(None, start_shape, 0, 0)

        Helper.printc("*** Setting elements' y position...")
        self._set_shape_y_position(start_shape)

        Helper.printc("*** Calculating pool and lane width and height...")
        x, y = (
            0,
            self._title.y + self._title.height + Configs.VSPACE_BETWEEN_TITLE_AND_POOL,
        )
        for pool in self._pools:
            for lane in pool.lanes:
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

            first_lane_y = pool.lanes[0].y

            pool.set_draw_position(Configs.SURFACE_LEFT_MARGIN, first_lane_y, painter)

        ### Reset traversed flags
        self._reset_traversed_flags()

        ### Set shape y position one more time, so that it aligns with the lane y position
        self._set_shape_y_position(start_shape)

        ### Set process map footer
        if self._footer is not None:
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

    def _reset_traversed_flags(self):
        """Reset the traversed flags for all shapes in the process map"""
        Helper.printc("*** Resetting traversed flags...", "32")
        for pool in self._pools:
            for lane in pool.lanes:
                lane.next_shape_y = 0
                lane.shape_row_count = 0
                for shape in lane.shapes:
                    Helper.printc(f"    {shape.name}", "32")
                    shape.y_pos_traversed = False

    def _get_orphan_elements(self) -> list:
        orphan_elements = []
        for pool in self._pools:
            for lane in pool.lanes:
                for shape in lane.shapes:
                    if (
                        len(shape.connection_to) == 0
                        and len(shape.connection_from) == 0
                    ):
                        orphan_elements.append(shape.name)

        return orphan_elements

    def _print_connection(self, shape: Shape):
        Helper.printc(f"*****    {shape.name}", "32")
        for connection in shape.connection_to:
            Helper.printc(f"            {connection.target.name}", "32")
            self._print_connection(connection.target)

    def draw(self) -> None:
        """Draw the process map"""

        ### --Validate the process map--

        ### Ensure title is defined
        if (len(self.title) == 0) and (self._title is None):
            raise ValueError("The process map must contain a title")

        ### Ensure at least a pool is defined
        if len(self._pools) == 0:
            raise EmptyProcessMapException(
                "The process map must contain at least one pool or lane"
            )

        ### Ensure at least one shape is defined
        for pool in self._pools:
            if len(pool.lanes) > 0:
                if len(pool.lanes[0].shapes) == 0:
                    raise EmptyProcessMapException(
                        "The process map must contain at least one shape"
                    )

        ### Ensure connections are defined
        orphan_elements = self._get_orphan_elements()
        if len(orphan_elements) > 0:
            raise UnconnectedElementException(
                f"The following element(s) are defined but not connected to other element(s): \n{orphan_elements}"
            )

        ### Replace the class type of shapes with the correct class type
        for pool in self._pools:
            for lane in pool.lanes:
                for index, shape in enumerate(lane.shapes):
                    self.replace_signal_element(lane, index, shape)
                    self.replace_conditional_element(lane, index, shape)
                    self.replace_message_element(lane, index, shape)

        ### Set the draw position of pools, lanes, shapes and connections
        self._set_draw_position(self.__painter)

        ### Draw the process map
        self._title.draw()

        if self._pools:
            for pool in self._pools:
                ### Draw the pools first
                pool.draw()
                if pool.lanes:
                    ### Draw the lanes second
                    for lane in pool.lanes:
                        lane.draw()

            for pool in self._pools:
                if pool.lanes:
                    ### Then draw the shapes in the lanes
                    for lane in pool.lanes:
                        lane.draw_shape()

                    ### Finally draw the connections between the shapes
                    for lane in pool.lanes:
                        lane.draw_connection()

        if self._footer is not None:
            self._footer.draw()

        if self.auto_size is True:
            self.__painter.set_surface_size(self.width, self.height)

    def replace_message_element(self, lane, index, shape):
        if type(shape) == Message:
            Helper.debug_log("  matched with Message")
            ### Check if the signal is a start signal. i.e it has no connection from
            if len(shape.connection_to) > 0 and len(shape.connection_from) == 0:
                Helper.debug_log("      start MESSAGE")
                new_shape = self.replace_element_type(lane, shape, ElementType.MESSAGE)

                lane.shapes[index] = self.replace_connections(shape, new_shape)

            elif (  ### Check if the signal is an intermediate signal. i.e it has both connection from and to
                len(shape.connection_to) > 0 and len(shape.connection_from) > 0
            ):
                Helper.debug_log("      MESSAGE_INTERMEDIATE")
                new_shape = self.replace_element_type(
                    lane, shape, ElementType.MESSAGE_INTERMEDIATE
                )
                lane.shapes[index] = self.replace_connections(shape, new_shape)

            else:  ### Check if the signal is an end signal. i.e it has no connection to
                Helper.debug_log("      MESSAGE_END")
                new_shape = self.replace_element_type(
                    lane, shape, ElementType.MESSAGE_END
                )
                lane.shapes[index] = self.replace_connections(shape, new_shape)

    def replace_conditional_element(self, lane, index, shape):
        if type(shape) == Conditional:
            Helper.debug_log("  matched with Conditional")
            ### Check if the signal is a start signal. i.e it has no connection from
            if len(shape.connection_to) > 0 and len(shape.connection_from) == 0:
                Helper.debug_log("      start CONDITIONAL")
                new_shape = self.replace_element_type(
                    lane, shape, ElementType.CONDITIONAL
                )

                lane.shapes[index] = self.replace_connections(shape, new_shape)

            elif (  ### Check if the signal is an intermediate signal. i.e it has both connection from and to
                len(shape.connection_to) > 0 and len(shape.connection_from) > 0
            ):
                Helper.debug_log("      intermediate CONDITIONAL_INTERMEDIATE")
                new_shape = self.replace_element_type(
                    lane, shape, ElementType.CONDITIONAL_INTERMEDIATE
                )
                lane.shapes[index] = self.replace_connections(shape, new_shape)

    def replace_signal_element(self, lane, index, shape):
        if type(shape) == Signal:
            Helper.debug_log("  matched with Signal")
            ### Check if the signal is a start signal. i.e it has no connection from
            if len(shape.connection_to) > 0 and len(shape.connection_from) == 0:
                Helper.debug_log("      start signal")
                new_shape = self.replace_element_type(lane, shape, ElementType.SIGNAL)

                lane.shapes[index] = self.replace_connections(shape, new_shape)

            elif (  ### Check if the signal is an intermediate signal. i.e it has both connection from and to
                len(shape.connection_to) > 0 and len(shape.connection_from) > 0
            ):
                Helper.debug_log("      intermediate signal")
                new_shape = self.replace_element_type(
                    lane, shape, ElementType.SIGNAL_INTERMEDIATE
                )
                lane.shapes[index] = self.replace_connections(shape, new_shape)

            else:  ### Check if the signal is an end signal. i.e it has no connection to
                Helper.debug_log("      end signal")
                new_shape = self.replace_element_type(
                    lane, shape, ElementType.SIGNAL_END
                )
                lane.shapes[index] = self.replace_connections(shape, new_shape)

    def replace_element_type(self, lane, shape, new_shape_type: ElementType):
        event_class = globals()[new_shape_type]
        new_shape = event_class(
            shape.name,
            lane.name,
        )

        return new_shape

    def replace_connections(self, current_shape, new_shape):
        new_shape.lane_id = current_shape.lane_id
        new_shape.pool_name = current_shape.pool_name
        new_shape.font = current_shape.font
        new_shape.font_size = current_shape.font_size
        new_shape.font_colour = current_shape.font_colour
        new_shape.fill_colour = current_shape.fill_colour
        new_shape.text_alignment = current_shape.text_alignment
        new_shape.connection_to = current_shape.connection_to
        for connection_index, connection in enumerate(current_shape.connection_to):
            new_connection = Connection(
                new_shape,
                connection.target,
                connection.label,
                connection.connection_type,
            )
            Helper.printc(
                f"      creating new connection: {new_connection.source.name}"
            )
            new_shape.connection_to[connection_index] = new_connection
        self.replace_connection_from(current_shape, new_shape)
        return new_shape

    def replace_connection_from(self, current_shape, new_shape):
        for shape_index, shape in enumerate(current_shape.connection_from):
            for _, connection_to in enumerate(shape.connection_to):
                new_connection = Connection(
                    connection_to.source,
                    new_shape,
                    connection_to.label,
                    connection_to.connection_type,
                )
                shape.connection_to[shape_index] = new_connection

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
