import argparse


def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbosely display all scoring report information",
    )
    return parser.parse_args()
