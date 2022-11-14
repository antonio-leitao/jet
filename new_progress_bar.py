import time

from rich.progress import Progress

verbose = False

with Progress() as progress:
    task = progress.add_task("Running tests", total=10)
    for job in range(10):
        if verbose:
            progress.console.print(f"[green]\u2713[/green] Working on job #{job}")
        time.sleep(0.2)
        progress.advance(task)
