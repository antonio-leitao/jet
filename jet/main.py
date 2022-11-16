import argparse
from jet.runner import Runner
from jet.doctor import doctor, JetError


def dispatcher(a):
    if a["action"] == "run":
        if a["all"]:
            print("running all tests (to be implemenetd")
            return

        if a["dir"] is not None:
            Runner(accent_color="134", default_directory=a["dir"]).run_tests()  # 99!
            return

        Runner(accent_color="134").run_tests()
        return

    if a["action"] == "see":
        if a["dir"] is not None:
            doctor(default_directory=a["dir"])
            return
        doctor()
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
        "-d",
        "--dir",
        help="""
        Path to tests directory. Defaults to working directory + /tests
        when not supplied.
        """,
        metavar="\b",
    )

    args = vars(parser.parse_args())

    dispatcher(args)


if __name__ == "__main__":
    main()
