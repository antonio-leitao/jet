from rich.layout import Layout
from rich.console import Console
import subprocess
from rich.panel import Panel
import os
import textwrap
from rich.box import MINIMAL
from rich.text import Text
from rich.align import Align
import itertools
import re


class Seer:
    def __init__(self, result, diagnosis, fun_name, fun_doc, mod_name, max_width=80):
        self.console = Console()
        self.blocks = []
        self.buffer = 8
        self.result = result
        self.diagnosis = diagnosis
        self.fun_name = fun_name
        self.fun_doc = fun_doc
        self.mod_name = mod_name
        self.colors = {
            "Failed": "red3",
            "Error": "orange3",
            "Warning": "yellow",
        }
        self.gum_colors = {"Failed": "160", "Error": "172", "Warning": "11"}

        # term = os.get_terminal_size().columns

        self.GUMPAD = int(max([0, os.get_terminal_size().columns - max_width]) / 2)
        self.MAX_WIDTH = os.get_terminal_size().columns - (12 + 2 * self.GUMPAD)
        self.TEXT_WIDTH = 60

    def _camel_case_split(self, identifier):
        matches = re.finditer(
            ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", identifier
        )
        return " ".join([m.group(0) for m in matches])

    def _bound_text(self, title, desc, max_width=70):
        desc = textwrap.fill(title + desc, max_width)[len(title) :]
        return desc

    def _center(self, node, **kwargs):
        node = Align(node, vertical="middle", align="center", pad=False, **kwargs)
        return node

    def report_result(self):
        color = self.colors[self.result]

        if self.result == "Failed":
            result = f" TEST FAILED "
        else:
            result = self._camel_case_split(self.diagnosis["type"])
            result = f" {result.upper()} "

        diag = self.diagnosis["description"]

        if len(diag) == 0:
            node = self._center(
                Text(result, style=f"bold white on {color}"),
            )
            self.blocks.append(node)
            return
        node = self._center(
            Text.assemble(
                (result, f"bold white on {color}"),
                ("\n\n"),
                (self._bound_text(result, diag), f"dim {color}"),
                justify="center",
            ),
        )
        self.blocks.append(node)
        return

    def observation(self, title, desc):
        node = self._center(
            Text.assemble(
                title,
                (self._bound_text(title, desc), "dim"),
                justify="left",
            ),
        )
        self.blocks.append(node)

    def captured_output(self):

        if len(self.diagnosis["out"]) == 0:
            return

        node = self._center(
            Panel(
                self._center(Text("\n" + self.diagnosis["out"])),
                subtitle="",
                title="Captured Output",
                width=self.TEXT_WIDTH + 4,
                border_style="dim",
            )
        )
        self.blocks.append(node)

    def locals_panel(self):
        variables = self.diagnosis["locals"]
        if (variables is None) or len(variables) == 0:
            self.console.height = self.buffer + 5
            return self._center(Text(""))
        count = 0
        text = Text()
        for k, v in variables.items():
            text.append(Text(f"{k} = {str(v)}\n", style="dim"))
            # text.append(self.highlight())
            count += 1
        self.console.height = max([self.buffer, count]) + 5
        return self._center(text)

    def function_panel(self):
        color = self.colors[self.result]
        filepath = self.diagnosis["mod_path"]
        lineno = self.diagnosis["line"] - 1
        text = Text()
        start_line = max([lineno - self.buffer, 0])
        current_line = start_line
        with open(filepath, "r") as text_file:
            for line in itertools.islice(text_file, start_line, lineno + 1):
                if current_line == lineno:
                    text.append(line, style=f"bold white on {color}")
                else:
                    text.append(line, style="dim")
                    # text.append(self.highlight(line))
                current_line += 1
        return self._center(text)

    def function_code_and_locals(self, threshold=95):
        if self.MAX_WIDTH >= threshold:
            layout = Layout()
            layout.split_row(
                Layout(
                    Panel(
                        self.function_panel(),
                        title=f"{self.fun_name} @ {self.mod_name}",
                    ),
                    name="code",
                ),
                Layout(
                    Panel(self.locals_panel(), title="Local variables"),
                    name="locals",
                ),
            )
            layout["code"].ratio = 1597
            layout["locals"].ratio = 987
            self.blocks.append(layout)
        else:
            self.blocks.append(
                self._center(
                    Panel(
                        self.function_panel(),
                        title=f"{self.fun_name} @ {self.mod_name}",
                        width=self.TEXT_WIDTH + 4,
                    )
                )
            )
            self.blocks.append(
                self._center(
                    Panel(
                        self.locals_panel(),
                        title="Local variables",
                        width=self.TEXT_WIDTH + 4,
                    )
                )
            )

    def make_report(self):
        self.report_result()
        # these can be added
        self.observation("Expected Behaviour: ", self.fun_doc),
        self.captured_output()
        self.function_code_and_locals()

    def print_report(self):
        self.make_report()
        with self.console.capture() as capture:
            # console.print(layout)
            for block in self.blocks:
                # console_height
                self.console.print(
                    Panel(block, box=MINIMAL, width=self.MAX_WIDTH, expand=True), end=""
                )
        return capture.get()

    def display(self):
        output = self.print_report()

        subprocess.run(
            [
                f"gum",
                "pager",
                "--border-foreground",
                self.gum_colors[self.result],
                "--margin",
                f"0 {self.GUMPAD}",
                "--help.margin",
                f"0 {self.GUMPAD}",
                output,
            ]
        )
