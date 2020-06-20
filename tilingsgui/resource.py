import json
import pathlib
from typing import Any, ClassVar, Dict, List

from .utils import get_current_time_string


class PathManager:
    _ROOT = pathlib.Path(__file__).parent.parent.absolute()
    _RESOURCES = "resources"
    _EXPORTS = "exports"

    @staticmethod
    def get_root_abs_path() -> pathlib.Path:
        return PathManager._ROOT

    @staticmethod
    def get_root_abs_path_str() -> str:
        return PathManager.get_root_abs_path().as_posix()

    @staticmethod
    def get_resources_abs_path() -> pathlib.Path:
        return PathManager._ROOT.joinpath(PathManager._RESOURCES)

    @staticmethod
    def get_resources_abs_path_str() -> str:
        return PathManager.get_resources_abs_path().as_posix()

    @staticmethod
    def get_png_abs_path() -> pathlib.Path:
        return PathManager._ROOT.joinpath(PathManager._RESOURCES, "img", "png")

    @staticmethod
    def get_png_abs_path_str() -> str:
        return PathManager.get_png_abs_path().as_posix()

    @staticmethod
    def get_exports_abs_path() -> pathlib.Path:
        return PathManager._ROOT.joinpath(PathManager._EXPORTS)

    @staticmethod
    def get_exports_abs_path_str() -> str:
        return PathManager.get_exports_abs_path().as_posix()


class ResourceManager:
    pass


class History:
    """A class that handles loading and saving exported tilings.
    """

    _MAX_SESSIONS: ClassVar[int] = 10
    _FILE_NAME: ClassVar[str] = "history.json"
    _SESSION_TIME: ClassVar[str] = "session_time"
    _TILINGS: ClassVar[str] = "tilings"
    _TILING_TIME: ClassVar[str] = "tiling_time"
    _TILING: ClassVar[str] = "tiling"

    @staticmethod
    def _get_empty_session_object() -> Dict[str, Any]:
        """Create an empty session json object.

        Returns:
            Dict[str, Any]: A dictionary for a session.
        """
        return {History._SESSION_TIME: get_current_time_string(), History._TILINGS: []}

    @staticmethod
    def _get_empty_json_object() -> List[Dict[str, Any]]:
        """Create an empty history json object.

        Returns:
            List[Dict[str, Any]]: A list with a single empty session.
        """
        return [History._get_empty_session_object()]

    @staticmethod
    def _create_tiling_entry(tiling_json: dict) -> Dict[str, Any]:
        """Create a tiling entry to add to a session.

        Args:
            tiling_json (dict): A json representation of a tiling.

        Returns:
            Dict[str, Any]: A dictionary with a timestamp and the tiling
        """
        return {
            History._TILING_TIME: get_current_time_string(),
            History._TILING: tiling_json,
        }

    def __init__(self) -> None:
        """Creates exports folder and file if they don't exists. If they
        do exists, the files content is loaded and used if valid JSON. If
        not, we start with a fresh one.
        """
        export_path = PathManager.get_exports_abs_path()
        export_path.mkdir(parents=True, exist_ok=True)

        self.path: pathlib.Path = export_path.joinpath(History._FILE_NAME)
        self.data: List[Dict[str, Any]] = self._get_history_data()

    def save(self) -> None:
        """If any exports have occurred this session, add them to
        the history file. There is a session limit so in case the
        limit is reacehed, the oldest one is removed.
        """
        if self._session_has_export():
            with open(self.path.as_posix(), "w") as history_file:
                if len(self.data) > History._MAX_SESSIONS:
                    json.dump(self.data[1:], history_file)
                else:
                    json.dump(self.data, history_file)

    def add_tiling(self, tiling_json: dict) -> None:
        """Add a tiling json to the current session.

        Args:
            tiling_json (dict): A json representation of a tiling.
        """
        if tiling_json is not None:
            self._get_current_session_tiling_list().append(
                History._create_tiling_entry(tiling_json)
            )

    def _get_history_data(self) -> List[Dict[str, Any]]:
        """Tries to open the export file and retrieve any json object
        from it. If either the directory or file does not exist, it is
        created. If the file does not exists or is invalid, an empty
        export object is returned. Otherwise, the existing object is
        returned.

        Returns:
            List[Dict[str, Any]]: A list of sessions, including the current one.
        """
        try:
            with open(self.path.as_posix(), "r") as history_file:
                data = json.load(history_file)
            data.append(History._get_empty_session_object())
            return data
        except FileNotFoundError:
            self.path.touch()
            return History._get_empty_json_object()
        except json.decoder.JSONDecodeError:
            return History._get_empty_json_object()

    def _get_current_session(self) -> Dict[str, Any]:
        """Retrieve the current session object.

        Returns:
            Dict[str, Any]: The current session dictionary.
        """
        return self.data[-1]

    def _get_current_session_tiling_list(self) -> List:
        """Return the current session's list of tilings.

        Returns:
            List: A list of tiling entries.
        """
        return self.data[-1][History._TILINGS]

    def _session_has_export(self) -> bool:
        """Check if any exports have taken place this session.

        Returns:
            bool: True iff the user has exported this session.
        """
        return bool(self._get_current_session_tiling_list())
