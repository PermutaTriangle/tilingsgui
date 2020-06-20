import json
import pathlib

from .utils import get_current_time_string


class PathManager:
    _ROOT = pathlib.Path(__file__).parent.parent.absolute()
    _RESOURCES = "resources"

    @staticmethod
    def get_root_abs_path() -> str:
        return PathManager._ROOT.as_posix()

    @staticmethod
    def get_resources_abs_path() -> str:
        return PathManager._ROOT.joinpath(PathManager._RESOURCES).as_posix()

    @staticmethod
    def get_png_abs_path() -> str:
        return PathManager._ROOT.joinpath(
            PathManager._RESOURCES, "img", "png"
        ).as_posix()


class FileManager:
    pass


class ResourceManager:
    pass


class History:
    @staticmethod
    def get_history_data():
        path = f"{PathManager.get_root_abs_path()}/history.json"
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

    def __init__(self):
        self.data = History.get_history_data()

    def save(self):
        if self.data[-1]["tilings"]:
            path = f"{PathManager.get_root_abs_path()}/history.json"
            with open(path, "w") as f:
                json.dump(self.data, f)

    def add_tiling(self, tiling_json):
        if tiling_json is not None:
            self.data[-1]["tilings"].append(
                {"tiling_time": get_current_time_string(), "tiling": tiling_json}
            )
