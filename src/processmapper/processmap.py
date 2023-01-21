from dataclasses import dataclass, field
from processmapper.lane import Lane
from processmapper.painter import Painter


@dataclass
class ProcessMap:
    _lanes: list = field(init=False, default_factory=list)

    width: int = field(init=True, default=1200)
    height: int = field(init=True, default=800)
    colour_theme: str = field(init=True, default="DEFAULT")

    def add_lane(self, lane_text: str) -> Lane:
        lane = Lane(lane_text)
        self._lanes.append(lane)
        return lane

    def get_surface_size(self) -> tuple:
        x, y = 0, 0
        if self._lanes:
            for lane in self._lanes:
                ### Calculate the x and y position of the lane and shapes in the lane
                x, y, w, h = lane.set_draw_position(x, y, self.__painter)
                self.width = max(self.width, x + w)
                self.height = max(self.height, y + h)

        return self.width, self.height

    def draw(self) -> None:
        self.__painter = Painter(self.width, self.height)

        self.__set_colour_palette(self.colour_theme)

        ### Determine the size of the process map
        self.width, self.height = self.get_surface_size()

        ### Draw the lanes and the shapes in the lanes
        if self._lanes:
            for lane in self._lanes:
                lane.draw()

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
