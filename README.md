# ProcessMapper

This is a python library to generate business process diagram using code.

```python
from processmapper.lane import ElementType
from processmapper.processmap import ProcessMap


with ProcessMap(600, 150) as my_process_map:
    with my_process_map.add_lane("User") as lane1:
        start = lane1.add_element("Start", ElementType.START)
        activity_1 = lane1.add_element("Login", ElementType.TASK)
        activity_2 = lane1.add_element("Search Records", ElementType.TASK)
        end = lane1.add_element("End", ElementType.END)
    my_process_map.draw()
    my_process_map.save("my_process_map.png")
```

![Process Map](https://raw.githubusercontent.com/abhishekkrthakur/processmapper/master/my_process_map.png)