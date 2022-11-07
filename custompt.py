"""Tester class

Receives function and reports its exit status.
"""


def basewrapper(function):
    try:
        function()
    except AssertionError as e:
        print(e.args[0])
        print(function.__doc__)
        print(function.__name__)
        pass


@basewrapper
def testing():
    """tests if lists are the same"""
    a = ["a", "b", "b", "c"]
    b = ["a", "b", "d", "c"]
    assert a == b, "lists are not the same"
