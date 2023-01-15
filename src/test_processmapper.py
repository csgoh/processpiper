from processmapper.processmap import ProcessMap, EventType, ActivityType, GatewayType


with ProcessMap() as my_process_map:
    with my_process_map.add_lane("Lane 1") as lane1:
        start = lane1.start("Start", EventType.START)
        activity_1 = lane1.activity("Activity 1", ActivityType.TASK)
        activity_2 = lane1.activity("Activity 2", ActivityType.TASK)
        activity_3 = lane1.activity("Activity 3", ActivityType.TASK)
        end = lane1.end("End", EventType.END)

        ### connect method 1
        start.connect(activity_1).connect(activity_2).connect(end)
        activity_1.connect(activity_3)

    my_process_map.draw()
    my_process_map.save("my_process_map.png")
