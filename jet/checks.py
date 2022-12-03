import inspect
from typing import Any
from classes import Result, Test


def _make_details(test: Test, description: str) -> Result:

    details = Result(
        result="Error",
        doc=test.doc,
        alias="JetError",
        description=description,
        mod_path=inspect.getfile(test.routine),
        out="",
        variables=[],
    )
    return details


def arguments(test: Test) -> Result:
    arguments = inspect.getfullargspec(test.routine)
    if len(arguments.args) == 0:
        return Result(result="Pass", doc=test.doc)
    result = _make_details(
        test,
        "Could not run test. Please supply all arguments as default arguments or none at all",
    )
    if arguments.defaults is None:
        return result
    if len(arguments.args) != len(arguments.defaults):
        return result
    return Result(result="Pass", doc=test.doc)
