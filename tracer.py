from rich.console import Console
from runner import Runner
import subprocess


routines = Runner().fetch_tests()


console = Console()

results = {}
for routine in routines:
    with console.capture() as capture:
        try:
            routine["routine"]()
        except Exception as exc:
            # capture error but not from here
            console.print_exception(
                max_frames=1,
                show_locals=True,
                suppress=[__file__],
            )
    results[routine["routine"].__name__] = capture.get()

# print("-----------------------")
# print(results.keys())
# print(results["test_arrays"])

import csv

with open("results_cache.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    cols = list(routines[0].keys())
    writer.writerow(cols)
    for routine in routines:
        writer.writerow([str(routine[k]) for k in cols])

subprocess.run(
    [
        "gum",
        "style",
        "--faint",
        "select for more details q to quit",
    ]
)
selected = subprocess.run(
    [
        f"gum",
        "table",
        "--widths",
        "20,20,20,20",
        "--file",
        "results_cache.csv",
    ],
    stdout=subprocess.PIPE,
    text=True,
)
# Erase Header
subprocess.run(["printf '\33[A[2K\r'"], shell=True)

print(selected.stdout.split(",")[1])
