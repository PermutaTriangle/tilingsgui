"""A collection of file and path related functionality.
"""

import json
import pathlib
import shutil
from typing import Any, ClassVar, Dict, Iterable, List

import pyglet

from .events import Observer
from .utils import get_current_time_string


class PathManager:
    """A collection of functions to fetch various paths.
    """

    _ROOT: ClassVar[pathlib.Path] = pathlib.Path(__file__).parent.parent.absolute()
    _TILINGS_GUI: ClassVar[str] = "tilingsgui"
    _RESOURCES: ClassVar[str] = "resources"
    _EXPORTS: ClassVar[str] = "exports"

    @staticmethod
    def as_string(path: pathlib.Path) -> str:
        """Convert a Path object to a string.

        Args:
            path (pathlib.Path): The path to convert.

        Returns:
            str: The path as a string using forward slashes.
        """
        return path.as_posix()

    @staticmethod
    def get_root_abs_path() -> pathlib.Path:
        """Get the absolute path of the project's root directory.

        Returns:
            pathlib.Path: Absolute path of '.'.
        """
        return PathManager._ROOT

    @staticmethod
    def get_resources_abs_path() -> pathlib.Path:
        """Get the absolute path of the project's resource directory.

        Returns:
            pathlib.Path: Absolute path of './resources'.
        """
        return PathManager._ROOT.joinpath(
            PathManager._TILINGS_GUI, PathManager._RESOURCES
        )

    @staticmethod
    def get_png_abs_path() -> pathlib.Path:
        """Get the absolute path of the project's png resource directory.

        Returns:
            pathlib.Path: Absolute path of './resources/img/png'.
        """
        return PathManager._ROOT.joinpath(
            PathManager._TILINGS_GUI, PathManager._RESOURCES, "img", "png"
        )

    @staticmethod
    def get_exports_abs_path() -> pathlib.Path:
        """Get the absolute path of the project's export directory.

        Returns:
            pathlib.Path: Absolute path of './exports'.
        """
        return PathManager._ROOT.joinpath(
            PathManager._TILINGS_GUI, PathManager._EXPORTS
        )


class History(Observer):
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

    def __init__(
        self, dispatchers: Iterable[pyglet.event.EventDispatcher] = ()
    ) -> None:
        """Creates exports folder and file if they don't exists. If they
        do exists, the files content is loaded and used if valid JSON. If
        not, we start with a fresh one.

        Args:
            dispatchers (Iterable[pyglet.event.EventDispatcher]): All dispatchers that
            dispatch events to this obserer. Defaults to an empty tuple.
        """
        super().__init__(dispatchers)
        export_path = PathManager.get_exports_abs_path()
        export_path.mkdir(parents=True, exist_ok=True)

        self._path: pathlib.Path = export_path.joinpath(History._FILE_NAME)
        self._data: List[Dict[str, Any]] = self._get_history_data()

    def on_close(self) -> bool:
        """A handler for the closing of the window event. If any exports have occurred
        this session, add them to the history file. There is a session limit so in case
        the limit is reacehed, the oldest one is removed.

        Returns:
            bool: False as we do not want to consume this event.
        """
        if self._session_has_export():
            with open(self._path.as_posix(), "w") as history_file:
                if len(self._data) > History._MAX_SESSIONS:
                    json.dump(self._data[1:], history_file)
                else:
                    json.dump(self._data, history_file)
            shutil.copy(
                self._path.as_posix(), f"{pathlib.Path.cwd()}/tilings_export.json"
            )
        return False

    def on_export(self, tiling_json: dict) -> bool:
        """Add a tiling json to the current session.

        Args:
            tiling_json (dict): A json representation of a tiling.

        Returns:
            bool: True as this event is unique to this handler.
        """
        if tiling_json is not None:
            self._get_current_session_tiling_list().append(
                History._create_tiling_entry(tiling_json)
            )
        return True

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
            with open(self._path.as_posix(), "r") as history_file:
                data = json.load(history_file)
            data.append(History._get_empty_session_object())
            return data
        except FileNotFoundError:
            self._path.touch()
            return History._get_empty_json_object()
        except json.decoder.JSONDecodeError:
            return History._get_empty_json_object()

    def _get_current_session(self) -> Dict[str, Any]:
        """Retrieve the current session object.

        Returns:
            Dict[str, Any]: The current session dictionary.
        """
        return self._data[-1]

    def _get_current_session_tiling_list(self) -> List:
        """Return the current session's list of tilings.

        Returns:
            List: A list of tiling entries.
        """
        return self._data[-1][History._TILINGS]

    def _session_has_export(self) -> bool:
        """Check if any exports have taken place this session.

        Returns:
            bool: True iff the user has exported this session.
        """
        return bool(self._get_current_session_tiling_list())


class Images:
    """A collection of string constants with names of image files.
    """

    ADD_POINT: ClassVar[str] = "add_point.png"
    ADD_CUSOM: ClassVar[str] = "add_custom.png"
    FACTOR: ClassVar[str] = "factor.png"
    FACTOR_INT: ClassVar[str] = "factor_int.png"
    PLACE_WEST: ClassVar[str] = "place_west.png"
    PLACE_EAST: ClassVar[str] = "place_east.png"
    PLACE_NORTH: ClassVar[str] = "place_north.png"
    PLACE_SOUTH: ClassVar[str] = "place_south.png"
    PPLACE_WEST: ClassVar[str] = "pplace_west.png"
    PPLACE_EAST: ClassVar[str] = "pplace_east.png"
    PPLACE_NORTH: ClassVar[str] = "pplace_north.png"
    PPLACE_SOUTH: ClassVar[str] = "pplace_south.png"
    FUSION_R: ClassVar[str] = "fusion_r.png"
    FUSION_C: ClassVar[str] = "fusion_c.png"
    FUSION_COM_R: ClassVar[str] = "fusion_comp_r.png"
    FUSION_COM_C: ClassVar[str] = "fusion_comp_c.png"
    MOVE: ClassVar[str] = "move.png"
    UNDO: ClassVar[str] = "undo.png"
    REDO: ClassVar[str] = "redo.png"
    STR: ClassVar[str] = "str.png"
    VERIFICATION: ClassVar[str] = "verification.png"
    ROWCOLSEP: ClassVar[str] = "rowcolsep.png"
    OBSTR_TRANS: ClassVar[str] = "obstr_trans.png"
    EXPORT: ClassVar[str] = "export.png"
    SEQUENCE: ClassVar[str] = "sequence.png"
    SHADING: ClassVar[str] = "shading.png"
    PRETTY: ClassVar[str] = "pretty.png"
    SHOW_CROSS: ClassVar[str] = "show_cross.png"
    SHOW_LOCAL: ClassVar[str] = "show_local.png"
    HTC: ClassVar[str] = "htc.png"
    TIKZ: ClassVar[str] = "tikz.png"
    OBSTR_INF: ClassVar[str] = "obs_inf.png"
