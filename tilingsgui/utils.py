import datetime

import pyperclip


def paste(warning=False):
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        if warning:
            print("Os does not support required c/p operations")
            print("Linux requires xclip")
        return ""


def get_current_time_string():
    return datetime.datetime.now().isoformat()
