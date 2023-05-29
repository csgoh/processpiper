

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
    _lanes: list = field(init=False, default_factory=list)
    _shapes: list = field(init=False, default_factory=list)
    _layout_grid: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        ### Put shapes into Grid
        self.set_shape_grid_position(None, self._find_start_shape())
        
    def add_to_same_lane(self, previous_shape: Shape, current_shape: Shape):
        """Add a shape to the same lane"""
        this_lane = self._get_lane_by_id(current_shape.lane_id)
        if this_lane.id in self._layout_grid:
            self._layout_grid[this_lane.id].append(current_shape)
        else:
            self._layout_grid[this_lane.id] = [current_shape]
        
        ### Append None to other array in _layout_grid
        for lane_id, grid in self._layout_grid.items():
            if lane_id != this_lane.id:
                grid.append(None)
            
    def add_to_different_lane(self, previous_shape: Shape, current_shape: Shape):
        """Add a shape to a different lane"""
        previous_lane = self._get_lane_by_id(previous_shape.lane_id)
        current_lane = self._get_lane_by_id(current_shape.lane_id)
        if previous_lane.id in self._layout_grid:
            self._layout_grid[previous_lane.id].append(previous_shape)
        else:
            self._layout_grid[previous_lane.id] = [previous_shape]
        if current_lane.id in self._layout_grid:
            self._layout_grid[current_lane.id].append(current_shape)
        else:
            self._layout_grid[current_lane.id] = [current_shape]

    def set_shape_grid_position(self, previous_shape: Shape, current_shape: Shape):
        if previous_shape is not None:
            if previous_shape.pool_name == current_shape.pool_name:
                if previous_shape.lane_id == current_shape.lane_id: # same pool, same lane
                    self.add_to_same_lane(previous_shape, current_shape)
                else: # same pool, different lane
                    self.add_to_different_lane(previous_shape, current_shape)
            else: # different pool, different lane
                ...
        else: # First shape
            ...

    def _get_lane_by_id(self, lane_id: int) -> Lane:
        """Get a lane by its id"""
        for pool in self._pools:
            for lane in pool.lanes:
                if lane.id == lane_id:
                    return lane
        return None

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

    def print(self):
        Helper.print_info("-------------Printing Grid - Start")
        for lane in self._lanes:
            for shape in lane:
                Helper.print_info(f"[{shape.name}]", end=' ')
            Helper.print_info("\n")
        Helper.print_info("-------------Printing Grid - End")
        Helper.print_info("-------------Printing Shapes - Start")
        for shape in self._shapes:
            Helper.print_info(f"[{shape.name}]", end=', ')
        Helper.print_info("\n")
        Helper.print_info("-------------Printing Shapes - End")
        
        

    
    