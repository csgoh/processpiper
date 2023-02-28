from dataclasses import dataclass, field
from processmapper.lane import Lane
from processmapper.pool import Pool
from processmapper.painter import Painter
from processmapper.shape import Shape
from processmapper.title import Title
import processmapper.constants as Configs
import processmapper.helper as Helper


@dataclass
class ProcessMap:
    _title: Title = field(init=False)
    _pools: list = field(init=False, default_factory=list)

    title: str = field(init=True, default="<Process Map Title>")
    width: int = field(init=True, default=1200)
    height: int = field(init=True, default=800)
    colour_theme: str = field(init=True, default="DEFAULT")
    __painter: Painter = field(init=False)

    lane_y_pos: int = field(init=False, default=0)
    lane_max_width: int = field(init=False, default=0)

    def __post_init__(self):
        self._title = Title(self.title)
        self._title.name = self.title

    def add_pool(self, pool_name: str) -> Pool:
        pool = Pool(pool_name)
        self._pools.append(pool)
        return pool

    ### TO DO: modify the method to support pool and lane
    def add_lane(self, lane_name: str) -> Lane:
        pool = self.add_pool("Default Pool")
        lane = pool.add_lane(lane_name)
        return lane

    # def get_surface_size(self) -> tuple:
    #     x, y = 0, 0
    #     if self._lanes:
    #         last_y_pos = 0
    #         for lane in self._lanes:
    #             ### Calculate the x and y position of the lane and shapes in the lane
    #             x, y, w, h = lane.set_draw_position(x, last_y_pos, self.__painter)
    #             self.width = max(self.width, x + w)
    #             self.height = max(self.height, y + h)
    #             last_y_pos = y + h + Lane.VSPACE_BETWEEN_LANES

    #     # self.__painter.set_surface_size(self.width, self.height)
    #     return self.width, self.height

    def find_start_shape(self) -> Shape:
        for pool in self._pools:
            for lane in pool._lanes:
                for shape in lane.shapes:
                    ### If the shape has no connection_from, it is the start shape
                    # print(f"{shape.name} - {len(shape.connection_from)}")
                    if len(shape.connection_from) == 0:
                        print(
                            f"Found start shape: <{shape.name}>, lane_id: {shape.lane_id}"
                        )
                        return shape
        print(f"Could not find start shape")
        return None

    def get_lane_by_id(self, id: int) -> Lane:
        for pool in self._pools:
            for lane in pool._lanes:
                if lane.id == id:
                    return lane
        return None

    ### Check how many rows of shapes are in the lane
    def check_lane_shape_row_count(self, shape: Shape) -> int:
        row_count = 0
        lane = self.get_lane_by_id(shape.lane_id)
        if len(shape.connection_to) <= 1:
            return 1
        else:
            for target_shape in shape.connection_to:
                if shape.lane_id == target_shape.lane_id:
                    row_count += 1

        return row_count

    def set_shape_x_position(self, shape: Shape, index: int = 0, x_pos: int = 0):
        lane = self.get_lane_by_id(shape.lane_id)
        if index == 0:
            shape.x = lane.get_next_x_position()
        else:
            ### If previous shape is connecting to multiple shapes,
            ### the x position of the shape is the same as the previous shape
            # shape.x = lane.get_current_x_position()
            shape.x = x_pos
        lane.width = max(lane.width, shape.x + 100)
        print(f"          x={shape.x}, y={shape.y}, w={shape.width}, [{lane.name}]")

        self.lane_max_width = max(self.lane_max_width, lane.width)
        shape.x_pos_traversed = True

        lane.shape_row_count = max(
            lane.shape_row_count, self.check_lane_shape_row_count(shape)
        )
        # print(
        #     f"            >>[{lane.name}], id={lane.id}, row_count={lane.shape_row_count}"
        # )

        preserved_x_pos = 0
        for index, next_shape in enumerate(shape.connection_to):
            if next_shape.x_pos_traversed is True:
                # print(f", -Skipped-")
                # print(f"")
                continue
            # lane.shape_row_count = max(lane.shape_row_count, index + 1)
            print(f"    |{index}| - <{next_shape.name}>")
            if index == 0:
                preserved_x_pos = self.set_shape_x_position(
                    next_shape, index, preserved_x_pos
                )
            else:
                self.set_shape_x_position(next_shape, index, preserved_x_pos)

        return shape.x

    def set_shape_y_position(self, shape: Shape, index: int = 0):
        lane = self.get_lane_by_id(shape.lane_id)
        if index == 0:
            ### If previous shape is connecting to one shape,
            ### the y position of the shape is the same as the previous shape
            shape.y = lane.get_current_y_position()
        else:
            ### Otherwise, the y position of the shape is the next y position
            shape.y = lane.get_next_y_position()
            if shape.lane_id == 2:
                print(f"shape.y: {shape.y}")

        shape.set_draw_position(self.__painter)
        print(f"<{shape.name}>, lane_id={shape.lane_id}, x={shape.x}, y={shape.y}")

        shape.y_pos_traversed = True

        # for shape in lane.shapes:
        for index, next_shape in enumerate(shape.connection_to):
            if next_shape.y_pos_traversed is True:
                # print(f", -Skipped-")
                # print(f"")
                continue
            print(f"    <{shape.name}>, next_shape: {next_shape.name}, index: {index}")
            # print(f"({index}) - <{next_shape.text}>", end="")
            self.set_shape_y_position(next_shape, index)

    def set_draw_position(self, painter: Painter) -> tuple:
        ### Set process map title
        self._title.set_draw_position(
            Configs.SURFACE_LEFT_MARGIN, Configs.SURFACE_TOP_MARGIN, painter
        )

        Helper.printc("***Setting x position...")
        start_shape = self.find_start_shape()

        self.set_shape_x_position(start_shape, 0, 0)

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

        for pool in self._pools:
            print(f"({pool.name})")
            for lane in pool._lanes:
                print(
                    f"      [{lane.name}], row count: {lane.shape_row_count}, x={lane.x}, y={lane.y}, mw={self.lane_max_width}, w={self.width}, h={lane.height}"
                )
                for shape in lane.shapes:
                    print(f"            <{shape.name}>: x={shape.x}, y={shape.y}")

    def draw(self) -> None:
        self.__painter = Painter(self.width, self.height)

        self.__set_colour_palette(self.colour_theme)

        ### Determine the size of the process map
        # self.width, self.height = self.get_surface_size()

        Helper.printc(f"Set draw position...")
        self.set_draw_position(self.__painter)

        Helper.printc(f"Start drawing...")
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

    def __set_colour_palette(self, palette: str) -> None:
        """This method sets the colour palette"""
        # self.__painter.set_colour_palette(palette)

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
                    print(f"        ->: {connection.text}")
                for connection in shape.connection_from:
                    print(f"        <-: {connection.text}")
