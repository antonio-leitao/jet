import argparse
from runner import Runner
from doctor import doctor


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

    args = vars(parser.parse_args())

    if args["action"] == "run":
        Runner(accent_color="134").run_tests()  # 99!

    if args["action"] == "check":
        doctor()


if __name__ == "__main__":
    # main(sys.argv[1])
    main()
