from src.processpiper import ProcessMap, EventType, ActivityType, GatewayType

with ProcessMap("This is a test diagram", colour_theme="GREENTURTLE") as my_process_map:
    with my_process_map.add_lane("Customer") as lane1:
        start = lane1.add_element("start", EventType.START)
        br1 = lane1.add_element("Branch 1", GatewayType.EXCLUSIVE)
        # br2 = lane1.add_element("Branch 2", GatewayType.EXCLUSIVE)
        # br3 = lane1.add_element("Branch 2", GatewayType.EXCLUSIVE)
        do = lane1.add_element("Do something", ActivityType.TASK)
        end = lane1.add_element("end", EventType.END)
        # start.connect(br1).connect(br2).connect(br3).connect(do).connect(end)
        # br1.connect(br2).connect(br3).connect(do).connect(end)
        start.connect(br1).connect(do).connect(end)

    my_process_map.draw()
    my_process_map.save("src/test01.png")
