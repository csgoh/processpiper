from processpiper import ProcessMap, EventType, ActivityType, GatewayType


def test_case1():
    with ProcessMap("Sample Process Map") as my_process_map:
        with my_process_map.add_lane("Application User") as lane1:
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


def test_case3():
    with ProcessMap("Test Process") as my_process_map:
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
    with ProcessMap("Sample Test Process") as my_process_map:
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
    with ProcessMap(
        "Sample Test Process", colour_theme="BLUEMOUNTAIN"
    ) as my_process_map:
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

        start.connect(login, "User \nAuthenticates").connect(
            enter_keyword, "Authenticated"
        ).connect(search_records, "Search Criteria")
        search_records.connect(result_found, "Result").connect(display_result, "Yes")
        display_result.connect(logout).connect(end)
        result_found.connect(log_error, "No").connect(display_result)

        my_process_map.set_footer("Generated by ProcessPiper")
        my_process_map.draw()
        my_process_map.save("my_process_map_test_case05.png")


def test_case6():
    with ProcessMap("Placement Test (Same Lane)") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("Start", EventType.START)
            task1 = lane1.add_element("Task 1", ActivityType.TASK)
            task2 = lane1.add_element("Task 2", ActivityType.TASK)
            task3 = lane1.add_element("Task 3", ActivityType.TASK)
            end = lane1.add_element("End", EventType.END)

            start.connect(task1, "label 1").connect(
                task2, "label 2\naddition\ntext"
            ).connect(task3, "label 3").connect(end, "label 4")

        my_process_map.set_footer("Generated by ProcessPiper")
        my_process_map.draw()
        my_process_map.save("my_process_map_test_case06.png")


def test_case7():
    with ProcessMap("Placement Test (Same Pool, Diff Lanes)") as my_process_map:
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

        my_process_map.set_footer("Generated by ProcessPiper")
        my_process_map.draw()
        my_process_map.save("my_process_map_test_case07.png")


def test_case8():
    with ProcessMap("Placement Test (Diff Pool)") as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                start = lane1.add_element("Start", EventType.START)
                task1 = lane1.add_element("Task 1", ActivityType.TASK)
                task2 = lane1.add_element("Task 2", ActivityType.TASK)
                task5 = lane1.add_element("Task 5", ActivityType.TASK)
                end = lane1.add_element("End", EventType.END)
        with my_process_map.add_pool("Pool 2") as pool2:
            with pool2.add_lane("Lane 1") as lane2:
                task3 = lane2.add_element("Task 3", ActivityType.TASK)
                task4 = lane2.add_element("Task 4", ActivityType.TASK)

            start.connect(task1).connect(task2).connect(task3).connect(task4).connect(
                task5
            ).connect(end)

    my_process_map.set_footer("Generated by ProcessPiper")
    my_process_map.draw()
    my_process_map.save("my_process_map_test_case08.png")


def test_case9():
    with ProcessMap("Sub Process Test") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("Start", EventType.START)
            task1 = lane1.add_element(
                "Sub Process 1",
                ActivityType.SUBPROCESS,
            )
            task2 = lane1.add_element("Task 2", ActivityType.TASK)
            end = lane1.add_element("End", EventType.END)

            start.connect(task1).connect(task2).connect(end)

    my_process_map.set_footer("Generated by ProcessPiper")
    my_process_map.draw()
    my_process_map.save("my_process_map_test_case09.png")


def test_case10(colour_theme: str = "BLUEMOUNTAIN"):
    with ProcessMap(
        "Shipment Process of a Hardware Retailer", colour_theme=colour_theme
    ) as my_process_map:
        with my_process_map.add_pool("Hardware Retailer") as pool1:
            with pool1.add_lane("Logistics Manager") as lane1:
                take_insurance = lane1.add_element("Take Insurance", ActivityType.TASK)

            with pool1.add_lane("Clerk") as lane2:
                start = lane2.add_element("Goods to ship", EventType.START)
                branching1 = lane2.add_element("", GatewayType.PARALLEL)
                decide = lane2.add_element(
                    "Decide if normal post or special shipment", ActivityType.TASK
                )
                branching2 = lane2.add_element(
                    "Mode of Delivery", GatewayType.EXCLUSIVE
                )
                check_extra_insurance = lane2.add_element(
                    "Check if extra insurance is needed", ActivityType.TASK
                )
                branching3 = lane2.add_element("", GatewayType.INCLUSIVE)
                fill_in_post = lane2.add_element(
                    "Fill in a Post label", ActivityType.TASK
                )
                branching4 = lane2.add_element("", GatewayType.INCLUSIVE)

                request_quote = lane2.add_element(
                    "Request quotes from carriers", ActivityType.TASK
                )
                assign_carrier = lane2.add_element(
                    "Assign carrier & prepare paper work", ActivityType.TASK
                )
                branching5 = lane2.add_element("", GatewayType.EXCLUSIVE)

            with pool1.add_lane("Warehouse Worker") as lane3:
                package_goods = lane3.add_element("Package goods", ActivityType.TASK)
                branching6 = lane3.add_element("", GatewayType.PARALLEL)
                add_paperwork = lane3.add_element(
                    "Add paperwork to move package to pick area", ActivityType.TASK
                )
                end = lane3.add_element("Goods available for pick up", EventType.END)

            start.connect(branching1)
            branching1.connect(decide).connect(branching2)
            branching1.connect(package_goods).connect(branching6)

            branching2.connect(check_extra_insurance).connect(branching3)
            branching2.connect(request_quote).connect(assign_carrier).connect(
                branching5
            )

            branching3.connect(take_insurance).connect(branching4)
            branching3.connect(fill_in_post).connect(branching4)

            branching4.connect(branching5).connect(branching6)

            branching6.connect(add_paperwork).connect(end)

            my_process_map.set_footer("Generated by ProcessPiper")
            my_process_map.draw()
            my_process_map.save(colour_theme + "-my_process_map_test_case10.png")


def test_case11():
    # 1: Test gateway branching to two tasks in two lanes
    # 2: Test two tasks merging into one gateway
    with ProcessMap("Test Case 11") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            branch1 = lane1.add_element("fan out", GatewayType.PARALLEL)
            task1 = lane1.add_element("Task 1", ActivityType.TASK)
            task2 = lane1.add_element("Task 2", ActivityType.TASK)
            branch2 = lane1.add_element("fan in", GatewayType.PARALLEL)

            branch1.connect(task1).connect(branch2)
            branch1.connect(task2).connect(branch2)

            my_process_map.draw()
            my_process_map.save("my_process_map_test_case11.png")


def test_case12():
    with ProcessMap("Test Case 11") as my_process_map:
        with my_process_map.add_pool("Hardware Retailer") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                task1 = lane1.add_element("Task 1", ActivityType.TASK)

            with pool1.add_lane("Lane 2") as lane2:
                branch1 = lane2.add_element("fan out", GatewayType.PARALLEL)
                task2 = lane2.add_element("Task 2", ActivityType.TASK)
                branch2 = lane2.add_element("fan in", GatewayType.PARALLEL)

                branch1.connect(task1).connect(branch2)
                branch1.connect(task2).connect(branch2)

                my_process_map.draw()
                my_process_map.save("my_process_map_test_case12.png")


if __name__ == "__main__":
    test_case1()
    test_case3()
    test_case4()
    test_case5()
    test_case6()
    test_case7()
    test_case8()
    test_case9()
    test_case10(colour_theme="DEFAULT")
    test_case10(colour_theme="BLUEMOUNTAIN")
    test_case10(colour_theme="ORANGEPEEL")
    test_case10(colour_theme="GREENTURTLE")
    test_case10(colour_theme="GREYWOOF")
    test_case12()
