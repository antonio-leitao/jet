import inspect


def _make_details(routine, description):
    details = {
        "mod_path": inspect.getfile(routine),
        "line": inspect.getsourcelines(routine)[1],
        "locals": [],
        "description": description,
        "type": "JetError",
        "out": "",
    }
    return details


def arguments(routine):
    a = inspect.getfullargspec(routine)
    na = len(a.args)
    if na == 0:
        return None, None
    details = _make_details(
        routine,
        "Could not run test. Please supply all arguments as default arguments or none at all",
    )
    if a.defaults is None:
        return "Error", details
    if na != len(a.defaults):
        return "Error", details
    return None, None
