import datetime
import re
import os
from processpiper.helper import Helper
from PIL import Image


def parse_and_generate_code(input_str, png_output_file):
    """
    Parse input string and generate code to create a diagram
    """

    # lines = input_str.strip().split("\n")
    lines = [
        line.strip()
        for line in input_str.strip().split("\n")
        if not line.startswith("#") and line.strip()
    ]

    process_map_title = parse_title(lines)

    if len(lines) == 0:
        raise ValueError(
            "No business process definition found. Please add pool(s), lane(s) and element(s)."
        )

    colour_theme = parse_colour_theme(lines)

    code_lines = [
        "from processpiper import ProcessMap, EventType, ActivityType, GatewayType",
        f'with ProcessMap("{process_map_title}") as my_process_map:'
        if colour_theme is None
        else f'with ProcessMap("{process_map_title}", colour_theme="{colour_theme}") as my_process_map:',
    ]

    indent = ""
    pool_id = 1
    lane_id = 0
    pool_found = False
    while lines:
        line = lines.pop(0).strip()
        if line.startswith("pool:"):
            pool_found, pool_id = parse_pool(code_lines, pool_id, line)

        elif line.startswith("lane:"):
            indent, lane_id = parse_lane(code_lines, pool_id, lane_id, pool_found, line)
            parse_element(lines, code_lines, indent, lane_id)

    parse_connection(input_str, code_lines)

    footer = input_str.strip().split("\n")[-1].split("footer:")
    indent = " " * 4
    if len(footer) > 1:
        code_lines.append(f'{indent}my_process_map.set_footer("{footer[1]}")')

    code_lines.append(f"{indent}my_process_map.draw()")
    code_lines.append(f'{indent}my_process_map.save("{png_output_file}")')

    return "\n".join(code_lines)


def parse_element(lines, code_lines, indent, lane_id):
    """
    This function parses an element from a list of lines and adds it to a code block with the
    appropriate indentation.
    """
    while (
        lines
        and not lines[0].strip().startswith("lane:")
        and not lines[0].strip().startswith("pool:")
        and not lines[0].strip().startswith("footer:")
        and lines[0].strip() != ""
    ):
        lane_element = lines.pop(0).strip()
        # check if lane_element contained '->' characters
        if lane_element.find("->") > 0:
            # push lane_element back to lines
            lines.insert(0, lane_element)
            break
        element_type, element_name, element_var = parse_lane_element(lane_element)
        code_lines.append(
            f'{indent}{element_var} = lane{lane_id}.add_element("{element_name}", {element_type})'
        )


def parse_lane(code_lines, pool_id, lane_id, pool_found, line):
    """
    The function parses a lane from a code line and adds it to a process map.
    """
    lane_name = line.split(":")[1].strip()
    lane_id += 1
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

    indent += " " * 4
    return indent, lane_id


def parse_pool(code_lines, pool_id, line):
    """
    This function parses a line of code to extract a pool name and adds it to a list of code lines with
    a specific format.
    """
    pool_name = line.split(":")[1].strip()
    indent = " " * 4
    code_lines.append(
        f'{indent}with my_process_map.add_pool("{pool_name}") as pool{pool_id}:'
    )
    pool_id += 1
    pool_found = True
    return pool_found, pool_id


def parse_connection(input_str, code_lines):
    """
    The function parses a string input containing connection information and generates code lines to
    establish those connections in Python.
    """
    connections_list = [
        line.split("->") for line in input_str.strip().split("\n") if "->" in line
    ]

    for connection in connections_list:
        for i in range(len(connection) - 1):
            element_name, label = get_element_name_and_label(connection[i].strip())
            target_element_name, target_label = get_element_name_and_label(
                connection[i + 1].strip()
            )
            if label:
                code_lines.append(
                    f'        {element_name}.connect({target_element_name}, "{label}")'
                )
            else:
                code_lines.append(
                    f"        {element_name}.connect({target_element_name})"
                )


def get_element_name_and_label(connection: str):
    """
    The function extracts the element name and label from a given connection string using regular
    expressions.
    """
    pattern = r"(\w+)-\"(.*?)\""
    if result := re.search(pattern, connection):
        return result[1], result[2]
    else:
        return connection, None


def parse_colour_theme(lines):
    """
    The function extracts the color theme from a list of lines if it exists.
    """
    return lines.pop(0).split(":")[1].strip() if "colourtheme" in lines[0] else None


def parse_title(lines):
    """
    The function extracts the title from a list of lines if the first line contains the word "title".
    """
    if "title" in lines[0]:
        process_map_title = lines.pop(0).split(":")[1].strip()
    else:
        raise ValueError("The first line must contain the word 'title'.")
    return process_map_title


def parse_lane_element(element_str):
    """
    The function parses a string representing a BPMN element and returns its type, name, and variable
    name.
    """
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


def show_code_with_line_number(code: str):
    """
    The function takes a string of code and prints it with line numbers.
    """
    print("Generated code: ")
    for i, line in enumerate(code.split("\n")):
        print(f"{i+1:3} {line}")


def validate_generated_code(code: str):
    if "add_lane" not in code:
        raise ValueError("There is no lane defined. Please add lanes to process map.")

    ### If a multiline code does not contain add_element, raise error
    if "add_element" not in code:
        raise ValueError("There is no element defined. Please add elements to lane.")


def render(text: str, png_output_file: str = ""):
    """Render text to diagram"""
    output_file_provided = True
    if png_output_file.strip() == "":
        output_file_provided = False
        # add datetime to the file name
        png_output_file = (
            f"piper_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )

    generated_code = parse_and_generate_code(text, png_output_file)
    validate_generated_code(generated_code)
    # show_code_with_line_number(generated_code)
    # print(generated_code)
    exec(generated_code)
    generated_image = Image.open(png_output_file)
    generated_image.load()
    # Clean up the generated image file
    if output_file_provided == False:
        os.remove(png_output_file)

    return generated_code, generated_image
