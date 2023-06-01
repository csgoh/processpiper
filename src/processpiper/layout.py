from dataclasses import dataclass, field
from .shape import Shape
from .lane import Lane
from .helper import Helper


@dataclass
class LaneRow:
    pass


@dataclass
class PoolRow:
    pass


@dataclass
class Grid:
    _pools: list = field(init=True, default_factory=list)
    _grid: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        ### Put shapes into self._grid
        self._grid = {}
        self.set_shapes_position(None, self._find_start_shape(), 0)

    def _get_lane_by_id(self, lane_id: int) -> Lane:
        """Get a lane by its id"""
        for pool in self._pools:
            for lane in pool.lanes:
                if lane.id == lane_id:
                    return lane
        return None

    def is_same_lane(self, previous_shape: Shape, current_shape: Shape) -> bool:
        Helper.print_info(f"    {previous_shape.lane_id=}=={current_shape.lane_id=}")
        return previous_shape.lane_id == current_shape.lane_id

    def is_same_pool(self, previous_shape: Shape, current_shape: Shape) -> bool:
        return (
            self._get_lane_by_id(previous_shape.lane_id).pool_id
            == self._get_lane_by_id(current_shape.lane_id).pool_id
        )

    def set_shapes_position(
        self,
        previous_shape: Shape,
        current_shape: Shape,
        index: int = 0,
    ):
        Helper.print_info(f"Setting position for {current_shape.name}, {index=}")
        self.add_shape_to_grid(previous_shape, current_shape, index)
        for connection_index, next_connection in enumerate(current_shape.connection_to):
            Helper.print_info(
                f"    Index {connection_index} - {next_connection.target.name}"
            )
            next_shape = next_connection.target
            self.set_shapes_position(current_shape, next_shape, connection_index)

    def add_shape_to_grid(
        self, previous_shape: Shape, current_shape: Shape, index: int
    ):
        ### If previous_shape is None, it is the start shape
        if previous_shape is None:
            ### Add the start shape to the grid
            Helper.print_info(f"     {current_shape.lane_id=} {index=}")
            self.add_shape_to_lane_row(current_shape.lane_id, 1, current_shape)
        else:
            (
                previous_shape_lane_id,
                previous_shape_row_number,
                previous_shape_col_number,
            ) = self.get_shape_lane_rowcolumn(previous_shape)

            Helper.print_info(
                f"***{previous_shape_lane_id=} {previous_shape_row_number=} {previous_shape_col_number=}"
            )
            if self.is_same_lane(previous_shape, current_shape):
                # Same lane

                if index == 0:
                    Helper.print_info(f"     Same lane, {index=}, add_shape_to_lane")
                    self.add_shape_to_lane(
                        current_shape.lane_id, previous_shape_row_number, current_shape
                    )
                else:
                    Helper.print_info(
                        f"     Same lane, {index=}, add_shape_to_lane_rowcolumn"
                    )
                    self.add_shape_to_lane_rowcolumn(
                        current_shape.lane_id,
                        index + 1,
                        previous_shape_col_number + 1,
                        current_shape,
                    )
            else:
                # Same pool but different lane
                # work for different pool too
                Helper.print_info(f"     Different lane {index=}")
                if index == 0:
                    self.add_shape_to_lane(
                        current_shape.lane_id, previous_shape_row_number, current_shape
                    )
                else:
                    self.add_shape_to_lane_rowcolumn(
                        current_shape.lane_id,
                        index + 1,
                        previous_shape_col_number + 1,
                        current_shape,
                    )

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

    def add_shape_to_lane_row(self, lane_id: str, row_number: int, shape: Shape):
        if lane_id not in self._grid:
            self._grid[lane_id] = {}
        row_number = f"row{row_number}"
        if row_number not in self._grid[lane_id]:
            self._grid[lane_id][row_number] = []
        self._grid[lane_id][row_number].append(shape)

    def add_shape_to_lane_rowcolumn(
        self, lane_id: str, row_number: int, col_number: int, shape: Shape
    ):
        if lane_id not in self._grid:
            self._grid[lane_id] = {}

        row_number = f"row{row_number}"
        if row_number not in self._grid[lane_id]:
            self._grid[lane_id][row_number] = []

        # check if shape exists
        if self._grid[lane_id][row_number] is not None:
            Helper.print_info(
                f"            #{lane_id}, {row_number}, {col_number} - {shape.name}"
            )
            if col_number > len(self._grid[lane_id][row_number]):
                for _ in range(col_number - len(self._grid[lane_id][row_number]) - 1):
                    self._grid[lane_id][row_number].append(None)
                self._grid[lane_id][row_number].append(shape)
            else:
                self._grid[lane_id][row_number][col_number - 1] = shape

        ### add max columns to other lanes
        max_columns = self.get_max_column_count()
        for this_lane_id in self._grid:
            for row in self._grid[this_lane_id]:
                if len(self._grid[this_lane_id][row]) < max_columns:
                    for _ in range(max_columns - len(self._grid[this_lane_id][row])):
                        self._grid[this_lane_id][row].append(None)

    def find_shape_rowcolumn_in_lane(self, lane_id: str, shape: Shape):
        if lane_id not in self._grid:
            return None, None

        for row_number, col in self._grid[lane_id].items():
            if shape in col:
                return row_number, col.index(shape) + 1

        return None, None

    def get_column_index(self, lane_id: str, shape: Shape):
        # find shape column index
        for _, col in self._grid[lane_id].items():
            if shape in col:
                return col.index(shape) + 1

    def is_column_empty(self, lane_id: str, row_number: int, col_number: int):
        row_number = f"row{row_number}"
        for row, col in self._grid[lane_id].items():
            if row == row_number:
                if col[col_number - 1] is not None:
                    return False
        return True

    def get_shape_lane_rowcolumn(self, shape: Shape):
        for lane_id, lane in self._grid.items():
            for row, col in lane.items():
                print(f"~~~{lane_id}, {shape.name}")
                # for item in col:
                #     print(f"    ->{item.name}")
                if shape in col:
                    # get row number
                    print(f"!!!Shape in col!!!")
                    row_number = int(row.replace("row", ""))
                    return lane_id, row_number, col.index(shape) + 1
        return None, None, None

    def add_shape_to_lane(self, lane_id: str, row_number: int, current_shape: Shape):
        print("calling add_shape_to_lane------------")
        if lane_id is not None:
            print("lane_id is not None")
            col_number = self.get_next_column(lane_id, row_number)

            self.add_shape_to_lane_rowcolumn(
                lane_id, row_number, col_number, current_shape
            )
        else:
            raise ValueError("lane_id must be provided")

    def add_shape_to_same_lane(self, previous_shape: Shape, current_shape: Shape):
        lane_id, row_number, _ = self.get_shape_lane_rowcolumn(previous_shape)

        if lane_id is not None:
            col_number = self.get_next_column(lane_id, row_number)

            self.add_shape_to_lane_rowcolumn(
                lane_id, row_number, col_number, current_shape
            )

    def add_shape_to_same_lane_next_row(
        self, previous_shape: Shape, current_shape: Shape
    ):
        lane_id, row_number, _ = self.get_shape_lane_rowcolumn(previous_shape)
        if lane_id is not None:
            col_number = self.get_next_column(lane_id, row_number)

            next_row_number = row_number + 1
            while True:
                if self.is_column_empty(lane_id, next_row_number, col_number):
                    self.add_shape_to_lane_rowcolumn(
                        lane_id, next_row_number, col_number, current_shape
                    )
                    break

                next_row_number += 1

    def add_shape_to_diff_lane(self, previous_shape: Shape, current_shape: Shape):
        ...

    def add_shape_to_diff_lane_next_column(
        self, lane_id: str, previous_shape: Shape, current_shape: Shape
    ):
        ...

    def get_next_column(self, lane_id: str, row_number: int) -> int:
        # get next None column
        if lane_id not in self._grid:
            return 1

        # find out the last column that is not None
        max_columns = self.get_max_column_count()
        print(f"------->max_columns: {max_columns}")
        last_column = 0
        row_number = f"row{row_number}"
        for col_number in range(max_columns + 1):
            for row, col in self._grid[lane_id].items():
                if row == row_number:
                    if col[col_number - 1] is not None:
                        last_column = col_number
        return last_column + 1

    def format_item(self, item, repeat: bool = False):
        item = str(item)
        fixed_length = 20

        # item = "" if item == "None" else item

        if repeat is False:
            spaces = " " * fixed_length
        else:
            spaces = item * fixed_length

        if item == "None":
            return spaces + "|"

        return item + spaces[: fixed_length - len(item)] + "|"

    def get_max_column_count(self):
        max_columns = 0
        # calculate max number of columns
        for _, lane in self._grid.items():
            for _, col in lane.items():
                if len(col) > max_columns:
                    max_columns = len(col)
        return max_columns

    def print_header(
        self,
    ):
        max_columns = self.get_max_column_count()
        # calculate max number of columns
        for _, lane in self._grid.items():
            for _, col in lane.items():
                if len(col) > max_columns:
                    max_columns = len(col)

        for _, lane in self._grid.items():
            Helper.print_info(self.format_item("ROW \ COL"), end="")
            for i in range(max_columns):
                Helper.print_info(f"{self.format_item(i+1)}", end="")
            Helper.print_info("")
            for _ in range(max_columns + 1):
                Helper.print_info(self.format_item("-", True), end="")
            Helper.print_info("")
            break

    def print_grid(self):
        for lane_id, lane in self._grid.items():
            Helper.print_info(lane_id)
            self.print_header()
            for row_number, col in lane.items():
                Helper.print_info(f"{self.format_item(row_number)}", end="")
                for item in col:
                    if item is not None:
                        Helper.print_info(f"{self.format_item(item.name)}", end="")
                    else:
                        Helper.print_info(f"{self.format_item('None')}", end="")

                Helper.print_info("")
                # result = row_number + ' '.join(formatted_items)
            Helper.print_info("")
