import os
from pathlib import Path

from src.utils.constants import PANDAS_READER, FileExtensionFormat


class LocalIO:
    database: str
    _path: Path

    def __init__(self, path: str | Path) -> None:
        self._path = Path("/".join(str(path).split("/")[:-1]))
        self.database = str(path).split("/")[-1]

        if not os.path.exists(self._path):
            self._create_path()

    def _create_path(self):
        self._path.mkdir(parents=True, exist_ok=True)

    def read(self):
        ext = FileExtensionFormat(os.path.splitext(self.database)[-1]).name
        reader = PANDAS_READER.get(ext)

        return reader(self._path / self.database)
