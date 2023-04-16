def parse_and_generate_code(input_str, png_output_file):
    """Parse input string and generate code to create a diagram"""

    lines = input_str.strip().split("\n")
    if "title" in lines[0]:
        process_map_title = lines.pop(0).split(":")[1].strip()
    else:
        raise ValueError("The first line must contain the word 'title'.")

    colour_theme = None
    if "colourtheme" in lines[0]:
        colour_theme = lines.pop(0).split(":")[1].strip()

    code_lines = [
        "from processpiper import ProcessMap, EventType, ActivityType, GatewayType",
        f'with ProcessMap("{process_map_title}") as my_process_map:'
        if colour_theme is None
        else f'with ProcessMap("{process_map_title}", colour_theme="{colour_theme}") as my_process_map:',
    ]

    indent = ""
    pool_id = 1
    lane_id = 1
    pool_found = False
    while lines:
        line = lines.pop(0).strip()
        if line.startswith("pool:"):
            pool_name = line.split(":")[1].strip()
            indent = " " * 4
            code_lines.append(
                f'{indent}with my_process_map.add_pool("{pool_name}") as pool{pool_id}:'
            )
            pool_id += 1
            pool_found = True

        elif line.startswith("lane:"):
            lane_name = line.split(":")[1].strip()
            if pool_found:
                indent = " " * 8
                code_lines.append(
                    f'{indent}with pool{pool_id - 1}.add_lane("{lane_name}") as lane{lane_id}:'
                )
            else:
                indent = " " * 4
                code_lines.append(
                    f'{indent}with my_process_map.add_lane("{lane_name}") as lane{lane_id}:'
                )
            lane_id += 1

            indent += " " * 4
            while (
                lines
                and not lines[0].strip().startswith("lane:")
                and not lines[0].strip().startswith("pool:")
                and not lines[0].strip().startswith("footer:")
                and not lines[0].strip() == ""
            ):

                lane_element = lines.pop(0).strip()
                element_type, element_name, element_var = parse_lane_element(
                    lane_element
                )
                code_lines.append(
                    f'{indent}{element_var} = lane1.add_element("{element_name}", {element_type})'
                )

    connections_list = [
        line.split("->") for line in input_str.strip().split("\n") if "->" in line
    ]

    for connections in connections_list:
        for i in range(len(connections) - 1):
            code_lines.append(f"        {connections[i]}.connect({connections[i + 1]})")

    footer = input_str.strip().split("\n")[-1].split("footer:")
    indent = " " * 4
    if len(footer) > 1:
        code_lines.append(f'{indent}my_process_map.set_footer("{footer[1]}")')

    code_lines.append(f"{indent}my_process_map.draw()")
    code_lines.append(f'{indent}my_process_map.save("{png_output_file}")')

    return "\n".join(code_lines)


def parse_lane_element(element_str):
    """Detect element type"""
    ### EventType
    if element_str.startswith("(start)"):
        element_type = "EventType.START"
        element_name = element_str[1 : element_str.index(")")].strip()
    elif element_str.startswith("(end)"):
        element_type = "EventType.END"
        element_name = element_str[1 : element_str.index(")")].strip()
    elif element_str.startswith("(@timer"):
        element_type = "EventType.TIMER"
        element_name = element_str[len("(@timer") : element_str.index(")")].strip()
    elif element_str.startswith("(@intermediate"):
        element_type = "EventType.INTERMEDIATE"
        element_name = element_str[
            len("(@intermediate") : element_str.index(")")
        ].strip()
    ### ActivityType
    elif element_str.startswith("[@subprocess"):
        element_type = "ActivityType.SUBPROCESS"
        element_name = element_str[len("[@subprocess") : element_str.index("]")].strip()
    elif element_str.startswith("["):
        element_type = "ActivityType.TASK"
        element_name = element_str[1 : element_str.index("]")].strip()
    ### GatewayType
    elif element_str.startswith("<@parallel"):
        element_type = "GatewayType.PARALLEL"
        element_name = element_str[len("<@parallel") : element_str.index(">")].strip()
    elif element_str.startswith("<@inclusive"):
        element_type = "GatewayType.INCLUSIVE"
        element_name = element_str[len("<@exclusive") : element_str.index(">")].strip()
    elif element_str.startswith("<@exclusive"):
        element_type = "GatewayType.EXCLUSIVE"
        element_name = element_str[len("<@exclusive") : element_str.index(">")].strip()
    elif element_str.startswith("<"):
        element_type = "GatewayType.EXCLUSIVE"
        element_name = element_str[1 : element_str.index(">")].strip()

    else:
        raise ValueError(f"Invalid element string: {element_str}")

    element_var = element_str.split(" as ")[1].strip()

    return element_type, element_name, element_var


def render(text: str, png_output_file: str = "diagram.png"):
    """Render text to diagram"""
    generated_code = parse_and_generate_code(text, png_output_file)
    print(generated_code)
    exec(generated_code)
