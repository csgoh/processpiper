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
    width: int = field(init=True, default=5000)
    height: int = field(init=True, default=5000)
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
            level=logging.DEBUG,
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
        self._layout_grid = Grid()

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
        return pool.add_lane(
            lane_name,
            font,
            font_size,
            font_colour,
            fill_colour,
            text_alignment,
            background_fill_colour,
        )

    def set_footer(
        self,
        footer_name: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
    ):
        """Set the footer text for the Process Map"""
        if not font:
            font = self.__painter.footer_font
        if font_size == 0:
            font_size = self.__painter.footer_font_size
        if not font_colour:
            font_colour = self.__painter.footer_font_colour

        self._footer = Footer(footer_name, font, font_size, font_colour)

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
    ):
        Helper.printc(
            "~~~ Setting shapes' x position...", "32", show_level="x_position"
        )
        for lane_id, lane in self._layout_grid.get_grid_items():
            Helper.printc(f"{lane_id=}", show_level="x_position")
            for row_number, col in lane.items():
                Helper.printc(f"{row_number=}", end=":\n", show_level="x_position")
                for col_idx, item in enumerate(col):
                    if item is not None:
                        item.x = (
                            Configs.SURFACE_LEFT_MARGIN
                            + Configs.POOL_TEXT_WIDTH
                            + Configs.HSPACE_BETWEEN_POOL_AND_LANE
                            + Configs.LANE_TEXT_WIDTH
                            + Configs.LANE_SHAPE_LEFT_MARGIN
                        ) + (
                            col_idx
                            * (Configs.BOX_WIDTH + Configs.HSPACE_BETWEEN_SHAPES)
                        )
                        Helper.printc(
                            f"    {item.name=}, {col_idx+1=}, {item.x=}",
                            show_level="x_position",
                        )
                    else:
                        Helper.printc("    {'None'}", show_level="x_position")
            Helper.printc("", show_level="x_position")

    def _set_shape_y_position(self):
        Helper.printc(
            "~~~ Setting shapes' y position...", "32", show_level="y_position"
        )
        for lane_id, lane in self._layout_grid.get_grid_items():
            Helper.printc(f"{lane_id=}", show_level="y_position")
            this_lane = self._get_lane_by_id(lane_id)
            Helper.printc(
                f"{this_lane.name=}, {this_lane.x=}, {this_lane.y=}",
                show_level="y_position",
            )
            for row_number, col in lane.items():
                Helper.printc(f"{row_number=}", end=":\n", show_level="y_position")
                row_idx = int(row_number.replace("row", "")) - 1
                for col_idx, item in enumerate(col):
                    if item is not None:
                        item.y = (
                            this_lane.y
                            + (Configs.LANE_SHAPE_TOP_MARGIN)
                            + (
                                row_idx
                                * (Configs.BOX_HEIGHT + Configs.VSPACE_BETWEEN_SHAPES)
                            )
                        )

                        Helper.printc(
                            f"    {item.name=}, {row_idx=}, {col_idx+1=}, {item.x=}, {item.y=}",
                            show_level="y_position",
                        )
                        item.set_draw_position(self.__painter)
                    else:
                        Helper.printc("    {'None'}", show_level="y_position")
            self.lane_max_width = max(self.lane_max_width, this_lane.width)
            Helper.printc("", show_level="y_position")

    def _set_draw_position(self) -> tuple:
        """Set the draw position for the process map"""
        ### Set process map title
        self._title.set_draw_position(
            Configs.SURFACE_LEFT_MARGIN, Configs.SURFACE_TOP_MARGIN, self.__painter
        )

        ### Put shapes into grid
        self._layout_grid.set_grid(self._pools)
        self._layout_grid.print_grid()

        Helper.printc(
            "~~~ Calculating pool and lane width and height...", show_level="pool_lane"
        )
        x_pos, y_pos = (
            0,
            self._title.y + self._title.height + Configs.VSPACE_BETWEEN_TITLE_AND_POOL,
        )
        for pool in self._pools:
            for lane in pool.lanes:
                x_pos, y_pos, _, _ = lane.set_draw_position(
                    x_pos, y_pos, self._layout_grid
                )

            y_pos += Configs.VSPACE_BETWEEN_POOLS

            first_lane_y = pool.lanes[0].y

            pool.set_draw_position(
                Configs.SURFACE_LEFT_MARGIN, first_lane_y, self.__painter
            )

        ### Set shape x position
        # start_shape = self._find_start_shape()
        self._set_shape_x_position()

        ### Set shape y position
        self._set_shape_y_position()

        ### Set process map footer
        if self._footer is not None:
            self._footer.set_draw_position(
                Configs.SURFACE_LEFT_MARGIN,
                y_pos + Configs.VSPACE_BETWEEN_POOL_AND_FOOTER,
                self.__painter,
            )
            self.height = (
                self._footer.y + self._footer.height + Configs.SURFACE_BOTTOM_MARGIN
            )
        else:
            self.height = (
                y_pos
                + Configs.VSPACE_BETWEEN_POOL_AND_FOOTER
                + Configs.SURFACE_BOTTOM_MARGIN
            )

        self.width = (
            Configs.SURFACE_LEFT_MARGIN
            + Configs.POOL_TEXT_WIDTH
            + self.lane_max_width
            + Configs.SURFACE_LEFT_MARGIN
        )

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
            if len(pool.lanes) > 0 and len(pool.lanes[0].shapes) == 0:
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
                    self._replace_signal_element(lane, index, shape)
                    self._replace_conditional_element(lane, index, shape)
                    self._replace_message_element(lane, index, shape)

        ### Set the draw position of pools, lanes, shapes and connections
        self._set_draw_position()

        ### Draw the process map
        self._title.draw()

        all_shapes = self._layout_grid.get_all_shapes()

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
                        Helper.printc(
                            f"Drawing shape for ({pool.name}, {lane.name})",
                            34,
                            show_level="draw",
                        )
                        lane.draw_shape()

                    ### Finally draw the connections between the shapes
                    for lane in pool.lanes:
                        lane.draw_connection(all_shapes)

        if self._footer is not None:
            self._footer.draw()

        if self.auto_size is True:
            self.__painter.set_surface_size(self.width, self.height)

    def _replace_message_element(self, lane, index, shape):
        if type(shape) == Message:
            ### Check if the signal is a start signal. i.e it has no connection from
            if len(shape.connection_to) > 0 and len(shape.connection_from) == 0:
                new_shape = self._replace_element_type(lane, shape, ElementType.MESSAGE)

            elif (  ### Check if the signal is an intermediate signal. i.e it has both connection from and to
                len(shape.connection_to) > 0 and len(shape.connection_from) > 0
            ):
                new_shape = self._replace_element_type(
                    lane, shape, ElementType.MESSAGE_INTERMEDIATE
                )
            else:  ### Check if the signal is an end signal. i.e it has no connection to
                new_shape = self._replace_element_type(
                    lane, shape, ElementType.MESSAGE_END
                )

            lane.shapes[index] = self._replace_connections(shape, new_shape)

    def _replace_conditional_element(self, lane, index, shape):
        if type(shape) == Conditional and len(shape.connection_to) > 0:
            if len(shape.connection_from) == 0:
                new_shape = self._replace_element_type(
                    lane, shape, ElementType.CONDITIONAL
                )
        
                lane.shapes[index] = self._replace_connections(shape, new_shape)
        
            elif len(shape.connection_from) > 0:
                new_shape = self._replace_element_type(
                    lane, shape, ElementType.CONDITIONAL_INTERMEDIATE
                )
                lane.shapes[index] = self._replace_connections(shape, new_shape)

    def _replace_signal_element(self, lane, index, shape):
        if type(shape) == Signal:
            ### Check if the signal is a start signal. i.e it has no connection from
            if len(shape.connection_to) > 0 and len(shape.connection_from) == 0:
                new_shape = self._replace_element_type(lane, shape, ElementType.SIGNAL)

            elif (  ### Check if the signal is an intermediate signal. i.e it has both connection from and to
                len(shape.connection_to) > 0 and len(shape.connection_from) > 0
            ):
                new_shape = self._replace_element_type(
                    lane, shape, ElementType.SIGNAL_INTERMEDIATE
                )
            else:  ### Check if the signal is an end signal. i.e it has no connection to
                new_shape = self._replace_element_type(
                    lane, shape, ElementType.SIGNAL_END
                )

            lane.shapes[index] = self._replace_connections(shape, new_shape)

    def _replace_element_type(self, lane, shape, new_shape_type: ElementType):
        event_class = globals()[new_shape_type]
        return event_class(
            shape.name,
            lane.name,
        )

    def _replace_connections(self, current_shape, new_shape):
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
            
            new_shape.connection_to[connection_index] = new_connection
        self._replace_connection_from(current_shape, new_shape)
        return new_shape

    def _replace_connection_from(self, current_shape, new_shape):
        for shape_index, shape in enumerate(current_shape.connection_from):
            for connection_to in shape.connection_to:
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
