import argparse
from jet.runner import Runner
from jet.doctor import doctor, JetError
import importlib.metadata

__version__ = importlib.metadata.version("jet")


def job_int(string):
    value = int(string)
    if value < 1:
        msg = "jobs cannot be less than one, received: %r" % string
        raise argparse.ArgumentTypeError(msg)
    if value > 64:
        msg = "jobs have to be less than 64, received: %r" % string
        raise argparse.ArgumentTypeError(msg)
    return value


def dispatcher(a):

    if a["action"] == "run":
        if a["jobs"] is not None:
            Runner(
                quiet=a["quiet"],
                run_all=a["all"],
                default_directory=a["dir"],
                supplied=a["files"],
                n_jobs=a["jobs"],
            ).parallel_run()  # 99!
            return

        Runner(
            quiet=a["quiet"],
            run_all=a["all"],
            default_directory=a["dir"],
            supplied=a["files"],
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
        "-a",
        "--all",
        help="""
        Skip initial selection, run all found modules.
        """,
        action="store_true",
    )

    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="""
        Consider only the specified list of python modules. Path is considered to be relative.
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
    )

    parser.add_argument(
        "-j",
        "--jobs",
        help="""
        Number of processes to use in parallel when running tests. Defaults to one.
        """,
        type=job_int,
        metavar="\b",
    )

    parser.add_argument(
        "-q",
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
