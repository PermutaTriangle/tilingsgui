"""Mathematical geometric objects.
"""

from typing import Iterator


class Point:
    """A two dimensional position.
    """

    def __init__(self, x: float, y: float) -> None:
        """Instansiate a point.

        Args:
            x (float): The horizontal coordinate.
            y (float): The vertical coordinate.
        """
        self.x: float = x
        self.y: float = y

    def dist_squared_to(self, other: "Point") -> float:
        """The distance to another point to the second power.

        Args:
            other (Point): The other point, who's distance to we want.

        Returns:
            float: The distance squared.
        """
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def coords(self) -> Iterator[float]:
        """Iterator of the point's coordinates.

        Yields:
            Iterator[float]: The coordinate with x first.
        """
        yield self.x
        yield self.y

    def __iter__(self) -> Iterator[float]:
        """See coords.
        """
        yield from self.coords()


class Rectangle:
    """A rectangle object.
    """

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        """Instansiate a rectangle object.

        Args:
            x (float): The x coordinate of the bottom left corner.
            y (float): The y coordinate of the bottom left corner.
            w (float): The horizontal length of the rectangle.
            h (float): The vertical length of the rectangle.
        """
        self.x: float = x
        self.y: float = y
        self.w: float = w
        self.h: float = h

    def center(self) -> Point:
        """Finds the center point of the rectangle.

        Returns:
            Point: The center of the rectangle.
        """
        return Point(self.x + self.w / 2, self.y + self.h / 2)
