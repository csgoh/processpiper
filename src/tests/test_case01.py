import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from processpiper import ProcessMap, EventType, ActivityType, GatewayType
from util_test import get_test_file_path


def test_case01():
    with ProcessMap(
        "Pizza Order Process", colour_theme="BLUEMOUNTAIN"
    ) as my_process_map:
        with my_process_map.add_lane("Customer") as lane1:
            start = lane1.add_element("start", EventType.START)
            browse_website = lane1.add_element(
                "Browse PizzaPiper website", ActivityType.TASK
            )
            order_pizza = lane1.add_element("Order a pizza", ActivityType.TASK)
            make_payment = lane1.add_element("Make payment", ActivityType.TASK)
            receive_pizza = lane1.add_element("Receive pizza", ActivityType.TASK)
            end = lane1.add_element("end", EventType.END)
        with my_process_map.add_pool("Pizza Piper Enterprise") as pool1:
            with pool1.add_lane("Pizza Shop") as lane2:
                receive_order = lane2.add_element("Receive order", ActivityType.TASK)
                bake_pizza = lane2.add_element("Bake pizza", ActivityType.TASK)
                pizza_ready = lane2.add_element("Pizza ready?", GatewayType.EXCLUSIVE)
            with pool1.add_lane("Pizza Delivery") as lane3:
                deliver_pizza = lane3.add_element("Deliver pizza", ActivityType.TASK)
            start.connect(browse_website)
            browse_website.connect(order_pizza)
            order_pizza.connect(make_payment)
            make_payment.connect(receive_order, "Order details")
            # receive_order.connect(bake_pizza, source_connection_side=Side.BOTTOM, target_connection_side=Side.LEFT)
            receive_order.connect(bake_pizza)
            bake_pizza.connect(pizza_ready)
            pizza_ready.connect(deliver_pizza, "Yes")
            deliver_pizza.connect(receive_pizza, "Freshly baked \npizza")
            # pizza_ready.connect(bake_pizza, "No", source_connection_side=Side.TOP, target_connection_side=Side.TOP)
            pizza_ready.connect(bake_pizza, "No")
            receive_pizza.connect(end)
        my_process_map.set_footer(" Generated by Process Piper")
        my_process_map.draw()

        output_png = get_test_file_path("test_case_01.png")
        output_bpmn = get_test_file_path("test_case_01.bpmn")
        my_process_map.save(output_png)
        my_process_map.export_to_bpmn(output_bpmn)


def test_case02():
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

        output_png = get_test_file_path("test_case_02.png")
        output_bpmn = get_test_file_path("test_case_02.bpmn")
        my_process_map.save(output_png)
        my_process_map.export_to_bpmn(output_bpmn)
