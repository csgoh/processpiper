from processmapper.processmap import ProcessMap
from processmapper.lane import Lane


# lane1: Lane


with ProcessMap() as my_process_map:
    with my_process_map.add_lane("Lane 1") as lane1:
        start = lane1.start("Start", "signal")
        activity_1 = lane1.activity("Activity 1")
        activity_2 = lane1.activity("Activity 2")
        activity_3 = lane1.activity("Activity 3")
        end = lane1.end("End")
        ### connect method 1
        start.connect(activity_1).connect(activity_2).connect(end)
        activity_1.connect(activity_3)

        ### connect method 2
        lane1.connect(start, activity_1, activity_2, end)
        lane1.connect(activity_1, activity_3)

    my_process_map.draw()
    my_process_map.save("my_process_map.png")
