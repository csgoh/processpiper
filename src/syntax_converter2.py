def parse_and_generate_code(input_str):
    lines = input_str.strip().split("\n")
    if "title" in lines[0]:
        process_map_title = lines.pop(0).split(":")[1].strip()
    else:
        raise ValueError("The first line must contain the word 'title'.")

    code_lines = [
        "from processpiper import ProcessMap, EventType, ActivityType, GatewayType",
        f'with ProcessMap("{process_map_title}") as my_process_map:',
    ]

    while lines:
        line = lines.pop(0).strip()
        print(f"line: {line}")
        if line.startswith("pool:"):
            pool_name = line.split(":")[1].strip()
            code_lines.append(
                f'    with my_process_map.add_pool("{pool_name}") as pool1:'
            )
        elif line.startswith("lane:"):
            print(f"    >> lane found {line}")
            lane_name = line.split(":")[1].strip()
            code_lines.append(f'        with pool1.add_lane("{lane_name}") as lane1:')

            while (
                lines
                and not lines[0].strip().startswith("lane:")
                and not lines[0].strip() == ""
            ):
                print(f"    >> lane element found {lines[0].strip()}")
                lane_element = lines.pop(0).strip()
                element_type, element_name, element_var = parse_lane_element(
                    lane_element
                )
                code_lines.append(
                    f'            {element_var} = lane1.add_element("{element_name}", {element_type})'
                )

    # connections = input_str.strip().split("\n")[-1].split("->")
    connections_list = [
        line.split("->") for line in input_str.strip().split("\n") if "->" in line
    ]

    for connections in connections_list:
        print(f"connections: {connections}")
        for i in range(len(connections) - 1):
            code_lines.append(f"        {connections[i]}.connect({connections[i + 1]})")

    code_lines.append("        my_process_map.draw()")
    code_lines.append('        my_process_map.save("src/diagram.png")')

    return "\n".join(code_lines)


def parse_lane_element(element_str):
    if element_str.startswith("(start)"):
        element_type = "EventType.START"
        element_name = element_str[1 : element_str.index(")")].strip()
    elif element_str.startswith("["):
        element_type = "ActivityType.TASK"
        element_name = element_str[1 : element_str.index("]")].strip()
    elif element_str.startswith("<"):
        element_type = "GatewayType.EXCLUSIVE"
        element_name = element_str[1 : element_str.index(">")].strip()
    elif element_str.startswith("(end)"):
        element_type = "EventType.END"
        element_name = element_str[1 : element_str.index(")")].strip()
    else:
        raise ValueError(f"Invalid element string: {element_str}")

    element_var = element_str.split(" as ")[1].strip()

    return element_type, element_name, element_var


input_syntax = """
title: Test Process
pool: System Search
     lane: End User
          (start) as start
          [Enter Keyword] as enter_keyword
          (end) as end
     lane: System
          [Login] as login
          [Search Records] as search_records
          <Result Found?> as result_found
          [Display Result] as display_result
          [Refine Search] as refine_search
          [Logout] as logout

start->login->enter_keyword->search_records->result_found->display_result->logout->end
result_found->refine_search->search_records
"""


generated_code = parse_and_generate_code(input_syntax)
print(generated_code)
with open("src/generated_process_map.py", "w") as f:
    f.write(generated_code)

exec(generated_code)
