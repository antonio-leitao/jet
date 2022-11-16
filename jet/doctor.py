"""Diagnosis script
Reads Diagnostics file and provides ummary of tests.
Gives detailed results on demand.
"""

import os
import json
import subprocess
from rich.console import Console


class JetError(Exception):
    pass


def prompt_diagnostic(online_csv):
    subprocess.run(["echo"])
    subprocess.run(
        [
            "gum",
            "style",
            "--faint",
            " ↑/↓ navigate • enter select • q quit",
        ]
    )

    selected = subprocess.run(
        [f"gum table <<< '{online_csv}' --widths '25,7,70'"],
        text=True,
        shell=True,
        stdout=subprocess.PIPE,
    )
    return selected.stdout.split(",")[0]


def doctor(default_directory=None):
    if default_directory is None:
        default_directory = os.getcwd() + "/tests"

    try:
        with open(default_directory + "/jet.results.json", "r") as f:
            results = json.load(f)
    except FileNotFoundError:
        raise JetError("No results to diagnose found. Run jet run to run tests")

    name = prompt_diagnostic(online_csv=results["online"])
    subprocess.run(["printf '\33[2A'"], shell=True)  # moves cursor 5 lines up
    subprocess.run(["printf '\33[J\r'"], shell=True)

    # script only continues ifsomething was selected
    if name != "\n":
        console = Console()
        for test in results["tests"]:
            if test["name"] == name:
                print(test["diagnosis"]["big_log"])
