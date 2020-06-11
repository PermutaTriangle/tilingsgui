"""Entrypoint.
"""

from gui import TilingGui


def main() -> None:
    """The application's starting point.
    """
    app = TilingGui()
    app.initial_configure()
    TilingGui.start()


if __name__ == "__main__":
    main()
