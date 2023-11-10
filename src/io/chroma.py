import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

import pandas as pd
from chromadb import PersistentClient
from chromadb.api.client import Client as ClientCreator
from chromadb.api.models import Collection
from pydantic import BaseModel

from src.utils.constants import DATADIR

from .local import LocalIO


class ChromaDBQueryResult(BaseModel):
    ids: list[list[str]]
    distances: list[list[float]]
    metadatas: list[list[dict[str, str]]]
    embeddings: Optional[str]
    documents: list[list[str]]


class ChromaDBIO:
    _path: Path
    collection_name: str
    chroma_client: ClientCreator = None
    collection: Collection
    directory: Path = DATADIR / "1_intermediate"
    __data: dict = {}

    def __init__(self, path: Path | str) -> None:
        self._path = Path("/".join(str(path).split("/")[:-1]))
        self.collection_name = str(path).split("/")[-1]

        if not os.path.exists(self._path):
            self._create_path()

        if not self.chroma_client:
            self._create_connection()

        self._get_collection()

    def _get_collection(self):
        self.collection = self.chroma_client.get_or_create_collection(
            self.collection_name
        )

    def _create_path(self):
        self._path.mkdir(parents=True, exist_ok=True)

    def _create_connection(self):
        self.chroma_client = PersistentClient(str(self._path))

    def create_collection(self, name: str):
        self.collection_name = name

        self.collection = self.chroma_client.create_collection(
            self.collection_name
        )

    def upsert_data(self, dataframe: str):
        df = LocalIO(self.directory / dataframe).read()

        self.collection.upsert(
            ids=df["id"].tolist()[0:10],
            documents=df["text"].tolist()[0:10],
            metadatas=df["metadata"].tolist()[0:10],
        )

    @lru_cache(maxsize=128)
    def query(self, query: str, *, n_results: int = 1):
        result = self.collection.query(query_texts=query, n_results=n_results)

        return ChromaDBQueryResult(**result)

    def _transform_chromadb_query_to_pandas(self, result: ChromaDBQueryResult):
        self.__data.update(
            {
                "ids": result.ids[0],
                "distances": result.distances[0],
                "documents": result.documents[0],
            }
        )

        tmp = pd.DataFrame(result.metadatas[0])

        return pd.concat([pd.DataFrame(self.__data), tmp], axis=1)

    def read_to_pandas(self, query: str, *, n_results: int = 1):
        result = self.query(query, n_results=n_results)

        return self._transform_chromadb_query_to_pandas(result)
