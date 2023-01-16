from processmapper.lane import EventType, ActivityType, GatewayType
from processmapper.processmap import ProcessMap


with ProcessMap() as my_process_map:
    with my_process_map.add_lane("Lane 1") as lane1:
        start = lane1.start("Start", EventType.START)
        activity_1 = lane1.activity("Activity 1", ActivityType.TASK)
        end = lane1.end("End", EventType.END)

        ### connect method 1
        start.connect(activity_1).connect(end)

        # lane1.start("Start", EventType.START).connect(
        #     lane1.activity("Activity 1", ActivityType.TASK)
        # ).connect(lane1.end("End", EventType.END))

    # with my_process_map.add_lane("Lane 1") as lane1:
    #     start = lane1.start("Start", EventType.START)
    #     activity_1 = lane1.activity("Activity 1", ActivityType.TASK)
    #     activity_2 = lane1.activity("Activity 2", ActivityType.TASK)
    #     activity_3 = lane1.activity("Activity 3", ActivityType.TASK)
    #     end = lane1.end("End", EventType.END)

    #     ### connect method 1
    #     start.connect(activity_1).connect(activity_2).connect(end)
    #     activity_1.connect(activity_3)
    # with my_process_map.add_lane("Lane 2") as lane2:
    #     start = lane2.start("Message Received", EventType.START)
    #     activity_4 = lane2.activity("Activity 4", ActivityType.TASK)
    #     activity_5 = lane2.activity("Activity 5", ActivityType.TASK)
    #     activity_6 = lane2.activity("Activity 6", ActivityType.TASK)
    #     end = lane2.end("End", EventType.END)

    #     ### connect method 2
    #     start.connect(activity_4)
    #     activity_4.connect(activity_5)
    #     activity_5.connect(activity_6)
    #     activity_6.connect(end)

    # my_process_map.draw()
    # my_process_map.save("my_process_map.png")
    my_process_map.print()
