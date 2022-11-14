import time

from rich.progress import Progress
import subprocess

verbose = True

with Progress() as progress:
    task = progress.add_task("Running tests", total=10)
    for job in range(10):
        if verbose:
            progress.console.print(f"[green]\u2713[/green] Working on job #{job}")
        time.sleep(0.2)
        progress.advance(task)
subprocess.run(["printf '\33[A[2K\r'"], shell=True)
