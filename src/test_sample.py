from processpiper import ProcessMap, EventType, ActivityType, GatewayType

with ProcessMap("debug01", colour_theme="BLUEMOUNTAIN", width=8192) as my_process_map:
    with my_process_map.add_lane("customer") as lane1:
        start = lane1.add_element("start", EventType.START)
        activity_9 = lane1.add_element("brings a defective computer", ActivityType.TASK)
    with my_process_map.add_lane("crs") as lane2:
        activity_10 = lane2.add_element("checks the defect", ActivityType.TASK)
        activity_11 = lane2.add_element(
            "hand out a repair cost calculation", ActivityType.TASK
        )
        gateway_1 = lane2.add_element("the customer decide", GatewayType.EXCLUSIVE)
        activity_3 = lane2.add_element("are acceptable", ActivityType.TASK)
        activity_4 = lane2.add_element("continues", ActivityType.TASK)
        activity_5 = lane2.add_element("takes her computer", ActivityType.TASK)
        activity_12 = lane2.add_element("consists of two activities", ActivityType.TASK)
        activity_13 = lane2.add_element(
            "execute two activities in an arbitrary order", ActivityType.TASK
        )
        activity_14 = lane2.add_element("is", ActivityType.TASK)
        activity_15 = lane2.add_element("check the hardware", ActivityType.TASK)
        activity_16 = lane2.add_element("repair the hardware", ActivityType.TASK)
        activity_17 = lane2.add_element("checks the software", ActivityType.TASK)
        activity_18 = lane2.add_element("configure the software", ActivityType.TASK)
        activity_19 = lane2.add_element(
            "test the proper system functionality after each of these activities",
            ActivityType.TASK,
        )
        gateway_6 = lane2.add_element("detect an error", GatewayType.EXCLUSIVE)
        activity_8 = lane2.add_element(
            "execute another arbitrary repair activity", ActivityType.TASK
        )
        end = lane2.add_element("end", EventType.END)
        start.connect(activity_9)
        activity_9.connect(activity_10)
        activity_10.connect(activity_11)
        activity_11.connect(gateway_1)
        gateway_1.connect(activity_3)
        activity_3.connect(activity_4)
        activity_4.connect(activity_12)
        gateway_1.connect(activity_5)
        activity_5.connect(activity_12)
        activity_12.connect(activity_13)
        activity_13.connect(activity_14)
        activity_14.connect(activity_15)
        activity_15.connect(activity_16)
        activity_16.connect(activity_17)
        activity_17.connect(activity_18)
        activity_18.connect(activity_19)
        activity_19.connect(gateway_6)
        gateway_6.connect(activity_8)
        activity_8.connect(end)
        gateway_6.connect(end)
    my_process_map.draw()
    my_process_map.save("images/test/test_diagram.png")
