import textwrap
import subprocess


def choose(
    titles: list[str],
    descriptions: list[str],
    summary: str,
    limit: int | None,
    color: str,
    add_all: bool = False,
    all_description: None | str = None,
    indentation: str = "      ",
    max_length: int = 200,
    line_width: int = 60,
) -> list | str:

    if add_all:
        titles.insert(0, "All")
        descriptions.insert(0, all_description)
    #if limit ==1 => indentation=0
    items = [
        prep_item(
            title,
            description,
            indentation,
            max_length=max_length,
            line_width=line_width,
        )
        for title, description in zip(titles, descriptions)
    ]

    subprocess.run(["echo"])

    subprocess.run(
        [
            "gum",
            "style",
            "--background",
            "53",  # 161 #color?
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
            summary,
        ]
    )

    command = [
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
        "--unselected-prefix",
        "[ ] ",
        "--cursor-prefix",
        "[ ] ",
        "--selected-prefix",
        "[\u2713] ",
    ] + items

    command += ["--no-limit"] if limit is None else ["--limit", str(limit)]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        text=True,
    )
    subprocess.run(["printf '\33[5A'"], shell=True)  # moves cursor 5 lines up
    subprocess.run(["printf '\33[J\r'"], shell=True)  # deletes everything to bottom
    return result.stdout.splitlines()[::2]


def prep_description(
    description: str, indentation: str, max_length: int, line_width: int
) -> str:
    if description is None:
        description = "..."
    # drop new lines
    description = description.replace("\n", " ")
    # truncate
    if len(description) > max_length - 3:
        description = description[:max_length] + "..."
        # justify
    description = textwrap.fill(description, line_width)
    # add indentation
    description = textwrap.indent(description, indentation)
    return description


def prep_item(
    title: str, description: str, indentation: str, max_length: int, line_width: int
) -> str:
    title = subprocess.run(["gum", "style", title], stdout=subprocess.PIPE).stdout
    desc = subprocess.run(
        [
            "gum",
            "style",
            "--faint",
            prep_description(
                description=description,
                indentation=indentation,
                max_length=max_length,
                line_width=line_width,
            ),
        ],
        stdout=subprocess.PIPE,
    ).stdout.splitlines()[0]
    return title + desc
