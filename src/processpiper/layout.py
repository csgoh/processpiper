from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table
from .shape import Shape
from .helper import Helper


@dataclass
class Grid:
    _pools: list = field(init=False, default_factory=list)
    _grid: dict = field(init=False, default_factory=dict)

    def set_grid(self, pools: list):
        """Set the grid for the process map"""

        self._pools = pools
        self._grid = {}
        self.set_shapes_position(None, self._find_start_shape(), 0)

    def get_grid_items(self):
        """Get the grid items"""

        return self._grid.items()

    def is_same_lane(self, previous_shape: Shape, current_shape: Shape) -> bool:
        """Check if the previous shape and current shape are in the same lane"""

        return previous_shape.lane_id == current_shape.lane_id

    def is_same_pool(self, previous_shape: Shape, current_shape: Shape) -> bool:
        """Check if the previous shape and current shape are in the same pool"""
        return previous_shape.pool_name == current_shape.pool_name

    def set_shapes_position(
        self,
        previous_shape: Shape,
        current_shape: Shape,
        index: int = 0,
    ):
        """Set the position of the shapes in the grid"""
        if current_shape.grid_traversed is True:
            Helper.printc(
                f"[orange4]{current_shape.name} is already traversed[/]",
                show_level="layout_grid",
            )
            return
        Helper.printc(
            f"Traversing [red]{current_shape.name}[/]", show_level="layout_grid"
        )
        current_shape.grid_traversed = True
        self.add_shape_to_grid(previous_shape, current_shape, index)
        for connection_index, next_connection in enumerate(current_shape.connection_to):
            next_shape = next_connection.target
            Helper.printc(
                f"    [dodger_blue1]{connection_index}: {current_shape.name} -> {next_shape.name}[/]",
                show_level="layout_grid",
            )
            self.set_shapes_position(current_shape, next_shape, connection_index)
        Helper.printc(
            f"Done traversing [:thumbsup: {current_shape.name}]",
            show_level="layout_grid",
        )

    def add_shape_to_grid(
        self, previous_shape: Shape, current_shape: Shape, index: int
    ):
        """Add the shape to the grid"""
        # ---If previous_shape is None, it is the start shape---
        if previous_shape is None:
            # ---Add the start shape to the grid---
            Helper.printc(
                f"    ==>Start adding [{current_shape.name}] to grid (append)",
                show_level="layout_grid",
            )
            self.add_shape_to_lane_row(current_shape.lane_id, 1, current_shape)
        else:
            (
                _,
                previous_shape_row_number,
                previous_shape_col_number,
            ) = self.get_shape_lane_rowcolumn(previous_shape)

            if self.is_same_lane(previous_shape, current_shape):
                # Same lane

                if index == 0:
                    Helper.printc(
                        (
                            "        ==>Same lane (row 0): ",
                            f"add_shape_to_lane [{current_shape.name}],",
                            f" {previous_shape_row_number=}",
                        ),
                        show_level="layout_grid",
                    )
                    self.add_shape_to_lane(
                        current_shape.lane_id, previous_shape_row_number, current_shape
                    )
                else:  ### Next row
                    Helper.printc(
                        f"        ==>Same lane (next row): add_shape_to_lane_rowcolumn [{current_shape.name}, {previous_shape_col_number}]",
                        show_level="layout_grid",
                    )
                    if self.is_column_empty(
                        current_shape.lane_id,
                        previous_shape_row_number,
                        previous_shape_col_number,
                    ):
                        Helper.printc("Is empty", 34, show_level="layout_grid")
                        self.add_shape_to_lane_rowcolumn(
                            current_shape.lane_id,
                            previous_shape_row_number,
                            previous_shape_col_number,
                            current_shape,
                        )
                    else:
                        Helper.printc("Not empty", 34, show_level="layout_grid")
                        Helper.printc(
                            f"Adding shape to {index + 1}, {previous_shape_col_number}",
                            show_level="layout_grid",
                        )
                        self.add_shape_to_lane_rowcolumn(
                            current_shape.lane_id,
                            index + 1,
                            # previous_shape_col_number + 1,
                            previous_shape_col_number,
                            current_shape,
                        )
            elif index == 0:
                if self.is_same_pool(previous_shape, current_shape):
                    Helper.printc(
                        f"        ==> {index=}, Same pool, diff lane: add_shape_to_lane [{current_shape.name}], {previous_shape_row_number+1}",
                        show_level="layout_grid",
                    )
                    self.add_shape_to_lane_rowcolumn(
                        current_shape.lane_id,
                        index + 1,
                        previous_shape_col_number + 1,
                        current_shape,
                    )
                else:
                    # Different pool
                    Helper.printc(
                        f"        ==> {index=}, Diff pool: add_shape_to_lane_rowcolumn [{current_shape.name}, {previous_shape_col_number=}]",
                        show_level="layout_grid",
                    )
                    self.add_shape_to_lane_rowcolumn(
                        current_shape.lane_id,
                        index + 1,
                        previous_shape_col_number,
                        current_shape,
                    )
            else:
                if self.is_same_pool(previous_shape, current_shape):
                    Helper.printc(
                        f"        ==> {index=}, Same pool, diff lane: add_shape_to_lane_rowcolumn [{current_shape.name}], {previous_shape_col_number=}",
                        show_level="layout_grid",
                    )
                else:
                    # Different pool
                    Helper.printc(
                        f"        ==> {index=}, Diff pool: add_shape_to_lane_rowcolumn [{current_shape.name}, {previous_shape_col_number=}]",
                        show_level="layout_grid",
                    )

                self.add_shape_to_lane_rowcolumn(
                    current_shape.lane_id,
                    index,
                    previous_shape_col_number,
                    current_shape,
                )

    def _find_start_shape(self) -> Shape:
        """Find the start shape in the process map"""
        for pool in self._pools:
            for lane in pool.lanes:
                for shape in lane.shapes:
                    ### If the shape has no connection_from, it is the start shape
                    Helper.printc(
                        f"{shape.name} - {len(shape.connection_from)}",
                        show_level="layout_grid",
                    )
                    if len(shape.connection_from) == 0:
                        return shape
        return None

    def get_all_shapes(self) -> list:
        """Get all the shapes points"""
        shapes = []
        for _, lane in self._grid.items():
            for _, col in lane.items():
                for item in col:
                    if item is not None:
                        shapes.append(item)
        return shapes

    def add_shape_to_lane_row(self, lane_id: str, row_number: int, shape: Shape):
        """Add the shape to the lane row"""
        if lane_id not in self._grid:
            self._grid[lane_id] = {}
        row_number = f"row{row_number}"
        if row_number not in self._grid[lane_id]:
            self._grid[lane_id][row_number] = []
        Helper.printc(
            f"            ### ({shape.name=}), {lane_id=}, {row_number=}",
            36,
            show_level="layout_grid",
        )
        self._grid[lane_id][row_number].append(shape)

    def add_shape_to_lane_rowcolumn(
        self, lane_id: str, row_number: int, col_number: int, shape: Shape
    ):
        """Add the shape to the lane row column"""
        if lane_id not in self._grid:
            self._grid[lane_id] = {}

        row_number = f"row{row_number}"
        if row_number not in self._grid[lane_id]:
            self._grid[lane_id][row_number] = []

        # check if shape exists
        if self._grid[lane_id][row_number] is not None:
            if col_number > len(self._grid[lane_id][row_number]):
                for _ in range(col_number - len(self._grid[lane_id][row_number]) - 1):
                    self._grid[lane_id][row_number].append(None)
                self._grid[lane_id][row_number].append(shape)
            elif col_number == 1:
                self._grid[lane_id][row_number].append(shape)
            else:
                if self._grid[lane_id][row_number][col_number - 1] is None:
                    self._grid[lane_id][row_number][col_number - 1] = shape
                else:
                    self._grid[lane_id][row_number].append(shape)

        Helper.printc(
            f"            ### {shape.name=}, {lane_id=}, {row_number=}, {col_number=}",
            36,
            show_level="layout_grid",
        )

        ### add max columns to other lanes
        max_columns = self.get_max_column_count()
        for this_lane_id in self._grid:
            for row in self._grid[this_lane_id]:
                if len(self._grid[this_lane_id][row]) < max_columns:
                    for _ in range(max_columns - len(self._grid[this_lane_id][row])):
                        self._grid[this_lane_id][row].append(None)

    def find_shape_rowcolumn_in_lane(self, lane_id: str, shape: Shape):
        # sourcery skip: use-next
        """Find the shape row and column in the lane"""
        if lane_id not in self._grid:
            return None, None

        for row_number, col in self._grid[lane_id].items():
            if shape in col:
                return row_number, col.index(shape) + 1

        return None, None

    def get_column_index(self, lane_id: str, shape: Shape):
        """Get the column index of the shape in the lane"""
        # find shape column index
        for _, col in self._grid[lane_id].items():
            if shape in col:
                return col.index(shape) + 1

    def is_column_empty(self, lane_id: str, row_number: int, col_number: int):
        # sourcery skip: use-any
        """Check if the column is empty"""

        row_number = f"row{row_number}"
        for row, col in self._grid[lane_id].items():
            if row == row_number and col[col_number - 1] is not None:
                shape = col[col_number - 1]
                Helper.printc(f"            ### {shape.name}", show_level="layout_grid")
                return False
        return True

    def get_shape_lane_rowcolumn(self, shape: Shape):
        """Get the shape lane, row and column"""
        for lane_id, lane in self._grid.items():
            for row, col in lane.items():
                if shape in col:
                    # get row number
                    row_number = int(row.replace("row", ""))
                    return lane_id, row_number, col.index(shape) + 1
        return None, None, None

    def add_shape_to_lane(self, lane_id: str, row_number: int, current_shape: Shape):
        """Add the shape to the lane"""
        if lane_id is not None:
            col_number = self.get_next_column(lane_id, row_number)
            # col_number = self.get_next_empty_column(lane_id, row_number)
            Helper.printc(
                f"            ### {lane_id=}, {row_number=}, {col_number=}",
                33,
                show_level="layout_grid",
            )
            self.add_shape_to_lane_rowcolumn(
                lane_id, row_number, col_number, current_shape
            )
        else:
            raise ValueError("lane_id must be provided")

    def add_shape_to_same_lane(self, previous_shape: Shape, current_shape: Shape):
        """Add the shape to the same lane"""
        lane_id, row_number, _ = self.get_shape_lane_rowcolumn(previous_shape)

        if lane_id is not None:
            col_number = self.get_next_column(lane_id, row_number)

            self.add_shape_to_lane_rowcolumn(
                lane_id, row_number, col_number, current_shape
            )

    def add_shape_to_same_lane_next_row(
        self, previous_shape: Shape, current_shape: Shape
    ):
        """Add the shape to the same lane next row"""
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

    def get_next_column(self, lane_id: str, row_number: int) -> int:
        """Get the next column"""
        # get next None column
        if lane_id not in self._grid:
            return 1

        # find out the last column that is not None
        max_columns = self.get_max_column_count()
        last_column = 0
        row_number = f"row{row_number}"
        for col_number in range(max_columns + 1):
            for row, col in self._grid[lane_id].items():
                if row == row_number and col[col_number - 1] is not None:
                    last_column = col_number
        return last_column + 1

    def format_itemX(self, item, repeat: bool = False):
        # sourcery skip: assign-if-exp, simplify-boolean-comparison
        """Format the item"""
        # get the first 20 characters from item
        item = str(item)[:20]
        fixed_length = 20

        if repeat is False:
            spaces = " " * fixed_length
        else:
            spaces = item * fixed_length

        if item == "None":
            return f"{spaces}|"

        return item + spaces[: fixed_length - len(item)] + "|"

    def format_item(self, item, repeat: bool = False):
        # sourcery skip: assign-if-exp, simplify-boolean-comparison
        """Format the item"""
        # get the first 20 characters from item
        item = str(item)[:20]
        fixed_length = 20

        if repeat is False:
            spaces = " " * fixed_length
        else:
            spaces = item * fixed_length

        if item == "None":
            return f"{spaces}"

        return item + spaces[: fixed_length - len(item)]

    def get_max_column_count(self):
        """Get the max number of columns"""
        max_columns = 0
        # calculate max number of columns
        for _, lane in self._grid.items():
            for _, col in lane.items():
                if len(col) > max_columns:
                    max_columns = len(col)
        return max_columns

    def get_lane_row_count(self, lane_id: str):
        """Get the lane row count"""
        return len(self._grid[lane_id])

    def print_headerX(
        self,
    ):
        """Print the header"""
        max_columns = self.get_max_column_count()
        # calculate max number of columns
        for _, lane in self._grid.items():
            for _, col in lane.items():
                if len(col) > max_columns:
                    max_columns = len(col)

        for _, lane in self._grid.items():
            Helper.printc(
                self.format_item(r"ROW \ COL"),
                end="",
                color=33,
                show_level="layout_grid",
            )
            for i in range(max_columns):
                Helper.printc(
                    f"{self.format_item(i+1)}",
                    end="",
                    color=33,
                    show_level="layout_grid",
                )
            Helper.printc("", show_level="layout_grid")
            for _ in range(max_columns + 1):
                Helper.printc(
                    self.format_item("-", True),
                    end="",
                    color=33,
                    show_level="layout_grid",
                )
            Helper.printc("", show_level="layout_grid")
            break

    def print_header(self, table: Table):
        max_columns = self.get_max_column_count()
        for _, lane in self._grid.items():
            for _, col in lane.items():
                if len(col) > max_columns:
                    max_columns = len(col)

        for _, lane in self._grid.items():
            table.add_column("ROW \ COL")
            for i in range(max_columns):
                table.add_column(self.format_item(i + 1))
            break

    def print_grid(self):
        if Helper.show_layout_grid is True:
            for lane_id, lane in self._grid.items():
                Helper.printc(f"{lane_id=}", color=33, show_level="layout_grid")
                console = Console()
                table = Table(
                    show_header=True, header_style="bold magenta", show_lines=True
                )
                self.print_header(table)
                for row_number, col in lane.items():
                    row_data = [self.format_item(row_number)]
                    for item in col:
                        if item is not None:
                            row_data.append(self.format_item(item.name))
                        else:
                            row_data.append(self.format_item("None"))

                    table.add_row(*row_data)

                console.print(table)