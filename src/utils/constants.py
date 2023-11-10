from enum import Enum
from pathlib import Path
from typing import Callable

import pandas as pd


class TransformTypeEnum(Enum):
    list = "list"
    bytes = "bytes"


class FileExtensionFormat(Enum):
    csv = ".csv"
    parquet = ".parquet"


PANDAS_READER: dict[str, Callable] = {
    "csv": pd.read_csv,
    "parquet": pd.read_parquet,
}

DATADIR: Path = Path(__file__).parent.parent.parent / "data"
