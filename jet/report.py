# standard
import itertools
import re
import textwrap

# self
from classes import Error

# dependencies
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align


def _camel_case_split(identifier: str) -> str:
    matches = re.finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", identifier
    )
    return " ".join([m.group(0) for m in matches])


def _bound_text(title: str, desc: str, text_width: int) -> str:
    desc = textwrap.fill(title + desc, text_width)[len(title) :]
    return desc


def _center(node, **kwargs):
    node = Align(node, vertical="middle", align="center", pad=False, **kwargs)
    return node


def report_result(result: Error, color: str, text_width: int):
    """Creates Headline and description"""
    if result.type == "Failed":
        text = f" TEST FAILED "
    else:
        text = _camel_case_split(result.name)
        text = f" {text.upper()} "

    if len(result.description) == 0:
        node = _center(
            Text(text, style=f"bold white on {color}"),
        )
        return node

    node = _center(
        Text.assemble(
            (text, f"bold white on {color}"),
            ("\n\n"),
            (_bound_text(text, result.description, text_width), f"dim {color}"),
            justify="center",
        ),
    )
    return node


def observation(title: str, desc: str, text_width: int):
    """General class for a fainted block with title"""
    node = _center(
        Text.assemble(
            title,
            (_bound_text(title, desc, text_width), "dim"),
            justify="left",
        ),
    )
    return node


def captured_output(output: str, text_width: int):
    """Display captured output"""
    node = _center(
        Panel(
            _center(Text("\n" + output)),
            subtitle="",
            title="Captured Output",
            width=text_width + 4,
            border_style="dim",
        )
    )
    return node


def locals_panel(result: Error, buffer: int, console):
    if (result.variables is None) or len(result.variables) == 0:
        console.height = buffer + 5
        return _center(Text(""))
    count = 0
    text = Text()
    for k, v in result.variables.items():
        text.append(Text(f"{k} = {str(v)}\n", style="dim"))
        # text.append(self.highlight())
        count += 1
    console.height = max([buffer, count]) + 5
    return _center(text)


def function_panel(result: Error, buffer: int, color: int):

    lineno = result.line - 1
    text = Text()
    start_line = max([lineno - buffer, 0])
    current_line = start_line
    with open(result.test.module.path, "r") as text_file:
        for line in itertools.islice(text_file, start_line, lineno + 1):
            if current_line == lineno:
                text.append(line, style=f"bold white on {color}")
            else:
                text.append(line, style="dim")
            current_line += 1
    return _center(text)


def function_and_locals_parallel(result: Error, buffer: int, color: str, console):
    layout = Layout()
    layout.split_row(
        Layout(
            Panel(
                function_panel(result, buffer, color),
                title=f"{result.test.name} @ {result.test.module.name}",
            ),
            name="code",
        ),
        Layout(
            Panel(locals_panel(result, buffer, console), title="Local variables"),
            name="locals",
        ),
    )
    layout["code"].ratio = 1597
    layout["locals"].ratio = 987
    return layout


def function_and_locals_inline(
    result: Error, buffer: int, color: str, text_width: int, console
):
    uno = _center(
        Panel(
            function_panel(result, buffer, color),
            title=f"{result.test.name} @ {result.test.module.name}",
            width=text_width + 4,
        )
    )
    dos = _center(
        Panel(
            Panel(locals_panel(result, buffer, console), title="Local variables"),
            title="Local variables",
            width=text_width + 4,
        )
    )
    return [uno, dos]
