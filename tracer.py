from rich.console import Console
from runner import Runner
import subprocess


routines = Runner(accent_color="134").fetch_tests()


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

cols = list(routines[0].keys())
online_csv = ",".join(cols) + "\n"
for routine in routines:
    online_csv += ",".join([str(routine[k]) for k in cols]) + "\n"
subprocess.run(
    [
        "gum",
        "style",
        "--faint",
        "select for more details q to quit",
    ]
)


selected = subprocess.run(
    [f"gum table <<< '{online_csv}' --widths '20,20,20,20'"],
    stdout=subprocess.PIPE,
    text=True,
    shell=True,
)
# Erase Header
# subprocess.run(["printf '\33[A[2K\r'"], shell=True)

# print(selected.stdout.split(",")[1])

#results["tests"]["name"/"doc"/"module"]["diagnosis"]