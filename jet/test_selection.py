import subprocess
import textwrap

##THIS ONE IS COMMON
def prep_description(desc, indentation, max_length=200, line_width=60):
    if desc is None:
        desc = "..."
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


GUM_COLORS = {"Failed": "160", "Error": "172", "Warning": "11"}


def prep_module(test, indentation, max_length=200, line_width=60):
    desc = test["result"] + " : " + test["diagnosis"]["description"]
    title = subprocess.run(
        ["gum", "style", test["name"]], stdout=subprocess.PIPE
    ).stdout
    desc = subprocess.run(
        [
            "gum",
            "style",
            "--faint",
            prep_description(
                desc,
                indentation=indentation,
                max_length=max_length,
                line_width=line_width,
            ),
        ],
        stdout=subprocess.PIPE,
    ).stdout.splitlines()[0]
    return title + desc


def prep_summary(summary):
    s = ""
    for result in ["Failed", "Warning", "Error"]:
        n = summary[result]
        if n == 0:
            continue
        s += f"{str(n)} {result.lower()}, "
    return s + f"out of {summary['n_tests']} tests."


def choose_tests(
    tests, summary, color="134", indentation="  ", max_length=200, line_width=60
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
            " Check Test Details ",
        ]
    )
    subprocess.run(
        [
            "gum",
            "style",
            "--faint",
            "--margin",
            "1 4",
            prep_summary(summary),  # exclude "all"
        ]
    )
    result = subprocess.run(
        [
            "gum",
            "choose",
            "--cursor.foreground",
            color,  # 2274A5
            "--selected.foreground",
            color,
            "--item.margin",
            "0 3",
            "--cursor.margin",
            "0 0",
            "--selected.margin",
            "0 3",
        ]
        + [
            prep_module(test, indentation, max_length=max_length, line_width=line_width)
            for test in tests
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    ###erases n lines where n is [nA[
    # subprocess.run(["printf '\33[4A[2K\r'"], shell=True)  # 4A2K
    subprocess.run(["printf '\33[5A'"], shell=True)  # moves cursor 5 lines up
    subprocess.run(["printf '\33[J\r'"], shell=True)  # deletes everything to bottom
    if len(result.stdout.splitlines()) < 1:
        return
    return result.stdout.splitlines()[0]
