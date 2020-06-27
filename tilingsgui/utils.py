"""A collection of various utility functionality.
"""

import datetime

import pyperclip


def paste() -> str:
    """Paste what is currently in clipboard. This can fail if os does not
    included required dependencies.
    * Win: None
    * Mac: pbcopy and pbpaste (should be built in)
    * Linux: xclip

    Returns:
        str: The pasted value as a string or an empty string if fails.
    """
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        print("Required clipboard tools for pyperclip missing")
        return ""


def get_current_time_string() -> str:
    """Get the current date and time as a string.

    Returns:
        str: The current datetime.
    """
    return datetime.datetime.now().isoformat()


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Returns the closest value to value in [min_value, max_value].

    Args:
        value (float): The value to map.
        min_value (float): Minimum value of interval.
        max_value (float): Maximum value of interval.

    Returns:
        float: The value clamped between boundaries
    """
    return min(max_value, max(value, min_value))
