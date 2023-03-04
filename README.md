[![license](https://img.shields.io/badge/license-mit-brightgreen.svg?style=plastic)](https://en.wikipedia.org/wiki/MIT_License)
[![CodeFactor](https://www.codefactor.io/repository/github/csgoh/processmapper/badge?style=plastic)](https://www.codefactor.io/repository/github/csgoh/processmapper)
![code size](https://img.shields.io/github/languages/code-size/csgoh/processmapper?style=plastic)

# ProcessMapper

This is a python library to generate business process diagram using code. The intention is adhere to BPMN notation.

It is still under development :construction:

Initial release would only cover the following basic business process elements. Other element types will be introduced in subsequence releases.

* Event: Start, End, Timer, Intermediate
* Activity: Task, Subprocess
* Gateway: Inclusive, Exclusive, Parallel

Any ideas or suggestions, please send it to me via [GitHub Discussions](https://github.com/csgoh/processmapper/discussions).

You can see the sample code and output for design concept below.

```python
from processmapper import ProcessMap, EventType, ActivityType, GatewayType

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


if __name__ == "__main__":
    test_case5()
```

![Process Map](https://github.com/csgoh/processmapper/blob/main/my_process_map_test_case05.png)

Thank you for checking out my project. I hope you find it useful and enjoyable.

<a href="https://www.buymeacoffee.com/csgoh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Implementation Checklist

These are a list of items that need to be implemented or fixed before the initial release.

- [X] Implement Start, End and Timer Event elements
- [X] Implement Task Activity elements
- [X] Implement Inclusive, Exclusive and Parallel Gateway elements
- [X] Implement pool and lane
- [X] Implement diagram title
- [X] Implement diagram footer
- [ ] Automatically change surface size based on the element layout
- [ ] Fix the connection alignment issue
- [ ] Implement placement (left to right) of for elements in the same lane
- [ ] Implement placement (left to right) of elements in the same pool but different lane
- [ ] Implement placement (top to bottom) of elements in the different pool
- [ ] Support colour themes
- [ ] Implement Intermediate Event and Subprocess Activity Elements
