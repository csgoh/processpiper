[![CodeFactor](https://www.codefactor.io/repository/github/csgoh/processmapper/badge)](https://www.codefactor.io/repository/github/csgoh/processmapper)

# ProcessMapper

This is a python library to generate business process diagram using code. The intention is adhere to BPMN notation.

It is still under development :construction:

You can see the sample code and output for design concept below.

```python
from processmapper.lane import ElementType
from processmapper.processmap import ProcessMap


with ProcessMap(1150, 220) as my_process_map:
    with my_process_map.add_lane("User") as lane1:
        start = lane1.add_element("Start", ElementType.START)
        login = lane1.add_element("Login", ActivityType.TASK)
        search_records = lane1.add_element("Search Records", ActivityType.TASK)
        result_found = lane1.add_element("Result Found?", GatewayType.EXCLUSIVE)
        display_result = lane1.add_element("Display Result", ActivityType.TASK)
        logout = lane1.add_element("Logout", ActivityType.TASK)
        end = lane1.add_element("End", ElementType.END)

        start.connect(login).connect(search_records).connect(result_found)
        result_found.connect(display_result).connect(logout).connect(end)
        result_found.connect(search_records)
      
    my_process_map.draw()
    my_process_map.save("my_process_map_demo.png")
```

![Process Map](https://github.com/csgoh/processmapper/blob/main/my_process_map_demo.png)
