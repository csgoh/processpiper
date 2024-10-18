import os.path
from unittest.mock import patch

import pytest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_test_file_path(filename: str):
    return os.path.join(ROOT_DIR, "data", "results", filename)


def get_solution_file_path(filename: str):
    return os.path.join(ROOT_DIR, "data", "solutions", filename)


def prep_for_test(filename: str):
    path = get_test_file_path(filename)

    if not os.path.exists(path):
        os.mkdir(path)

    output_file = os.path.join(path, filename)

    # remove the file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    return output_file


# Patch get_uuid method
@pytest.fixture
def mock_uuid():
    with patch("processpiper.helper.Helper.get_uuid") as mock_get_uuid:
        # Setup predictable UUIDs
        mock_get_uuid.side_effect = lambda prefix="PIPER": f"{prefix}-1234"
        yield mock_get_uuid
