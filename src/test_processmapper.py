from processmapper import ProcessMap, EventType, ActivityType, GatewayType


def test_case1():
    with ProcessMap(1150, 520) as my_process_map:
        with my_process_map.add_lane("Application \nUser") as lane1:
            start = lane1.add_element("Start", EventType.START)
            login = lane1.add_element("Login", ActivityType.TASK)
            search_records = lane1.add_element("Search Records", ActivityType.TASK)
            result_found = lane1.add_element("Result Found?", GatewayType.EXCLUSIVE)
            display_result = lane1.add_element("Display Result", ActivityType.TASK)
            logout = lane1.add_element("Logout", ActivityType.TASK)
            end = lane1.add_element("End", EventType.END)

            ### connect method 1
            start.connect(login).connect(search_records).connect(result_found)
            result_found.connect(display_result).connect(logout).connect(end)
            result_found.connect(search_records)

        my_process_map.draw()
        my_process_map.save("my_process_map_test_case01.png")
    # my_process_map.print()


def test_case2():
    with ProcessMap(1150, 520) as my_process_map:
        with my_process_map.add_lane("Application \nUser") as lane1:
            start = lane1.add_element("Start", EventType.START)
            enter_keyword = lane1.add_element("Enter Keyword", ActivityType.TASK)
            end = lane1.add_element("End", EventType.END)

        with my_process_map.add_lane("System") as lane2:
            login = lane2.add_element("Login", ActivityType.TASK)
            search_records = lane2.add_element("Search Records", ActivityType.TASK)
            result_found = lane2.add_element("Result Found?", GatewayType.EXCLUSIVE)
            display_result = lane2.add_element("Display Result", ActivityType.TASK)
            logout = lane2.add_element("Logout", ActivityType.TASK)

        start.connect(login).connect(enter_keyword).connect(search_records).connect(
            result_found
        )
        result_found.connect(display_result).connect(logout).connect(end)
        result_found.connect(search_records)

        my_process_map.draw()
        my_process_map.save("my_process_map_test_case02.png")
    # my_process_map.print()


if __name__ == "__main__":
    # test_case1()
    test_case2()
