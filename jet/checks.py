# standard imports
import inspect

# self imports
from classes import Error, Test


def _wrap_error(test: Test, description: str) -> Error:

    error = Error(
        type="Error",
        name="JetError",
        description=description,
        line=inspect.getsourcelines(test.routine)[1],
        variables=[],
        out="",
        test=Test(name=test.name, doc=test.doc, module=test.module),
    )
    return error


def arguments(test: Test) -> Error | None:
    arguments = inspect.getfullargspec(test.routine)
    if len(arguments.args) == 0:
        return None
    error = _wrap_error(
        test,
        "Could not run test. Please supply all arguments as default arguments or none at all",
    )
    if arguments.defaults is None:
        return error
    if len(arguments.args) != len(arguments.defaults):
        return error
    return None
