from dataclasses import dataclass, field
from processmapper.lane import Lane
from processmapper.painter import Painter


@dataclass
class ProcessMap:
    lanes: list = field(init=False, default_factory=list)

    width: int = field(init=False, default=1200)
    height: int = field(init=False, default=800)

    def add_lane(self, lane_text: str) -> Lane:
        lane = Lane(lane_text)
        self.lanes.append(lane)
        return lane

    def get_surface_size(self) -> tuple:
        x, y = 0, 0
        if self.lanes:
            for lane in self.lanes:
                ### Calculate the x and y position of the lane and shapes in the lane
                x, y, w, h = lane.set_draw_position(x, y)
                self.width = max(self.width, x + w)
                self.height = max(self.height, y + h)

        return self.width, self.height

    def draw(self) -> None:
        ### Determine the size of the process map
        self.width, self.height = self.get_surface_size()
        self.__painter = Painter(self.width, self.height)

        ### Draw the lanes and the shapes in the lanes
        if self.lanes:
            for lane in self.lanes:
                lane.draw(self.__painter)

    def save(self, filename: str) -> None:
        self.__painter.save_surface(filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def print(self) -> None:
        for lane in self.lanes:
            print(f"[{lane.text}, number of elements: {len(lane.shapes)}]")
            for shape in lane.shapes:
                print(f'    ("{shape.text}", type: {shape.__class__.__name__})')
                for connection in shape.connection_to:
                    print(f"        ->: {connection.text}")
                for connection in shape.connection_from:
                    print(f"        <-: {connection.text}")
