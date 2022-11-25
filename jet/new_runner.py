from typing import NamedTuple, Any
import os
import importlib.util
import sys
import jet.ui as ui

# maybe put these somewhere else?
class JetConfig(NamedTuple):
    path: str
    files: list[str]
    run_all: bool
    quiet: bool
    color: str = "134"
    show_percentage: bool = False
    n_jobs: int = 1


class Module(NamedTuple):
    name: str
    doc: str
    path: str
    module: Any


class Test(NamedTuple):
    name: str
    doc: str
    path: str


class Result(NamedTuple):
    mod_path: str
    line: str
    variables: dict
    doc: str
    alias: str
    out: str


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


def filter_modules(modules: list, color: str) -> list[Module]:

    modules.append(Module(name="Run All", doc="Run all test modules"))



    choices = ui.choose(modules={mod.name: mod.doc for mod in modules},
                        summary = f"Found {len(modules)} modules"
                        color = color,
                        limit = "--no-limit")
    if "Run All" in choices:
       return modules[1:]
    
    return [mod for mod in modules if mod.name in choices]


