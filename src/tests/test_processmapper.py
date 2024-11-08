import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from processpiper import ProcessMap, EventType, ActivityType, GatewayType
from processpiper.coordinate import Side
from util_test import get_test_file_path


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

        output_file = get_test_file_path("test_processmapper_01.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


def test_case2():
    with ProcessMap(
        "Product Order Processing", colour_theme="BLUEMOUNTAIN"
    ) as my_process_map:
        with my_process_map.add_lane("Customer") as lane1:
            start = lane1.add_element("Start", EventType.START)
            order = lane1.add_element("Order is received", ActivityType.TASK)
            process_confirm_payment = lane1.add_element(
                "Process & Confirm Payment", ActivityType.TASK
            )
        with my_process_map.add_lane("Sales") as lane2:
            list_order = lane2.add_element(
                "List all Order Requirements", ActivityType.TASK
            )
            credit_pending = lane2.add_element(
                "Credit Pending Addressed", ActivityType.TASK
            )
            confirmed = lane2.add_element("Confirmed?", GatewayType.EXCLUSIVE)
            generate_order = lane2.add_element("Generate Order", ActivityType.TASK)
            end = lane2.add_element("End", EventType.END)
        with my_process_map.add_lane("Credit & Invoicing") as lane3:
            order_received = lane3.add_element("Order is received", ActivityType.TASK)
            branching1 = lane3.add_element("Received?", GatewayType.PARALLEL)
            credit_check = lane3.add_element("Perform Credit Check", ActivityType.TASK)
            pending_credit = lane3.add_element("Pending Credit?", GatewayType.EXCLUSIVE)
            prepare_invoice = lane3.add_element("Prepare Invoice", ActivityType.TASK)
            invoice_sent = lane3.add_element("Invoice is Sent", ActivityType.TASK)
        with my_process_map.add_lane("Warehouse") as lane4:
            generated_order = lane4.add_element(
                "Order will be generated", ActivityType.TASK
            )
            pack_order = lane4.add_element("Pack Order", ActivityType.TASK)
            ship_order = lane4.add_element("Ship Order", ActivityType.TASK)

        start.connect(order)
        order.connect(list_order)
        list_order.connect(order_received)
        order_received.connect(branching1)
        branching1.connect(credit_check)
        branching1.connect(generated_order)
        credit_check.connect(pending_credit)
        pending_credit.connect(credit_pending, "No")
        pending_credit.connect(prepare_invoice, "Yes")
        credit_pending.connect(confirmed)
        confirmed.connect(generate_order, "No")
        confirmed.connect(prepare_invoice, "Yes")
        generate_order.connect(end)
        prepare_invoice.connect(invoice_sent)
        invoice_sent.connect(process_confirm_payment)

        generated_order.connect(pack_order)
        pack_order.connect(ship_order)
        ship_order.connect(process_confirm_payment)
        process_confirm_payment.connect(end)

        my_process_map.set_footer("Generated by ProcessPiper")
        my_process_map.draw()

        output_file = get_test_file_path("test_processmapper_02.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


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

        output_file = get_test_file_path("test_processmapper_03.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


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

        output_file = get_test_file_path("test_processmapper_04.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


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

        output_file = get_test_file_path("test_processmapper_05.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


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

        output_file = get_test_file_path("test_processmapper_06.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


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

        output_file = get_test_file_path("test_processmapper_07.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


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

    output_file = get_test_file_path("test_processmapper_08.png")
    my_process_map.save(output_file)
    output_file = output_file.replace(".png", ".bpmn")
    my_process_map.export_to_bpmn(output_file)


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

    output_file = get_test_file_path("test_processmapper_09.png")
    my_process_map.save(output_file)
    output_file = output_file.replace(".png", ".bpmn")
    my_process_map.export_to_bpmn(output_file)


def test_case10(colour_theme: str = "BLUEMOUNTAIN"):
    with ProcessMap(
        "Shipment Process of a Hardware Retailer", colour_theme=colour_theme
    ) as my_process_map:
        with my_process_map.add_pool("Hardware Retailer") as pool1:
            with pool1.add_lane("Logistics Manager") as lane1:
                take_insurance = lane1.add_element("Take Insurance", ActivityType.TASK)

            with pool1.add_lane("Clerk") as lane2:
                start = lane2.add_element("Goods to ship", EventType.START)
                branching1 = lane2.add_element("Branching 1", GatewayType.PARALLEL)
                decide = lane2.add_element(
                    "Decide if normal post or special shipment", ActivityType.TASK
                )
                branching2 = lane2.add_element(
                    "Mode of Delivery", GatewayType.EXCLUSIVE
                )
                check_extra_insurance = lane2.add_element(
                    "Check if extra insurance is needed", ActivityType.TASK
                )
                branching3 = lane2.add_element("Branching 3", GatewayType.INCLUSIVE)
                fill_in_post = lane2.add_element(
                    "Fill in a Post label", ActivityType.TASK
                )
                branching4 = lane2.add_element("Branching 4", GatewayType.INCLUSIVE)

                request_quote = lane2.add_element(
                    "Request quotes from carriers", ActivityType.TASK
                )
                assign_carrier = lane2.add_element(
                    "Assign carrier & prepare paper work", ActivityType.TASK
                )
                branching5 = lane2.add_element("Branching 5", GatewayType.EXCLUSIVE)

            with pool1.add_lane("Warehouse Worker") as lane3:
                package_goods = lane3.add_element("Package goods", ActivityType.TASK)
                branching6 = lane3.add_element("Branching 6", GatewayType.PARALLEL)
                add_paperwork = lane3.add_element(
                    "Add paperwork to move package to pick area", ActivityType.TASK
                )
                end = lane3.add_element("Goods available for pick up", EventType.END)

            start.connect(branching1)
            branching1.connect(decide).connect(branching2)
            branching1.connect(package_goods).connect(branching6)

            branching2.connect(check_extra_insurance).connect(branching3)

            # branching2.connect(request_quote).connect(assign_carrier).connect(
            #     branching5
            # )
            branching2.connect(request_quote).connect(assign_carrier).connect(
                branching5,
                source_connection_side=Side.RIGHT,
                target_connection_side=Side.BOTTOM,
            )
            branching3.connect(take_insurance).connect(branching4)
            # branching3.connect(fill_in_post).connect(branching4)

            # branching3.connect(fill_in_post).connect(branching4, source_connection_side=Side.BOTTOM, target_connection_side=Side.BOTTOM)
            # branching3.connect(fill_in_post).connect(branching4, source_connection_side=Side.BOTTOM)
            branching3.connect(fill_in_post).connect(
                branching4, target_connection_side=Side.BOTTOM
            )

            # branching4.connect(branching5).connect(branching6)
            branching4.connect(branching5).connect(
                branching6,
                source_connection_side=Side.RIGHT,
                target_connection_side=Side.TOP,
            )

            branching6.connect(add_paperwork).connect(end)

            my_process_map.set_footer("Generated by ProcessPiper")
            my_process_map.draw()

            output_file = get_test_file_path("test_processmapper_10.png")
            my_process_map.save(output_file)
            output_file = output_file.replace(".png", ".bpmn")
            my_process_map.export_to_bpmn(output_file)


def test_case11():
    # 1: Test gateway branching to two tasks in two lanes
    # 2: Test two tasks merging into one gateway
    with ProcessMap("Test Case 11") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("Start", EventType.START)
            branch1 = lane1.add_element("fan out", GatewayType.PARALLEL)
            task1 = lane1.add_element("Task 1", ActivityType.TASK)
            task2 = lane1.add_element("Task 2", ActivityType.TASK)
            branch2 = lane1.add_element("fan in", GatewayType.PARALLEL)
            end = lane1.add_element("End", EventType.END)

            start.connect(branch1)
            branch1.connect(task1).connect(branch2)
            branch1.connect(task2).connect(branch2)
            branch2.connect(end)

            my_process_map.draw()

            output_file = get_test_file_path("test_processmapper_11.png")
            my_process_map.save(output_file)
            output_file = output_file.replace(".png", ".bpmn")
            my_process_map.export_to_bpmn(output_file)


def test_case12():
    with ProcessMap("Test Case 12") as my_process_map:
        with my_process_map.add_pool("Hardware Retailer") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                task1 = lane1.add_element("Task 1", ActivityType.TASK)

            with pool1.add_lane("Lane 2") as lane2:
                start = lane2.add_element("Start", EventType.START)
                branch1 = lane2.add_element("fan out", GatewayType.PARALLEL)
                task2 = lane2.add_element("Task 2", ActivityType.TASK)
                branch2 = lane2.add_element("fan in", GatewayType.PARALLEL)
                end = lane2.add_element("End", EventType.END)

                start.connect(branch1)
                branch1.connect(task1).connect(branch2)
                branch1.connect(task2).connect(branch2)
                branch2.connect(end)

                my_process_map.draw()

                output_file = get_test_file_path("test_processmapper_12.png")
                my_process_map.save(output_file)
                output_file = output_file.replace(".png", ".bpmn")
                my_process_map.export_to_bpmn(output_file)


def test_case13():
    with ProcessMap("Conditional Events") as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                cond = lane1.add_element("Start", EventType.CONDITIONAL)
                cond_intermediate = lane1.add_element(
                    "Intermediate", EventType.CONDITIONAL
                )
                end = lane1.add_element("End", EventType.END)

        cond.connect(cond_intermediate).connect(end)

        my_process_map.draw()

        output_file = get_test_file_path("test_processmapper_13.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


def test_case14():
    with ProcessMap("Message Events") as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                mesg = lane1.add_element("Start", EventType.MESSAGE)
                mesg_intermediate = lane1.add_element("Intermediate", EventType.MESSAGE)
                mesg_end = lane1.add_element("End", EventType.MESSAGE)

        mesg.connect(mesg_intermediate).connect(mesg_end)

        my_process_map.draw()

        output_file = get_test_file_path("test_processmapper_14.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


def test_case15():
    with ProcessMap("Signal Events") as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                mesg = lane1.add_element("Start", EventType.SIGNAL)
                mesg_intermediate = lane1.add_element("Intermediate", EventType.SIGNAL)
                mesg_end = lane1.add_element("End", EventType.SIGNAL)

        # mesg.connect(mesg_intermediate).connect(mesg_mesg).connect(mesg_end)
        mesg.connect(mesg_intermediate).connect(mesg_end)

        my_process_map.draw()

        output_file = get_test_file_path("test_processmapper_15.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


def test_case16():
    with ProcessMap("All Events") as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1") as lane1:
                event1 = lane1.add_element("START", EventType.START)
                event2 = lane1.add_element("INTERMEDIATE", EventType.INTERMEDIATE)
                event3 = lane1.add_element("SIGNAL", EventType.SIGNAL)
                event4 = lane1.add_element("SIGL_INT", EventType.SIGNAL_INTERMEDIATE)
                event5 = lane1.add_element("SIGNAL_END", EventType.SIGNAL_END)
                event6 = lane1.add_element("CONDITIONAL", EventType.CONDITIONAL)
                event7 = lane1.add_element(
                    "COND_INT", EventType.CONDITIONAL_INTERMEDIATE
                )
                event8 = lane1.add_element("MESSAGE", EventType.MESSAGE)
                event9 = lane1.add_element("MSG_INT", EventType.MESSAGE_INTERMEDIATE)
                event10 = lane1.add_element("MESSAGE_END", EventType.MESSAGE_END)
                event11 = lane1.add_element("LINK", EventType.LINK)
                event12 = lane1.add_element("END", EventType.END)

        event1.connect(event2).connect(event3)
        event3.connect(event4).connect(event5)
        event5.connect(event6).connect(event7)
        event7.connect(event8).connect(event9)
        event9.connect(event10).connect(event11)
        event11.connect(event12)

        my_process_map.draw()

        output_file = get_test_file_path("test_processmapper_16.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)


def test_case17():
    with ProcessMap("All Events") as my_process_map:
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 1A") as lane1:
                event1 = lane1.add_element("START", EventType.START)

                event12 = lane1.add_element("END", EventType.END)
        with my_process_map.add_pool("Pool 2") as pool2:
            with pool2.add_lane("Lane 1A") as lane2:
                task1 = lane2.add_element("TASK 1", ActivityType.TASK)

                task2 = lane2.add_element("TASK 22", ActivityType.TASK)

        # event1.connect(task1).connect(task2).connect(event12)
        # event1.connect(task2).connect(event12)
        event1.connect(task1).connect(task2).connect(event12)

        my_process_map.draw()

        output_file = get_test_file_path("test_processmapper_17.png")
        my_process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        my_process_map.export_to_bpmn(output_file)
