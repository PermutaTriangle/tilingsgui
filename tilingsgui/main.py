"""Entrypoint.
"""

from .app import TilingGui


def main() -> None:
    """The application's starting point.
    """
    app = TilingGui(resizable=True)
    app.start()


if __name__ == "__main__":
    main()
