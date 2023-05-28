

from dataclasses import dataclass


@dataclass
class LaneRow:
    pass

@dataclass
class PoolRow:
    pass

@dataclass
class Grid:
    
    def __init__(self, pools):
        for pool in pools:
            for lane in pool.lanes:
                lane_row = []
                for shape in lane.shapes):
                    lane_row.append(shape)
                self.lanes.append(lane_row)

    
    
    