import datetime
import json
import pathlib

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


def get_history_data():
    path = f"{get_root_folder()}/history.json"
    try:
        with open(path, "r") as json_file:
            data = json.load(json_file)
        data.append({"session_time": get_current_time_string(), "tilings": []})
        return data
    except FileNotFoundError:
        pathlib.Path(path).touch()
        return [{"session_time": get_current_time_string(), "tilings": []}]
    except json.decoder.JSONDecodeError:
        return [{"session_time": get_current_time_string(), "tilings": []}]


def save_history_data(data):
    path = f"{get_root_folder()}/history.json"
    with open(path, "w") as f:
        json.dump(data, f)


def get_current_time_string():
    return datetime.datetime.now().isoformat()
