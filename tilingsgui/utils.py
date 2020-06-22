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
        return ""


def get_current_time_string() -> str:
    """Get the current date and time as a string.

    Returns:
        str: The current datetime.
    """
    return datetime.datetime.now().isoformat()
