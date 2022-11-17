"""Diagnosis script
Reads Diagnostics file and provides ummary of tests.
Gives detailed results on demand.
"""

import os
import json
import subprocess
from jet.seer import Seer
from jet.test_selection import choose_tests


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

    name = choose_tests(results["tests"], summary=results["summary"]["string"])
    # subprocess.run(["printf '\33[2A'"], shell=True)  # moves cursor 5 lines up
    # subprocess.run(["printf '\33[J\r'"], shell=True)

    # script only continues ifsomething was selected
    if name != "\n":
        for test in results["tests"]:
            if test["name"] == name:
                Seer(
                    max_width=120,
                    result=test["result"],
                    diagnosis=test["diagnosis"],
                    fun_name=test["name"],
                    fun_doc=test["doc"],
                    mod_name=test["module"],
                ).display()
