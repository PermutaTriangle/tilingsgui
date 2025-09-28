"""Entrypoint."""

import argparse

from .app import TilingGui


def get_args() -> str:
    """Get json argument if any."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j", "--json", type=str, default="", help="start GUI with provided tiling"
    )
    return parser.parse_args().json


def main() -> None:
    """The application's starting point."""
    app = TilingGui(get_args(), resizable=True)  # type: ignore
    app.start()


if __name__ == "__main__":
    main()
