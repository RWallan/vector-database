import os
from pathlib import Path

import pandas as pd

from src.io import LocalIO


class ETL:
    _raw_data: pd.DataFrame
    database: pd.DataFrame
    _database_file: str
    _output_path: Path
    TOPICS_OF_INTEREST: list[str] = [
        "artificial-intelligence",
        "data-science",
        "machine-learning",
    ]

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._output_path = self.path.parent.parent / "1_intermediate"
        self._database_file = (
            self._split_extension_file(str(self.path).split("/")[-1])
            + ".parquet"
        )

    @staticmethod
    def _split_extension_file(path: str):
        return os.path.splitext(path)[0]

    def read(self):
        self._raw_data = LocalIO(self.path).read()

    def _drop_na(self):
        self._raw_data = self._raw_data.dropna()

    def _remove_truncated_flagged(self):
        self._raw_data = self._raw_data.loc[
            ~self._raw_data["subtitle_truncated_flag"], :
        ]

    def _filter_topics_of_interest(self):
        self._raw_data = self._raw_data.loc[
            self._raw_data["category"].isin(self.TOPICS_OF_INTEREST), :
        ]

    def _create_text_column(self):
        self._raw_data["text"] = (
            self._raw_data["title"] + " " + self._raw_data["subtitle"]
        )

    def _create_metadata_column(self):
        self._raw_data["metadata"] = self._raw_data[
            ["text", "category"]
        ].to_dict(orient="records")

    def _create_id_column(self):
        self._raw_data["id"] = self._raw_data.index.astype(str)

    def _filter_columns_to_write(self):
        self._raw_data = self._raw_data[["id", "text", "metadata"]]

    def transform(self):
        self._drop_na()
        self._remove_truncated_flagged()
        self._filter_topics_of_interest()
        self._create_text_column()
        self._create_metadata_column()
        self._create_id_column()
        self._filter_columns_to_write()

        self.database = self._raw_data

    def write(self):
        self.database.to_parquet(
            self._output_path / self._database_file, index=False
        )

    def pipeline(self):
        self.read()
        self.transform()
        self.write()

        return str(self._output_path)
