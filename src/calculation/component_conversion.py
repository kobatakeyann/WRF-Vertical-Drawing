import warnings
from math import cos, sin

import numpy as np
import xarray as xr
from wrf import CoordPair

_has_warned = False


def xy_components_to_cross_section_component(
    x_component: np.ndarray | xr.DataArray,
    y_component: np.ndarray | xr.DataArray,
    start_point: CoordPair,
    end_point: CoordPair,
) -> np.ndarray:
    if (
        end_point.lon is None
        or end_point.lat is None
        or start_point.lon is None
        or start_point.lat is None
    ):
        raise ValueError(
            "Start and end points must have longitude and latitude."
        )

    delta_lon = end_point.lon - start_point.lon
    delta_lat = end_point.lat - start_point.lat

    if delta_lat == 0:
        return np.array(x_component)
    if delta_lon == 0:
        return np.array(y_component)
    if delta_lon < 0:
        raise Exception(
            "Cannot convert xy-components to component along vertical cross section. Set start point at left and end point at right."
        )

    global _has_warned
    if not _has_warned:
        warnings.warn(
            "This function is only valid for relatively small area because of the simple approximation of the azimuth.",
            UserWarning,
            stacklevel=2,
        )
        _has_warned = True

    azimuth = np.arctan2(delta_lon, delta_lat)
    component_along_cross_section = x_component * sin(
        azimuth
    ) + y_component * cos(azimuth)
    return np.array(component_along_cross_section)
