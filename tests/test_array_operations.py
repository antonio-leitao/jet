"""Module to test if array operations perform as intended"""


import time
import warnings


def test_addition():
    """Array addition works as intended."""
    time.sleep(0.75)
    pass


def test_array_multiplication():
    """Multiplication also working fine"""
    time.sleep(0.75)
    pass


def test_dot_product():
    """Do product between two arrays"""
    time.sleep(0.75)
    pass


def test_division_by_zero_product():
    """Division by zero should work in this algebra"""
    time.sleep(0.75)
    1 / 0


def test_scalar_multiplication():
    """This other weird test also passed"""
    time.sleep(0.75)
    warnings.warn("This test raised a warning", Warning)


def test_linear_sum():
    """This function adds two different arrays. Arrays are assumed to be of size 3"""
    time.sleep(0.75)
    a = ["banana", "apple", "yellow"]
    b = ["banana", "tomato", "blue", "wheel"]
    print("This is a print function inside the test.")
    print("The output is captured at runtime and stored if the test does not pass.")
    assert len(b) == 3, "This test did not work at all."
