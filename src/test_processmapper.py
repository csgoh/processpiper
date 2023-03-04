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
    with ProcessMap(950, 520) as my_process_map:
        with my_process_map.add_lane("Application \nUser") as lane1:
            start = lane1.add_element("Start", EventType.START)
            enter_keyword = lane1.add_element("Enter Keyword", ActivityType.TASK)
            end = lane1.add_element("End", EventType.END)

        with my_process_map.add_lane("System") as lane2:
            login = lane2.add_element("Login", ActivityType.TASK)
            search_records = lane2.add_element("Search Records", ActivityType.TASK)
            result_found = lane2.add_element("Result Found?", GatewayType.EXCLUSIVE)
            display_result = lane2.add_element("Display Result", ActivityType.TASK)
            refine_search = lane2.add_element("Refine Search", ActivityType.TASK)
            logout = lane2.add_element("Logout", ActivityType.TASK)

        start.connect(login).connect(enter_keyword).connect(search_records).connect(
            result_found
        ).connect(display_result).connect(logout).connect(end)
        result_found.connect(refine_search).connect(search_records)

        my_process_map.draw()
        my_process_map.save("my_process_map_test_case02.png")


def test_case3():
    with ProcessMap("Test Process", 950, 500) as my_process_map:
        with my_process_map.add_pool("System Search") as pool1:
            with pool1.add_lane("End User") as lane1:
                start = lane1.add_element("Start", EventType.START)
                enter_keyword = lane1.add_element("Enter Keyword", ActivityType.TASK)
                end = lane1.add_element("End", EventType.END)

            with pool1.add_lane("System") as lane2:
                login = lane2.add_element("Login", ActivityType.TASK)
                search_records = lane2.add_element("Search Records", ActivityType.TASK)
                result_found = lane2.add_element("Result Found?", GatewayType.EXCLUSIVE)
                display_result = lane2.add_element("Display Result", ActivityType.TASK)
                refine_search = lane2.add_element("Refine Search", ActivityType.TASK)
                logout = lane2.add_element("Logout", ActivityType.TASK)

        start.connect(login).connect(enter_keyword).connect(search_records).connect(
            result_found
        ).connect(display_result).connect(logout).connect(end)
        result_found.connect(refine_search).connect(search_records)

        my_process_map.draw()
        my_process_map.save("my_process_map_test_case03.png")


def test_case4():
    with ProcessMap("Sample Test Process", 950, 700) as my_process_map:
        with my_process_map.add_pool("System Search") as pool1:
            with pool1.add_lane("End User") as lane1:
                start = lane1.add_element("Start", EventType.START)
                enter_keyword = lane1.add_element("Enter Keyword", ActivityType.TASK)
                end = lane1.add_element("End", EventType.END)

            with pool1.add_lane("System") as lane2:
                login = lane2.add_element("Login", ActivityType.TASK)
                search_records = lane2.add_element("Search Records", ActivityType.TASK)
                result_found = lane2.add_element("Result Found?", GatewayType.EXCLUSIVE)
                display_result = lane2.add_element("Display Result", ActivityType.TASK)
                logout = lane2.add_element("Logout", ActivityType.TASK)

        with my_process_map.add_lane("System 2") as lane3:
            log_error = lane3.add_element("Log Error", ActivityType.TASK)

        start.connect(login).connect(enter_keyword).connect(search_records).connect(
            result_found
        ).connect(display_result).connect(logout).connect(end)
        result_found.connect(log_error).connect(display_result)

        my_process_map.draw()
        my_process_map.save("my_process_map_test_case04.png")


def test_case5():
    with ProcessMap("Sample Test Process", 1100, 700) as my_process_map:
        with my_process_map.add_lane("End User") as lane1:
            start = lane1.add_element("Start", EventType.START)
            enter_keyword = lane1.add_element("Enter Keyword", ActivityType.TASK)
        with my_process_map.add_pool("System Search") as pool1:
            with pool1.add_lane("Database System") as lane2:
                login = lane2.add_element("Login", ActivityType.TASK)
                search_records = lane2.add_element("Search Records", ActivityType.TASK)
                result_found = lane2.add_element("Result Found?", GatewayType.EXCLUSIVE)
                display_result = lane2.add_element("Display Result", ActivityType.TASK)
                logout = lane2.add_element("Logout", ActivityType.TASK)
                end = lane2.add_element("End", EventType.END)

            with pool1.add_lane("Log System") as lane3:
                log_error = lane3.add_element("Log Error", ActivityType.TASK)

        start.connect(login).connect(enter_keyword).connect(search_records).connect(
            result_found
        ).connect(display_result).connect(logout).connect(end)
        result_found.connect(log_error).connect(display_result)

        my_process_map.draw()
        my_process_map.save("my_process_map_test_case05.png")


def test_case6():
    with ProcessMap("Placement Test (Same Lane)", 1100, 300) as my_process_map:
        with my_process_map.add_lane("End User") as lane1:
            start = lane1.add_element("Start", EventType.START)
            task1 = lane1.add_element("Task 1", ActivityType.TASK)
            task2 = lane1.add_element("Task 2", ActivityType.TASK)
            task3 = lane1.add_element("Task 3", ActivityType.TASK)
            end = lane1.add_element("End", EventType.END)

            start.connect(task1).connect(task2).connect(task3).connect(end)

        my_process_map.set_footer("Generated by ProcessMap")
        my_process_map.draw()
        my_process_map.save("my_process_map_test_case06.png")


def test_case7():
    with ProcessMap(
        "Placement Test (Same Pool, Diff Lanes)", 1300, 650
    ) as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                start = lane1.add_element("Start", EventType.START)
                task1 = lane1.add_element("Task 1", ActivityType.TASK)
                task5 = lane1.add_element("Task 5", ActivityType.TASK)
                end = lane1.add_element("End", EventType.END)
            with pool1.add_lane("Lane 2") as lane2:
                task2 = lane2.add_element("Task 2", ActivityType.TASK)
                task4 = lane2.add_element("Task 4", ActivityType.TASK)

            with pool1.add_lane("Lane 3") as lane3:
                task3 = lane3.add_element("Task 3", ActivityType.TASK)

                start.connect(task1).connect(task2).connect(task3)
                task3.connect(task4).connect(task5).connect(end)

        my_process_map.set_footer("Generated by ProcessMap")
        my_process_map.draw()
        my_process_map.save("my_process_map_test_case07.png")


if __name__ == "__main__":
    test_case6()
    test_case7()
