import os
import sqlite3
from pathlib import Path

import pandas as pd


class SQLiteIO:
    database: str
    _path: Path
    _connection: sqlite3.Connection = None
    _cursor: sqlite3.Cursor

    def __init__(self, path: str | Path) -> None:
        self._path = Path("/".join(str(path).split("/")[:-1]))
        self.database = str(path).split("/")[-1]

        if not os.path.exists(self._path):
            self._create_path()

        if self._connection is None:
            self._create_connection()

    def _create_path(self):
        self._path.mkdir(parents=True, exist_ok=True)

    def _create_connection(self):
        self._connection = sqlite3.connect(self._path / self.database)
        self._cursor = self._connection.cursor()

    def query(self, query: str, params: tuple = ()):
        return self._cursor.execute(query, params)

    def read(self, query: str = None, table_name: str = None):
        if query:
            return pd.read_sql_query(query, con=self._connection)

        return pd.read_sql_query(
            f"SELECT * FROM `{table_name}`", con=self._connection
        )

    def __del__(self):
        if self._connection:
            self._connection.commit()
            self._connection.close()

    def close(self):
        del self
