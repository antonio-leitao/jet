"""Test script finder
Finds all scripts .py that start with test_ in the folder tests.
return all function name too?
"""
import os
import inspect
import importlib.util
import sys
import subprocess
import traceback
import warnings
import json
from tqdm import tqdm
import io
from contextlib import redirect_stdout
import textwrap
import time
from rich.progress import Progress


warnings.filterwarnings("error")


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


def _clean_name(path):
    mod_name = os.path.split(path)[-1].removesuffix(".py").removeprefix("test_")
    mod_name = mod_name.split("_")
    mod_name = " ".join(mod_name)
    return mod_name.capitalize()


# path comes in -> module path, name, description and module
def _get_data(path):
    module = _importfile(path)
    name = _clean_name(path)
    data = {"doc": module.__doc__, "path": path, "module": module}
    return name, data


def _catch(exc, f):
    """type, descriptiom, place, output"""
    out = f.getvalue()
    x = traceback.format_exc()
    details = {
        "type": type(exc).__name__,
        "description": str(exc),
        "place": [i.replace("  ", "") for i in x.split("\n") if i][-2],
        "output": out,
    }
    return details


class Runner:
    def __init__(self):
        self.modules = {}
        self.verbose = 2
        self.colors = {
            "Pass": "green",  # 92m
            "Failed": "red",
            "Warning": "yellow",
            "Error": "gray23",
        }
        self.indentation = "    "
        self.main_color = "#458588"

    def get_modules(self, path=None):
        if path is None:
            path = os.getcwd() + "/tests"
        for dirpath, subdirs, files in os.walk(path):
            for x in files:
                if x.endswith(".py") and x.startswith("test_"):
                    name, data = _get_data(os.path.join(dirpath, x))
                    self.modules[name] = data

    def format_option(self, name, desc=None, max_length=200, line_width=60):
        if desc is None:
            return name
        if len(desc) == 0:
            return name
        # drop new lines
        desc = desc.replace("\n", " ")
        # truncate
        if len(desc) > max_length - 3:
            desc = desc[:max_length] + "..."
        # justify
        desc = textwrap.fill(desc, line_width)
        # add indentation
        desc = textwrap.indent(desc, self.indentation)

        return f"{name}\n\033[3m{desc}\033[0m"

    def choose_modules(self):
        self.get_modules()
        options = [self.format_option(k, v["doc"]) for k, v in self.modules.items()]

        print("Which modules to run?")
        result = subprocess.run(
            [
                "gum",
                "choose",
                "--no-limit",
                "--cursor.foreground",
                self.main_color,  # 2274A5
                "--selected.foreground",
                self.main_color,
                self.format_option("All"),
            ]
            + options,  # [list(self.modules.keys())],
            stdout=subprocess.PIPE,
            text=True,
        )

        choices = self.unformat_option(result.stdout.splitlines())
        return choices

    def unformat_option(self, choice_list):
        choices = [s.split(self.indentation)[0] for s in choice_list]
        return choices

    def fetch_modules(self):
        choices = self.choose_modules()
        if "All" in choices:
            return
        self.modules = {k: v for k, v in self.modules.items() if k in choices}
        return

    def fetch_module_routines(self, module, module_name):
        routines = []
        for key, value in inspect.getmembers(module, inspect.isroutine):
            if key.startswith("test"):
                routine_data = {
                    "routine": value,
                    "name": _clean_name(value.__name__),
                    "doc": value.__doc__ if value.__doc__ is not None else "",
                    "module": module_name,
                }
                routines.append(routine_data)
        return routines

    def fetch_tests(self):
        self.fetch_modules()
        tests = []
        for module_name in self.modules.keys():
            routines = self.fetch_module_routines(
                self.modules[module_name]["module"], module_name
            )
            tests.extend(routines)
        return tests

    def archive_routine_results(self, routine, result, details):
        test_result = {k: v for k, v in routine.items() if k != "routine"}
        test_result["result"] = result
        test_result["diagnosis"] = details
        self.results["tests"].append(test_result)

    def dump_results(self, path="result.json"):
        with open(path, "w") as fp:
            json.dump(self.results, fp)

    def evaluate(self, routine):
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                routine()
            return "Pass", []
        except AssertionError as exc:
            return "Failed", _catch(exc, f)
        except RuntimeWarning as exc:
            return "Warning", _catch(exc, f)
        except Exception as exc:
            return "Error", _catch(exc, f)

    def run_tests(self):
        tests = self.fetch_tests()
        n_tests = len(tests)
        self.results = {
            "summary": {
                "n_tests": n_tests,
                "Pass": 0,
                "Failed": 0,
                "Warning": 0,
                "Error": 0,
            },
            "tests": [],
        }

        with Progress() as progress:
            task = progress.add_task("Running tests", total=n_tests)
            for routine in tests:
                # verbose with some extent
                result, details = self.evaluate(routine["routine"])
                self.results["summary"][result] += 1

                # srchive only errors, warning and fails
                if result != "Pass":
                    self.archive_routine_results(routine, result, details)

                if self.verbose > 1:
                    progress.console.print(self.verbose_two(result, routine["routine"]))
                time.sleep(0.2)
                progress.advance(task)
            progress.console.print(self.verbose_one())

        subprocess.run(["printf '\33[A[2K\r'"], shell=True)  # erase progress line
        self.dump_results()

    def verbose_one(self):
        s = "Summary: "
        for result in ["Pass", "Failed", "Warning", "Error"]:
            n = self.results["summary"][result]
            if n == 0:
                continue
            s += f"[{self.colors[result]}]{str(n)} {result.lower()}[/{self.colors[result]}], "
        return s[:-2]

    def verbose_two(self, result, routine):
        # TODO change color names to init
        doc = routine.__doc__
        if doc is None:
            doc = _clean_name(routine.__name__)

        if result == "Pass":
            tick = "\u2713"
            return f"[{self.colors['Pass']}]{tick}[/{self.colors['Pass']}] {doc}"

        if result == "Failed":
            cross = "\u2717"
            return f"[{self.colors['Failed']}]{cross}[/{self.colors['Failed']}] {doc}"

        else:
            mark = "?"
            return f"[{self.colors['Warning']}]{mark}[/{self.colors['Warning']}] {doc}"


if __name__ == "__main__":
    runner = Runner().run_tests()
