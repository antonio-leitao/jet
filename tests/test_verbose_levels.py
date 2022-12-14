"""Examples of how JET displays test names.
These functions should all pass and show what is written when they don't.
"""

import time


def test_simple_pass():
    """Default output is the function docstring"""
    time.sleep(0.5)
    pass


def test_test_with_no_docstring_displays_its_name():
    time.sleep(0.5)
    pass


def test_simple_test_fail():
    time.sleep(0.5)
    assert 5 == 2, "Error message is displayed if test fails"
