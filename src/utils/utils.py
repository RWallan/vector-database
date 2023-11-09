import numpy as np

from .constants import TransformTypeEnum


def create_random_vector(range: tuple[int, int], size: int, seed: int = None):
    if seed:
        np.random.seed(seed)

    return np.random.uniform(range[0], range[1], size)


def transform_np_array(array: np.array, type: TransformTypeEnum):
    if TransformTypeEnum(type).value == "list":
        return array.tolist()
    elif TransformTypeEnum(type).value == "bytes":
        return array.tobytes()


def desserialize_bytes_array(array: np.byte):
    return np.frombuffer(array, dtype=np.float64)
