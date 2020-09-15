"""Entrypoint.
"""

import sys

from .app import TilingGui


def main() -> None:
    """The application's starting point."""
    app = TilingGui(sys.argv[1] if len(sys.argv) > 1 else "", resizable=True)
    app.start()


if __name__ == "__main__":
    main()
