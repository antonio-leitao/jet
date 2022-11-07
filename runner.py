"""Test script finder
Finds all scripts .py that start with test_ in the folder tests.
return all function name too?
"""
import os
import inspect
import importlib.util
import sys


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


def get_modules(path=None):
    if path is None:
        path = os.getcwd() + "/tests"
    mods = []
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if x.endswith(".py") and x.startswith("test_"):
                mods.append(os.path.join(dirpath, x))
    return mods


# COLLECT EVERYTHING FIRST IN ORDER TO BE ABLE TO RUN A PROGRESS BAR


def get_routines(module):
    routines = []
    object = _importfile(module)
    for key, value in inspect.getmembers(object, inspect.isroutine):
        if key.startswith("test"):
            routines.append(value)
        # print("KEY: ", value.__name__)
        # print("DOC: ", value.__doc__)
        # print("------")
        # run test and log all stuff (maybe its gonna be necessary)
    return routines


# for module in get_modules():
#     mod_name = os.path.split(module)[-1]
#     print("NAME:", mod_name.removesuffix(".py").removeprefix("test_"))
#     for routine in get_routines(module):
#         print(routine.__name__)


def clean_module_name(module):
    mod_name = os.path.split(module)[-1].removesuffix(".py").removeprefix("test_")
    mod_name = mod_name.split("_")
    mod_name = " ".join(mod_name)
    return mod_name.capitalize()


test = "/Users/antonio/Documents/Projects/NAU_NauTesting/tests/test_array_operations.py"

print(clean_module_name(test))
