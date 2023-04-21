![release](https://img.shields.io/pypi/v/processpiper?style=plastic)
![Wheel](https://img.shields.io/pypi/wheel/processpiper?style=plastic)
![Downloads](https://img.shields.io/pypi/dm/processpiper?style=plastic)
![Platforms](https://img.shields.io/badge/Platform%3A-win%20%7C%20ubuntu%20%7C%20osx-brightgreen?style=plastic)
[![license](https://img.shields.io/badge/license-mit-brightgreen.svg?style=plastic)](https://en.wikipedia.org/wiki/MIT_License)
[![CodeFactor](https://www.codefactor.io/repository/github/csgoh/processpiper/badge?style=plastic)](https://www.codefactor.io/repository/github/csgoh/processpiper)
![code size](https://img.shields.io/github/languages/code-size/csgoh/processmapper?style=plastic)
![python version](https://img.shields.io/pypi/pyversions/processpiper?style=plastic)
![stars](https://img.shields.io/github/stars/csgoh/processpiper?style=plastic)
[![Twitter Follow](https://img.shields.io/twitter/follow/CSGohNZ?style=social)](https://twitter.com/CSGohNZ)

# ProcessPiper (Business Process Diagram as Code)
A python library to generate business process diagram using code. 

## Why ProcessPiper?
1. Generate professional business process diagrams with Python code, eliminating the need for manual drawing and complex tools.
2. Improve teamwork by utilising source code repositories for change monitoring, collaboration, and diagram history.
3. Enhance precision by generating diagrams with code, sharing/exporting them in PNG format, and integrating them with Python tools.


# Features
* Generate business process diagrams with Python code
* Alternatively business process diagram can be generated by using plain text
* Business process diagrams contains
  * Diagram title
  * Pool(s)
  * Lane(s)
  * Elements:
    * Event: Start, End, Timer, Intermediate
    * Activity: Task, Subprocess
    * Gateway: Inclusive, Exclusive, Parallel
* Support for different colour themes
  * Default
  * GREYWOOF
  * BLUEMOUNTAIN
  * ORANGEPEEL
  * GREENTURTLE
* Save diagram as PNG file

## Installation
### Install from PyPI
```bash
pip install processpiper
```

### Python version requirements:
* Python 3.10, 3.11
  
### Library Dependencies
* Pillow 9.4.0

### Supported Platforms
* Windows
* Ubuntu
* MacOS

## Documentation
Please refer to [Processpiper Wiki](https://github.com/csgoh/processpiper/wiki) for more information on how to use this RaC library.

## Examples
### (Method 1) Generate diagram using plain text
This is a sample code to generate a business process diagram using plain text. 
```python
from processpiper.text2diagram import render

input_syntax = """
title: Sample Test Process
    lane: End User
        (start) as start
        [Enter Keyword] as enter_keyword
        (end) as end
pool: System Search
    lane: Database System
        [Login] as login
        [Search Records] as search_records
        <Result Found?> as result_found
        [Display Result] as display_result
        [Logout] as logout
    lane: Log System
        [Log Error] as log_error

start->login->enter_keyword->search_records->result_found->display_result->logout->end
result_found->log_error->display_result

footer: Generated by ProcessPiper
"""

render(input_syntax, "my_process_map.png")

```

### (Method 2) Generate diagram using Python code
This is a sample code to generate a business process diagram using Python code. The code is self-explanatory. The diagram is generated using the default colour theme.

```python

```python
from processpiper import ProcessMap, EventType, ActivityType, GatewayType

with ProcessMap(
    "Sample Test Process", colour_theme="BLUEMOUNTAIN") as my_process_map:
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
    my_process_map.save("my_process_map.png")
```

The generated diagram is as follows:
![Process Map](https://github.com/csgoh/processpiper/blob/main/images/test/test_auto_case1.png)


## Development Status
Initial first release would only cover the following basic business process elements. Other element types will be introduced in subsequence releases.

* Event: Start, End, Timer, Intermediate
* Activity: Task, Subprocess
* Gateway: Inclusive, Exclusive, Parallel

Any ideas or suggestions, please send it to me via [GitHub Discussions](https://github.com/csgoh/processmapper/discussions).




