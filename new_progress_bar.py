import time

from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Running Tests", total=10)
    for job in range(10):
        progress.console.print(f"Working on job #{job}")
        time.sleep(0.2)
        progress.advance(task)
