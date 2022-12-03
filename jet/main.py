""":: JET ::
Simple, clean minimalistic testing library.
Testing library for python with emphasis on simplicity and presentation.
"""

import argparse

from new_runner import Run
from classes import JetConfig
import importlib.metadata
import textwrap
import os

#__version__ = importlib.metadata.version("jet")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__doc__),
    )

    parser.add_argument(
        "action",
        help="""Jet action: [run, check].
        Either run new tests or diagnose errors from previous ones. Each
        run overwrites previous diagnostics reports. This might change in
        the future
        """,
        choices=["run", "see"],
        default="run",
    )

    parser.add_argument(
        "-a",
        "--all",
        help="""
        Skip initial selection, run all found modules.
        """,
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="""
        List of modules to consider only instead of entire directory.
        """,
        metavar="\b",
    )

    parser.add_argument(
        "-d",
        "--dir",
        help="""
        Path to tests directory. Defaults to working directory + /tests
        when not supplied.
        """,
        metavar="\b",
        default=os.getcwd() + "/tests",
    )

    parser.add_argument(
        "-j",
        "--jobs",
        help="""
        Number of processes to use in parallel when running tests. Defaults to one.
        """,
        type=int,
        metavar="\b",
        default=1,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="""
        Disable outputing test results as they run.
        """,
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--percentage",
        help="""
        Whether to show progress as a percentage instead of count.
        """,
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--color",
        help="""
        Main color as a 256 color code. Default is 134
        """,
        type=str,
        default="134",
        metavar="\b",
    )

    parser.add_argument(
        "--version",
        action="version",
        #version="%(prog)s {version}".format(version=__version__),
        version=2,
    )

    args = parser.parse_args()

    session = JetConfig(
        path=args.dir,
        files=args.files,
        run_all=args.all,
        quiet=args.quiet,
        color=args.color,
        show_percentage=args.percentage,
        n_jobs=args.jobs,
        second_color="rgb(249,38,114)",
        test_colors={
            "Pass": "green",
            "Failed": "red3",
            "Error": "orange3",
            "Warning": "yellow",
        },
    )

    if args.action == "run":
        Run(config=session)
    # lif args.action =="see":
    #    See(config = session)


if __name__ == "__main__":
    main()
