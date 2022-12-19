# standard
import subprocess
import json

# self imports
import jet_test.ui as ui
from jet_test.report import (
    report_result,
    observation,
    captured_output,
    function_and_locals_inline,
    function_and_locals_parallel,
)
from jet_test.classes import SeeConfig, JetError, Test, Module, Error

# dependencies
from rich.console import Console
from rich.panel import Panel
from rich.box import MINIMAL
from rich.console import Console


def _read_error(result: dict) -> Error:
    error = Error(
        type=result["type"],
        name=result["name"],
        description=result["description"],
        line=result["line"],
        variables=result["variables"],
        out=result["out"],
        test=Test(
            name=result["test"]["name"],
            doc=result["test"]["doc"],
            module=Module(
                name=result["test"]["module"]["name"],
                doc=result["test"]["module"]["doc"],
                path=result["test"]["module"]["path"],
            ),
        ),
    )
    return error


# load json into list of results
def load_results(path: str) -> tuple[list[Error], str]:
    try:
        with open(path + "/jet.results.json", "r") as f:
            results = json.load(f)
    except FileNotFoundError:
        raise JetError("No results to diagnose found. Run jet run to run tests")

    errors = [_read_error(res) for res in results["tests"]]

    return errors, results["summary"]


# choose a single result#
def choose_result(
    results: list[Error], summary: str, foreground: str, background: str
) -> Error:
    choice = ui.choose(
        title_text=" Choose Report ",
        titles=[res.test.name for res in results],
        descriptions=[res.type + ": " + res.description for res in results],
        summary=summary,
        limit=1,
        color=foreground,
        background=background,
    )
    for res in results:
        if res.test.name == choice[0]:
            return res


# map components to result
def create_report(error: Error, config: SeeConfig, color: str) -> list:
    report = [
        report_result(error, color, config.text_width),
        observation("Excpected Behaviour: ", error.test.doc, config.text_width),
    ]

    if error.out:
        report.append(captured_output(error.out, config.text_width))

    if config.doc_width >= 95:
        report.append(
            function_and_locals_parallel(error, config.buffer, color, config.console)
        )
    else:
        report.extend(
            function_and_locals_inline(
                error, config.buffer, color, config.text_width, config.console
            )
        )

    return report


def print_report(report: list, width: int, console: Console) -> str:
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


def See(config: SeeConfig) -> None:
    color_dict = {
        "Pass": config.pass_color,
        "Failed": config.failed_color,
        "Error": config.error_color,
        "Warning": config.warning_color,
    }

    results, summary = load_results(config.path)
    result = choose_result(results, summary, config.foreground, config.background)
    color = color_dict[result.type]
    report = create_report(result, config, color)
    doc = print_report(report, config.doc_width, config.console)
    display_report(doc, pad=config.pad, color=color_dict[result.type])
