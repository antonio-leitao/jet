from typing import NamedTuple, Any


class JetError(Exception):
    pass


# maybe put these somewhere else?
class JetConfig(NamedTuple):
    path: str
    files: list[str]
    run_all: bool
    quiet: bool
    color: str = "134"
    second_color: str = "rgb(249,38,114)"
    show_percentage: bool = False
    n_jobs: int = 1
    test_colors: dict = {
        "Pass": "green",  # 92m
        "Failed": "red3",
        "Error": "orange3",
        "Warning": "yellow",
    }


class Module(NamedTuple):
    name: str
    doc: str
    path: str
    module: Any


class Test(NamedTuple):
    name: str
    doc: str
    routine: Any


class Result(NamedTuple):
    result: str
    doc: str
    alias: str | None = None
    description: str | None = None
    mod_path: str | None = None
    line: str | None = None
    variables: dict | None = None
    out: str | None = None
