# standard library imports
import subprocess
import os
import textwrap
import itertools
import re
import json


# self imports
import jet.ui as ui
from jet.classes import JetConfig, Result, JetError

# dependencies
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.box import MINIMAL
from rich.text import Text
from rich.align import Align
from rich.console import Console

# load json into list of results
def load_results(path: str) -> tuple[list[Result], str]:
    try:
        with open(path + "/jet.results.json", "r") as f:
            results = json.load(f)
    except FileNotFoundError:
        raise JetError("No results to diagnose found. Run jet run to run tests")

    results = [Result(**res) for res in results]

    return results, results["summary"]


# choose a single result#
def choose_result(results: list[Result], summary: str) -> Result:
    return result


# map components to result
def create_report(result: Result) -> list:
    report = []
    report.append(component1(result.name))
    return report


def print_report(report: list, width: int) -> str:
    console = Console()
    with console.capture() as capture:
        for block in report:
            console.print(Panel(block, box=MINIMAL, width=width, expand=True), end="")
    return capture.get()


def display_report(doc: str, pad: int, color: int):
    subprocess.run(
        [
            f"gum",
            "pager",
            "--border-foreground",
            color,
            "--margin",
            f"0 {pad}",
            "--help.margin",
            f"0 {pad}",
            doc,
        ]
    )


def See(config: JetConfig, max_width:int, buffer:) -> None:
    results, summary = load_results(config.dir)
    result = choose_result(results, summary)
    report = create_report(result)
    doc = print_report(report, width)
    display_report(doc, pad = pad, color=config.gum_colors[result.result])
