[![license](https://img.shields.io/badge/license-mit-brightgreen.svg?style=plastic)](https://en.wikipedia.org/wiki/MIT_License)
[![CodeFactor](https://www.codefactor.io/repository/github/csgoh/processmapper/badge?style=plastic)](https://www.codefactor.io/repository/github/csgoh/processmapper)
![code size](https://img.shields.io/github/languages/code-size/csgoh/processmapper?style=plastic)

# ProcessMapper

This is a python library to generate business process diagram using code. The intention is adhere to BPMN notation.

It is still under development :construction:

Any ideas or suggestions, please send it to me via [GitHub Discussions](https://github.com/csgoh/processmapper/discussions).

You can see the sample code and output for design concept below.

```python
from processmapper import ProcessMap, EventType, ActivityType, GatewayType

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


if __name__ == "__main__":
    test_case3()
```

![Process Map](https://github.com/csgoh/processmapper/blob/main/my_process_map_test_case03.png)
