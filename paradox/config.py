import argparse


def parse_cli():

    """Parse CLI flags given by user

    Returns:
        argparse.Namespace: Namespace containing user-supplied arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbosely display all scoring report information",
    )
    return parser.parse_args()
