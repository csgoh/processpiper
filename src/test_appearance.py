from .processpiper import ProcessMap, EventType, ActivityType, GatewayType


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
        process_map.save("images/test/test_appearance01.png")


if __name__ == "__main__":
    test_case01()