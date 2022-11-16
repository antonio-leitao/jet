import argparse
from jet.runner import Runner
from jet.doctor import doctor, JetError
import importlib.metadata

__version__ = importlib.metadata.version("jet")


def dispatcher(a):
    if a["action"] == "run":
        Runner(
            quiet=a["quiet"], run_all=a["all"], default_directory=a["dir"]
        ).run_tests()  # 99!
        return

    if a["action"] == "see":
        doctor(default_directory=a["dir"])
        return

    raise JetError("Unrecognized arguments")


def main():
    """JET simple clean minimalistic testing library.
    Testing library or python with emphasis on presentation and minimalism
    """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "action",
        help="""Jet action: [run, check].
        Either run new tests or diagnose errors from previous ones. Each
        run overwrites previous diagnostics reports. This might change in
        the future
        """,
    )

    parser.add_argument(
        "--all",
        help="""
        Skip initial selection, run all found modules.
        """,
        action="store_true",
    )

    parser.add_argument(
        "--dir",
        help="""
        Path to tests directory. Defaults to working directory + /tests
        when not supplied.
        """,
        metavar="\b",
    )

    parser.add_argument(
        "--quiet",
        help="""
        Disable outputing test results as they run.
        """,
        action="store_true",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    args = vars(parser.parse_args())

    dispatcher(args)


if __name__ == "__main__":
    main()
