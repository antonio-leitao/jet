""":: JET ::
Simple, clean minimalistic testing library.
Testing library for python with emphasis on simplicity and presentation.
"""

# standard
import argparse
import os
import textwrap
from dataclasses import asdict
import importlib.metadata

# self
from runner import Run
from seer import See
from classes import JetConfig, RunConfig, SeeConfig

# dependencies
from rich.console import Console

# __version__ = importlib.metadata.version("jet")


def add_run_subparser(subparsers):
    run = subparsers.add_parser("run", help="Run tests")
    run.add_argument(
        "-a",
        "--all",
        help="""Run all test modules. Skips intial module selection.
        """,
        action="store_true",
        default=False,
    )
    run.add_argument(
        "-d",
        "--dir",
        help="""Path to tests directory. Defaults to /tests when not supplied.
        """,
        metavar="\b",
        default=os.getcwd() + "/tests",
    )

    run.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="""List of modules to consider only instead of entire directory.
        """,
        metavar="\b",
    )
    run.add_argument(
        "-j",
        "--n-jobs",
        help="""Number of processes to use in parallel when running tests. Defaults to one.
        """,
        type=int,
        default=1,
        metavar="\b",
    )

    run.add_argument(
        "-q",
        "--quiet",
        help="""Disable outputing test results as they run.
        """,
        action="store_true",
        default=False,
    )
    run.add_argument(
        "-p",
        "--percentage",
        help="""Whether to show progress as a percentage instead of count.
        """,
        action="store_true",
    )


def handle_run(args, session):
    config = RunConfig(
        run_all=args.all,
        path=args.dir,
        files=args.files,
        n_jobs=args.n_jobs,
        quiet=args.quiet,
        show_percentage=args.percentage,
        **asdict(session),
    )
    # print(config)
    Run(config=config)


def add_see_subparser(subparsers):
    see = subparsers.add_parser("see", help="See test results")
    see.add_argument(
        "-d",
        "--dir",
        help="""Path to tests directory. Defaults to /tests when not supplied.
        """,
        metavar="\b",
        default=os.getcwd() + "/tests",
    )
    see.add_argument(
        "--doc-width",
        help="""Width (number of columns collumns) of report doc.
        """,
        type=int,
        default=120,
        metavar="\b",
    )

    see.add_argument(
        "--buffer",
        help="""Number of lines of code to show in the report.
        """,
        type=int,
        default=8,
        metavar="\b",
    )

    see.add_argument(
        "--text-width",
        help="""Width (number of columns collumns) of text blocks in report.
        """,
        type=int,
        default=60,
        metavar="\b",
    )


def handle_see(args, session):
    _pad = int(max([0, os.get_terminal_size().columns - args.doc_width]) / 2)

    config = SeeConfig(
        pad=_pad,
        path=args.dir,
        doc_width=os.get_terminal_size().columns - (12 + 2 * _pad),
        text_width=args.text_width,
        buffer=args.buffer,
        console=Console(),
        **asdict(session),
    )
    See(config=config)


def main_parser():
    # default args
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__doc__),
    )
    # default args
    parser.add_argument(
        "--version",
        action="version",
        # version="%(prog)s {version}".format(version=__version__),
        version=2,
    )
    parser.add_argument(
        "--foreground",
        help="Main foreground color",
        type=str,
        default="134",
        metavar="\b",
    )
    parser.add_argument(
        "--background",
        help="Main background color",
        type=str,
        default="53",
        metavar="\b",
    )
    parser.add_argument(
        "--pass-color",
        help="Color for passed tests.",
        type=str,
        default="#008700",  # green
        metavar="\b",
    )
    parser.add_argument(
        "--failed-color",
        help="Color for failed tests.",
        type=str,
        default="#d70000",  # red3
        metavar="\b",
    )
    parser.add_argument(
        "--error-color",
        help="Color for tests that raised unexpected errors.",
        type=str,
        default="#d78700",  # orange3
        metavar="\b",
    )
    parser.add_argument(
        "--warning-color",
        help="Color for tests that result raised warnings.",
        type=str,
        default="#ffff00",  # yellow
        metavar="\b",
    )

    # command args
    subparsers = parser.add_subparsers(dest="command")
    add_run_subparser(subparsers)
    add_see_subparser(subparsers)
    return parser


def main():
    parser = main_parser()
    args = parser.parse_args()

    session = JetConfig(
        foreground=args.foreground,
        background=args.background,
        pass_color=args.pass_color,
        failed_color=args.failed_color,
        error_color=args.error_color,
        warning_color=args.warning_color,
        second_color="rgb(249,38,114)",
    )

    if args.command == "run":
        handle_run(args, session)
    elif args.command == "see":
        handle_see(args, session)


if __name__ == "__main__":
    main()
