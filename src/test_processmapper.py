from processmapper.lane import EventType, ActivityType, GatewayType
from processmapper.processmap import ProcessMap


with ProcessMap(1150, 220) as my_process_map:
    with my_process_map.add_lane("Application \nUser") as lane1:
        start = lane1.add_element("Start", EventType.START)
        login = lane1.add_element("Login", ActivityType.TASK)
        search_records = lane1.add_element("Search Records", ActivityType.TASK)
        result_found = lane1.add_element("Result Found?", GatewayType.EXCLUSIVE)
        display_result = lane1.add_element("Display Result", ActivityType.TASK)
        logout = lane1.add_element("Logout", ActivityType.TASK)
        end = lane1.add_element("End", EventType.END)

        # start = lane1.start("Start", ActivityType.TASK)
        # activity_1 = lane1.activity("Login", ActivityType.TASK)
        # activity_2 = lane1.activity("Search Records", ActivityType.TASK)
        # end = lane1.end("End", EventType.END)

        ### Another method to add element
        # start = Event("Start")
        # activity_1 = Activitty("Logon")
        # lane1.add_element(start)
        # lane1.add_element(activity_1)

        ### connect method 1
        start.connect(login).connect(search_records).connect(result_found)
        result_found.connect(display_result).connect(logout).connect(end)
        result_found.connect(search_records)

        # lane1.start("Start", EventType.START).connect(
        #     lane1.activity("Activity 1", ActivityType.TASK)
        # ).connect(lane1.end("End", EventType.END))

    my_process_map.draw()
    my_process_map.save("my_process_map_test.png")
    # my_process_map.print()
