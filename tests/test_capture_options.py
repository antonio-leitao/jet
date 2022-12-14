"""Examples on how JET deals with local variables and outputs.
"""
import time
import warnings


def test_passing_test_with_print_function():
    """Standard ouput is blocked by default"""
    time.sleep(0.5)
    print("this is the standard output of a function")


def test_failing_test_with_print_function():
    """Standard ouput is blocked by default"""
    print("this is the standard output of a function")
    time.sleep(0.5)
    a = ["banana", "book", "apple"]
    b = ["banana", "nook", "apple"]
    assert (
        a == b
    ), "If test fails, standard output and local variables be viewed in the report"


def test_error_capturing():
    time.sleep(0.5)
    warnings.warn("This is an example test that raises a warning", Warning)
    pass
