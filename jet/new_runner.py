"""Test script finder
Finds all scripts .py that start with test_ in the folder tests.
return all function name too?
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

# self imports
import ui as ui
import checks as jetcheck
from classes import JetConfig, Module, Test, Result

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


def _catch(result, doc, captured_output, exception, info, variables) -> Result:
    details = Result(
        result=result,
        doc=doc,
        alias=type(exception).__name__,
        description=str(exception),
        out=captured_output.getvalue(),
        variables=_clean_variables(variables),
        line=info.lineno,
        mod_path=info.filename,
    )

    return details


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


def filter_modules(modules: list[Module], color: str) -> list[Module]:

    choices = ui.choose(
        titles=[mod.name for mod in modules],
        descriptions=[mod.doc for mod in modules],
        summary=f"Found {len(modules)} modules",
        add_all=True,
        all_description="Run all test modules",
        limit=None,
        color=color,
    )
    if "All" in choices:
        return modules[1:]

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
            )

            tests.append(test)

    return tests


def run_tests(
    tests: list[Test],
    show_percentage: bool,
    second_color: str,
    quiet: bool,
    test_colors: dict,
) -> tuple[list[Result], str]:

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
            # run test
            result = evaluate(test)
            # log test result
            tracker[result.result] += 1

            # print results if not verbose
            if not quiet:
                progress.console.print(build_summary_line(result, test_colors))
            # save result if failed
            if result.result != "Pass":
                results.append(result)
            # advance progress bar
            progress.advance(task)

        # print summary
        summary, summary_bw = build_summary(tracker, test_colors)
        if summary != "JET":
            progress.console.print(summary)

    sys.stdout.write("\33[A")
    sys.stdout.write("\33[J\r")
    return results, summary_bw


def do_pre_checks(test: Test) -> Result:
    # add custom tests and checks here.
    result = jetcheck.arguments(test)
    return result


def evaluate(test: Test) -> Result:
    result = do_pre_checks(test)
    if result.result != "Pass":
        return result
    captured_output = io.StringIO()
    try:
        with redirect_stdout(captured_output):
            test.routine()
        return Result(result="Pass", doc=test.doc)
    except AssertionError as exception:
        info = traceback.extract_tb(sys.exc_info()[2])[-1]
        variables = inspect.trace()[-1][0].f_locals
        return _catch("Failed", test.doc, captured_output, exception, info, variables)

    except RuntimeWarning as exception:
        info = traceback.extract_tb(sys.exc_info()[2])[-1]
        variables = inspect.trace()[-1][0].f_locals
        return _catch("Warning", test.doc, captured_output, exception, info, variables)

    except Exception as exception:
        info = traceback.extract_tb(sys.exc_info()[2])[-1]
        variables = inspect.trace()[-1][0].f_locals
        return _catch("Error", test.doc, captured_output, exception, info, variables)


def build_summary(tracker: dict, test_colors: dict) -> tuple[str, str]:
    s = "JET: "
    bw = "JET: "
    for result in ["Pass", "Failed", "Warning", "Error"]:
        n = tracker[result]
        if n == 0:
            continue
        s += f"[{test_colors[result]}]{str(n)} {result.lower()}[/{test_colors[result]}], "
        bw += f"{str(n)} {result.lower()}, "
    return s[:-2], bw[:-2]


def build_summary_line(result: Result, test_colors: dict) -> str:
    doc = result.doc
    if result.result == "Pass":
        tick = "\u2713"
        return f"[{test_colors['Pass']}]{tick}[/{test_colors['Pass']}] {doc}"
    if result.result == "Failed":
        cross = "\u2717"
        return f"[{test_colors['Failed']}]{cross}[/{test_colors['Failed']}] {doc}"
    else:
        mark = "?"
        return f"[{test_colors['Warning']}]{mark}[/{test_colors['Warning']}] {doc}"


def dump_results(results: list[Result], summary: str, path: str) -> None:

    dictionary = {"summary": summary, "tests": [r._asdict() for r in results]}
    with open(path + "/jet.results.json", "w") as fp:
        json.dump(dictionary, fp)


def Run(config: JetConfig) -> None:
    modules = get_modules(config.path, config.files)

    if not config.run_all:
        modules = filter_modules(modules, config.color)

    tests = get_routines(modules)

    # if config.n_jobs ==1:
    results, summary = run_tests(
        tests,
        show_percentage=config.show_percentage,
        second_color=config.second_color,
        quiet=config.quiet,
        test_colors=config.test_colors,
    )

    dump_results(results, summary, config.path)
