import subprocess
import textwrap

def prep_description(desc, indentation, max_length=200, line_width=60):
    # drop new lines
    desc = desc.replace("\n", " ")
    # truncate
    if len(desc) > max_length - 3:
        desc = desc[:max_length] + "..."
        # justify
    desc = textwrap.fill(desc, line_width)
    # add indentation
    desc = textwrap.indent(desc, indentation)
    return desc


def prep_module(mod, indentation, max_length=200, line_width=60):
    title = subprocess.run(
        ["gum", "style", mod["title"]], stdout=subprocess.PIPE
    ).stdout
    desc = subprocess.run(
        [
            "gum",
            "style",
            "--faint",
            prep_description(
                mod["desc"],
                indentation=indentation,
                max_length=max_length,
                line_width=line_width,
            ),
        ],
        stdout=subprocess.PIPE,
    ).stdout.splitlines()[0]
    return title + desc


def choose_modules(
    modules, color="38", indentation="      ", max_length=200, line_width=60
):
    subprocess.run(["echo"])
    subprocess.run(
        [
            "gum",
            "style",
            "--background",
            "53",  # 161
            "--margin",
            "0 4",
            "--bold",
            " Choose Modules ",
        ]
    )

    subprocess.run(
        [
            "gum",
            "style",
            "--faint",
            "--margin",
            "1 4",
            f"Found {len(modules)} modules",
        ]
    )
    result = subprocess.run(
        [
            "gum",
            "choose",
            "--no-limit",
            "--cursor.foreground",
            color,  # 2274A5
            "--selected.foreground",
            color,
            "--unselected-prefix",
            "[ ] ",
            "--cursor-prefix",
            "[ ] ",
            "--selected-prefix",
            "[\u2713] ",
        ]
        + [
            prep_module(mod, indentation, max_length=max_length, line_width=line_width)
            for mod in modules
        ],
        # [list(self.modules.keys())],
        stdout=subprocess.PIPE,
        text=True,
    )

    ###erases n lines where n is [nA[
    # subprocess.run(["printf '\33[4A[2K\r'"], shell=True)  # 4A2K
    subprocess.run(["printf '\33[5A'"], shell=True)  # moves cursor 5 lines up
    subprocess.run(["printf '\33[J\r'"], shell=True)  # deletes everything to bottom
    return result.stdout.splitlines()[::2]
