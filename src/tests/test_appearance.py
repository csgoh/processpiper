import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from processpiper import ProcessMap, EventType, ActivityType, GatewayType
from util_test import get_test_file_path


def test_case01():
    # Test title, element and footer font size
    with ProcessMap("Test Diagram") as process_map:
        with process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("Start", EventType.START)
            task1 = lane1.add_element("Task 1", ActivityType.TASK)
            gateway1 = lane1.add_element("Gateway", GatewayType.EXCLUSIVE)
            end = lane1.add_element("End", EventType.END)
            start.connect(task1).connect(gateway1).connect(end)

        process_map.set_title_font_size(30)
        process_map.set_element_font_size(10)
        process_map.set_footer("My footer", font_size=20)

        process_map.draw()

        output_file = get_test_file_path("test_appearance_01.png")
        process_map.save(output_file)
        output_file = output_file.replace(".png", ".bpmn")
        process_map.export_to_bpmn(output_file)
