"""Example of how to add new custom failing conditions.
This module shows how to add a custom error condition to your tests.
For example a maximum running time.
"""

import timeit
import time
from functools import wraps


class PatienceError(Exception):
    pass


def timebounded(test_function):
    """Example wrapper for a custom suport.
    Throws an error if the wrapped function exceeds a certain amount of time to run"""

    @wraps(test_function)
    def wrappee():
        elapsed = timeit.timeit(test_function, number=1)
        if elapsed > 0.5:
            raise PatienceError(
                f"CUSTOM ERROR: The function called {test_function.__name__} exceded my patience"
            )

    return wrappee


@timebounded
def test_timings_of_calculation():
    """The function should not exeed 0.5 seconds."""
    time.sleep(1)

