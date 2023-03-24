from dataclasses import dataclass, field
from processmapper.lane import Lane
from processmapper.pool import Pool
from processmapper.painter import Painter
from processmapper.shape import Shape
from processmapper.title import Title
from processmapper.footer import Footer
import processmapper.constants as Configs
import processmapper.helper as Helper


@dataclass
class ProcessMap:
    _title: Title = field(init=False)
    _footer: Footer = field(init=False, default=None)
    _pools: list = field(init=False, default_factory=list)

    title: str = field(init=True, default="<Process Map Title>")
    width: int = field(init=True, default=3200)
    height: int = field(init=True, default=3200)
    auto_size: bool = field(init=True, default=True)
    colour_theme: str = field(init=True, default="DEFAULT")
    # __painter: Painter = field(init=False)
    next_shape_x: int = field(init=False, default=0)

    lane_y_pos: int = field(init=False, default=0)
    lane_max_width: int = field(init=False, default=0)

    def __post_init__(self):
        self.__painter = Painter(self.width, self.height)
        self.__set_colour_theme(self.colour_theme)
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

    ### TO DO: modify the method to support pool and lane
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
        if font == "":
            font = self.__painter.footer_font
        if font_size == 0:
            font_size = self.__painter.footer_font_size
        if font_colour == "":
            font_colour = self.__painter.footer_font_colour

        self._footer = Footer(footer_name, font, font_size, font_colour)

    def get_current_x_position(self) -> int:
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
        for pool in self._pools:
            for lane in pool._lanes:
                for shape in lane.shapes:
                    ### If the shape has no connection_from, it is the start shape
                    print(f"{shape.name} - {len(shape.connection_from)}")
                    if len(shape.connection_from) == 0:
                        # print(
                        #     f"Found start shape: <{shape.name}>, lane_id: {shape.lane_id}"
                        # )
                        return shape
        # print(f"Could not find start shape")
        return None

    def get_lane_by_id(self, id: int) -> Lane:
        for pool in self._pools:
            for lane in pool._lanes:
                if lane.id == id:
                    return lane
        return None

    def get_pool_by_name(self, name: str) -> Pool:
        for pool in self._pools:
            if pool.name == name:
                return pool
        return None

    ### Check how many rows of shapes are in the lane
    def check_lane_shape_row_count(self, shape: Shape) -> int:
        row_count = 0
        lane = self.get_lane_by_id(shape.lane_id)
        if len(shape.connection_to) <= 1:
            return 1
        else:
            for connection in shape.connection_to:
                target_shape = connection.target
                if shape.lane_id == target_shape.lane_id:
                    row_count += 1

        return row_count

    def set_shape_x_position(
        self,
        previous_shape: Shape,
        current_shape: Shape,
        index: int = 0,
        x_pos: int = 0,
    ):
        current_lane = self.get_lane_by_id(current_shape.lane_id)
        if index == 0:
            current_pool = self.get_pool_by_name(current_shape.pool_name)
            if previous_shape is not None:
                if previous_shape.pool_name == current_shape.pool_name:
                    # print(f"pool name: {current_shape.pool_name}")
                    if previous_shape.lane_id == current_shape.lane_id:
                        current_shape.x = self.get_next_x_position()
                        print(f"          same pool same lane")
                    else:
                        current_shape.x = self.get_next_x_position()
                        print(f"          same pool diff lane")
                else:
                    previous_pool = self.get_pool_by_name(previous_shape.pool_name)
                    current_shape.x = self.get_next_x_position()
                    print(f"          diff pool")
            else:
                current_shape.x = self.get_next_x_position()
                print(f"          previous = none")
        else:
            ### If previous shape is connecting to multiple shapes,
            ### the x position of the shape is the same as the previous shape
            current_shape.x = x_pos
        current_lane.width = max(current_lane.width, current_shape.x + 100)
        print(
            f"          x={current_shape.x}, y={current_shape.y}, w={current_shape.width}, [{current_lane.name}]"
        )

        self.lane_max_width = max(self.lane_max_width, current_lane.width)
        current_shape.x_pos_traversed = True

        current_lane.shape_row_count = max(
            current_lane.shape_row_count, self.check_lane_shape_row_count(current_shape)
        )

        preserved_x_pos = 0
        for index, next_connection in enumerate(current_shape.connection_to):
            next_shape = next_connection.target
            if next_shape.x_pos_traversed is True:
                continue
            print(f"    |{index}| - <{next_shape.name}>")
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
        lane = self.get_lane_by_id(shape.lane_id)
        if index == 0:
            ### If previous shape is connecting to one shape,
            ### the y position of the shape is the same as the previous shape
            shape.y = lane.get_current_y_position()
        else:
            ### Otherwise, the y position of the shape is the next y position
            shape.y = lane.get_next_y_position()

        shape.set_draw_position(self.__painter)
        # print(f"<{shape.name}>, lane_id={shape.lane_id}, x={shape.x}, y={shape.y}")

        shape.y_pos_traversed = True

        # for shape in lane.shapes:
        for index, connection in enumerate(shape.connection_to):
            next_shape = connection.target
            if next_shape.y_pos_traversed is True:
                continue
            # print(f"    <{shape.name}>, next_shape: {next_shape.name}, index: {index}")
            self.set_shape_y_position(next_shape, index)

    def set_draw_position(self, painter: Painter) -> tuple:
        ### Set process map title
        self._title.set_draw_position(
            Configs.SURFACE_LEFT_MARGIN, Configs.SURFACE_TOP_MARGIN, painter
        )

        Helper.printc("***Setting x position...")
        start_shape = self.find_start_shape()

        self.set_shape_x_position(None, start_shape, 0, 0)

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
                lane.height = (
                    (lane.shape_row_count * 60)
                    + ((lane.shape_row_count - 1) * Configs.VSPACE_BETWEEN_SHAPES)
                    + Configs.LANE_SHAPE_TOP_MARGIN
                    + Configs.LANE_SHAPE_BOTTOM_MARGIN
                )
                # print(
                #     f"lane.height: {lane.height} = ({lane.shape_row_count} * 60) + ({lane.shape_row_count} - 1) * {Configs.VSPACE_BETWEEN_SHAPES} + {Configs.LANE_SHAPE_TOP_MARGIN} + {Configs.LANE_SHAPE_BOTTOM_MARGIN}"
                # )
                y = lane.y + lane.height + Configs.VSPACE_BETWEEN_LANES
                # print(f"{x} = {lane.y} + {lane.height} + {lane.VSPACE_BETWEEN_LANES}")

            y += Configs.VSPACE_BETWEEN_POOLS

            first_lane_y = pool._lanes[0].y

            pool.set_draw_position(Configs.SURFACE_LEFT_MARGIN, first_lane_y, painter)

        Helper.printc(f"***Setting y position...")
        self.set_shape_y_position(start_shape)

        ### Set process map footer
        if self._footer != None:
            self._footer.set_draw_position(
                Configs.SURFACE_LEFT_MARGIN,
                y + Configs.VSPACE_BETWEEN_POOL_AND_FOOTER,
                painter,
            )

        self.width = (
            Configs.SURFACE_LEFT_MARGIN
            + Configs.POOL_TEXT_WIDTH
            + self.lane_max_width
            + Configs.SURFACE_LEFT_MARGIN
        )

        self.height = (
            self._footer.y + self._footer.height + Configs.SURFACE_BOTTOM_MARGIN
        )

    def draw(self) -> None:
        # self.__painter = Painter(self.width, self.height)

        # Helper.printc(f"Set draw position...")
        self.set_draw_position(self.__painter)

        # Helper.printc(f"Start drawing...")
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
            # print(f"Auto sizing..")
            self.__painter.set_surface_size(self.width, self.height)

    def __set_colour_theme(self, palette: str) -> None:
        """This method sets the colour palette"""
        self.__painter.set_colour_theme(palette)

    def save(self, filename: str) -> None:
        self.__painter.save_surface(filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def print(self) -> None:
        for lane in self._lanes:
            print(f"[{lane.text}, number of elements: {len(lane.shapes)}]")
            for shape in lane.shapes:
                print(f'    ("{shape.text}", type: {shape.__class__.__name__})')
                for connection in shape.connection_to:
                    print(f"        ->: {connection.target.text}")
                for connection in shape.connection_from:
                    print(f"        <-: {connection.text}")
