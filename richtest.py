import subprocess
import textwrap

indentation = "    "

modules = [
    {"title": "Raspberry Pi’s", "desc": "I have ’em all over my house"},
    {"title": "Nutella", "desc": "It's good on toast"},
    {"title": "Bitter melon", "desc": "It cools you down"},
    {"title": "Nice socks", "desc": "And by that I mean socks without holes"},
    {"title": "Eight hours of sleep", "desc": "I had this once"},
    {"title": "Cats", "desc": "Usually"},
    {"title": "Plantasia, the album", "desc": "My plants love it too"},
    {"title": "Pour over coffee", "desc": "It takes forever to make though"},
    {"title": "VR", "desc": "Virtual reality...what is there to say?"},
    {"title": "Noguchi Lamps", "desc": "Such pleasing organic forms"},
    {"title": "Linux", "desc": "Pretty much the best OS"},
    {"title": "Business school", "desc": "Just kidding"},
    {"title": "Pottery", "desc": "Wet clay is a great feeling"},
    {"title": "Shampoo", "desc": "Nothing like clean hair"},
    {"title": "Table tennis", "desc": "It’s surprisingly exhausting"},
    {"title": "Milk crates", "desc": "Great for packing in your extra stuff"},
    {"title": "Afternoon tea", "desc": "Especially the tea sandwich part"},
    {"title": "Stickers", "desc": "The thicker the vinyl the better"},
    {"title": "20° Weather", "desc": "Celsius, not Fahrenheit"},
    {"title": "Warm light", "desc": "Like around 2700 Kelvin"},
    {"title": "The vernal equinox", "desc": "The autumnal equinox is pretty good too"},
    {"title": "Gaffer’s tape", "desc": "Basically sticky fabric"},
    {"title": "Terrycloth", "desc": "In other words, towel fabric"},
]


def prep_description(desc, max_length=200, line_width=60):
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


def prep_module(mod):
    title = subprocess.run(
        ["gum", "style", mod["title"]], stdout=subprocess.PIPE
    ).stdout

    desc = subprocess.run(
        ["gum", "style", "--faint", prep_description(mod["desc"])],
        stdout=subprocess.PIPE,
    ).stdout.splitlines()[0]
    return title + desc


print("Which modules to run?\n")
result = subprocess.run(
    [
        "gum",
        "choose",
        "--no-limit",
        "--cursor.foreground",
        "38",  # 2274A5
        "--selected.foreground",
        "38",
        "--unselected-prefix",
        "[ ] ",
        "--cursor-prefix",
        "[ ] ",
        "--selected-prefix",
        "[\u2713] ",
    ]
    + [prep_module(mod) for mod in modules],  # [list(self.modules.keys())],
    stdout=subprocess.PIPE,
    text=True,
)

print(result.stdout.splitlines()[::2])
