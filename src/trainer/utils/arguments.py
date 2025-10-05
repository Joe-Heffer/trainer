"""Argument parsing utilities for the trainer CLI."""

import argparse

from trainer import __version__


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="trAIner - Your AI Personal Trainer",
        prog="trainer",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser.parse_args()
