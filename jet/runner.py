"""Test script finder
Finds all scripts .py that start with test_ and runs the test functions.
"""
# standard imports
import os
import inspect
import importlib.util
import sys
import traceback
import warnings
import json
import io
from contextlib import redirect_stdout
from typing import Any
from dataclasses import asdict

# self imports
import jet.ui as ui
import jet.checks as jetcheck
from jet.classes import RunConfig, Module, Test, Error

# dependencies
from rich.text import Text
from rich.console import Console
from rich.theme import Theme
from rich.progress import (
    Progress,
    ProgressColumn,
    TaskProgressColumn,
    TextColumn,
    BarColumn,
)

warnings.filterwarnings("error")


class CompletedColumn(ProgressColumn):
    """Renders completed count/total, e.g. '  10/1000'.

    Best for bounded tasks with int quantities.

    Space pads the completed count so that progress length does not change as task progresses
    past powers of 10.

    Args:
        separator (str, optional): Text to separate completed and total values. Defaults to "/".
    """

    def __init__(self, separator="/", table_column=None):
        self.separator = separator
        super().__init__(table_column=table_column)

    def render(self, task):
        """Show completed/total."""
        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        total_width = len(str(total))

        if int(f"{completed:{total_width}d}") == total:
            return Text(
                f"{completed:{total_width}d}{self.separator}{total}",
                style="bar.finished",
            )

        return Text(
            f"{completed:{total_width}d}{self.separator}{total}",
            style="progress.percentage",
        )


class ErrorDuringImport(Exception):
    """Errors that occurred while trying to import something to document it."""

    def __init__(self, filename, exc_info):
        self.filename = filename
        self.exc, self.value, self.tb = exc_info

    def __str__(self):
        exc = self.exc.__name__
        return "problem in %s - %s: %s" % (self.filename, exc, self.value)


def _importfile(path):
    """Import a Python source file or compiled file given its path."""
    magic = importlib.util.MAGIC_NUMBER
    with open(path, "rb") as file:
        is_bytecode = magic == file.read(len(magic))
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    if is_bytecode:
        loader = importlib._bootstrap_external.SourcelessFileLoader(name, path)
    else:
        loader = importlib._bootstrap_external.SourceFileLoader(name, path)
    # XXXWe probably don't need to pass in the loader here.
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    try:
        return importlib._bootstrap._load(spec)
    except:
        raise ErrorDuringImport(path, sys.exc_info())


def _clean_name(path: str) -> str:
    mod_name = os.path.split(path)[-1].removesuffix(".py").removeprefix("test_")
    mod_name = mod_name.replace("_", " ")
    return mod_name.capitalize()


def _get_module_data(path: str) -> Module:
    module = _importfile(path)
    return Module(name=_clean_name(path), doc=module.__doc__, path=path, module=module)


def _is_jsonable(x: Any) -> bool:
    try:
        json.dumps(x)
        return True
    except:
        return False


def _clean_variables(variables: dict) -> dict:
    if variables is None:
        return variables
    if len(variables) == 0:
        return variables

    new_variables = {}
    for k, v in variables.items():
        if hasattr(v, "__name__"):
            v = v.__name__
        elif not _is_jsonable(v):
            v = str(v)
        new_variables[k] = v
    return new_variables


def _track(error: Error, tracker: dict) -> dict:
    if error is None:
        tracker["Pass"] += 1
    else:
        tracker[error.type] += 1
    return tracker


def get_modules(path: str, files: list) -> list[Module]:
    modules = []
    if not files:
        for dirpath, subdirs, files in os.walk(path):
            for x in files:
                if not (x.endswith(".py") and x.startswith("test_")):
                    continue
                modules.append(_get_module_data(os.path.join(dirpath, x)))
        return modules

    for x in files:
        x = os.path.split(x)[-1]
        if not (x.endswith(".py") and x.startswith("test_")):
            continue
        modules.append(_get_module_data(os.path.join(dirpath, x)))
    return modules


def filter_modules(
    modules: list[Module], foreground: str, background: str
) -> list[Module]:

    choices = ui.choose(
        title_text=" Choose Modules ",
        titles=[mod.name for mod in modules],
        descriptions=[mod.doc for mod in modules],
        summary=f"Found {len(modules)} modules",
        add_all=True,
        all_description="Run all test modules",
        limit=None,
        color=foreground,
        background=background,
    )

    if "All" in choices:
        return modules

    return [mod for mod in modules if mod.name in choices]


def get_routines(modules: list[Module]) -> list[Test]:
    tests = []
    for module in modules:
        for key, value in inspect.getmembers(module.module, inspect.isroutine):
            if not key.startswith("test"):
                continue
            test = Test(
                name=_clean_name(value.__name__),
                doc=value.__doc__
                if value.__doc__ is not None
                else _clean_name(value.__name__),
                routine=value,
                module=Module(name=module.name, doc=module.doc, path=module.path),
            )

            tests.append(test)

    return tests


def run_tests(
    tests: list[Test],
    show_percentage: bool,
    second_color: str,
    quiet: bool,
    color_dict: dict,
) -> tuple[list[Error], str]:

    # maybe collapase this as its a bit ugly the second color thing
    console = Console(theme=Theme({"progress.percentage": second_color}))
    progress_column = TaskProgressColumn() if show_percentage else CompletedColumn()
    n_tests = len(tests)
    results = []
    tracker = {
        "n_tests": n_tests,
        "Pass": 0,
        "Failed": 0,
        "Warning": 0,
        "Error": 0,
    }
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        progress_column,
        console=console,
    ) as progress:

        task = progress.add_task("Running tests", total=n_tests)
        for test in tests:
            error = evaluate(test)
            progress.update(task, advance=1, refresh=True)
            tracker = _track(error, tracker)

            if not quiet:
                if error is None:
                    error_type = "Pass"
                    text = test.doc
                else:
                    error_type = error.type
                    text = error.description if error.description else test.name
                progress.console.print(
                    build_summary_line(
                        error_type=error_type,
                        text=text,
                        color_dict=color_dict,
                    )
                )

            if error is not None:
                results.append(error)

        summary, summary_bw = build_summary(tracker, color_dict)
        if summary != "JET":
            progress.console.print(summary)

    sys.stdout.write("\33[A")
    sys.stdout.write("\33[J\r")
    return results, summary_bw


def do_pre_checks(test: Test) -> Error | None:
    # add custom tests and checks here.
    error = jetcheck.arguments(test)
    return error


def evaluate(test: Test) -> Error | None:
    error = do_pre_checks(test)
    if error is not None:
        return error
    captured_output = io.StringIO()
    try:
        with redirect_stdout(captured_output):
            test.routine()
        return None
    except AssertionError as exception:
        info = traceback.extract_tb(sys.exc_info()[2])[-1]
        variables = inspect.trace()[-1][0].f_locals
        return Error(
            type="Failed",
            name=type(exception).__name__,
            description=str(exception),
            line=info.lineno,
            variables=_clean_variables(variables),
            out=captured_output.getvalue(),
            test=Test(name=test.name, doc=test.doc, module=test.module),
        )
    except Warning as exception:
        info = traceback.extract_tb(sys.exc_info()[2])[-1]
        variables = inspect.trace()[-1][0].f_locals
        return Error(
            type="Warning",
            name=type(exception).__name__,
            description=str(exception),
            line=info.lineno,
            variables=_clean_variables(variables),
            out=captured_output.getvalue(),
            test=Test(name=test.name, doc=test.doc, module=test.module),
        )

    except Exception as exception:
        info = traceback.extract_tb(sys.exc_info()[2])[-1]
        variables = inspect.trace()[-1][0].f_locals
        return Error(
            type="Error",
            name=type(exception).__name__,
            description=str(exception),
            line=info.lineno,
            variables=_clean_variables(variables),
            out=captured_output.getvalue(),
            test=Test(name=test.name, doc=test.doc, module=test.module),
        )


def build_summary(tracker: dict, color_dict: dict) -> tuple[str, str]:
    s = "JET: "
    bw = "JET: "
    for result in ["Pass", "Failed", "Error", "Warning"]:
        n = tracker[result]
        if n == 0:
            continue
        s += f"[{color_dict[result]}]{str(n)} {result.lower()}[/{color_dict[result]}], "
        bw += f"{str(n)} {result.lower()}, "
    return s[:-2], bw[:-2]


def build_summary_line(error_type: str, text: str, color_dict: dict) -> str:
    color = color_dict[error_type]
    if error_type == "Pass":
        tick = "\u2713"
        return f"[{color}]{tick}[/{color}] {text}"
    if error_type == "Failed":
        cross = "\u2717"
        return f"[{color}]{cross}[/{color}] {text}"
    if error_type == "Error":
        return f"[{color}]![/{color}] {text}"
    return f"[{color}]?[/{color}] {text}"


def dump_results(results: list[Error], summary: str, path: str) -> None:

    dictionary = {"summary": summary, "tests": [asdict(r) for r in results]}
    with open(path + "/jet.results.json", "w") as fp:
        json.dump(dictionary, fp)


def Run(config: RunConfig) -> None:
    color_dict = {
        "Pass": config.pass_color,
        "Failed": config.failed_color,
        "Error": config.error_color,
        "Warning": config.warning_color,
    }

    modules = get_modules(config.path, config.files)

    if not config.run_all:
        modules = filter_modules(
            modules=modules,
            foreground=config.foreground,
            background=config.background,
        )

    tests = get_routines(modules)

    # if config.n_jobs ==1:
    results, summary = run_tests(
        tests,
        show_percentage=config.show_percentage,
        second_color=config.second_color,
        quiet=config.quiet,
        color_dict=color_dict,
    )
    dump_results(results, summary, config.path)
