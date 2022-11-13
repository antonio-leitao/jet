"""This is a descripiton of a module.
I should probably strip this description of newlines since I imagine that it would be an issue in the end
"""


def test_username(username):
    print("this")
    assert username == "Mike Wazowski"


def test_arrays():
    """Checks differences between arrays"""
    a = ["banana", "book", "apple"]
    b = ["banana", "nook", "apple"]
    assert a == b, "the arrays should be different but aren't"


def test_something_else():
    """This is another that fails"""
    a = ["banana", "book", "apple"]
    b = ["banana", "nook", "apple"]
    assert a == b, "this other test is a fail case"


def test_this_other_thing():
    """This one also fails"""
    a = ["banana", "book", "apple"]
    b = ["banana", "nook", "apple"]
    assert a == b, "this test should be failing"


def test_pass():
    """Should always pass under these configurations"""
    pass


def test_standard_output():
    """This function should always fail and has standard output"""

    print("this is a standard output")
    assert 1 == 2
