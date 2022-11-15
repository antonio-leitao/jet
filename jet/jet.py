import argparse
from jet.runner import Runner
from doctor import doctor, JetError


def jet():
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
        "-d",
        "--dir",
        help="""
        Path to tests directory. Defaults to working directory + /tests
        when not supplied.
        """,
        metavar="\b",
    )

    args = vars(parser.parse_args())

    if args["action"] == "run":
        Runner(accent_color="134").run_tests()  # 99!

    elif args["action"] == "check":
        doctor()

    else:
        raise JetError("Unrecognized argument, please use one of [run, check]")


if __name__ == "__main__":
    # main(sys.argv[1])
    jet()
