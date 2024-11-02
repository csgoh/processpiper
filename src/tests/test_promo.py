import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from processpiper import text2diagram
from util_test import get_test_file_path


def manual_test_promo():
    input_syntax = """
    title: Sample Test Process
    colourtheme: GREENTURTLE
    lane: End User
        (start) as start
        [Enter Keyword] as enter_keyword
        (end) as end

    start->enter_keyword->end
    """

    output_file = get_test_file_path("test_promo_01.png")

    text2diagram.render(input_syntax, output_file, show_code=True)
