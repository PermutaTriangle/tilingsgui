import pathlib
from io import BytesIO

import pyperclip


def paste(warning=False):
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        if warning:
            print("Os does not support required c/p operations")
            print("Try: sudo apt-get install xclip")
        return ""


def get_root_folder():
    return pathlib.Path(__file__).parent.parent.absolute().as_posix()


def get_resource_folder_abs_path():
    return f"{get_root_folder()}/resources"


def get_png_resource_folder_abs_path():
    return f"{get_resource_folder_abs_path()}/img/png"
