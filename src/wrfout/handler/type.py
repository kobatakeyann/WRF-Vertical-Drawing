from enum import Enum, auto
from typing import NamedTuple

import xarray as xr


class VectorComponent(NamedTuple):
    u: xr.DataArray
    v: xr.DataArray


class VertivalCoordinate(Enum):
    PRESSURE = auto()
    HEIGHT = auto()
