from datetime import datetime
from math import cos, sin

import netCDF4 as nc
import numpy as np
from numpy import ndarray
from wrf import ALL_TIMES, CoordPair, getvar, interpline, to_np, vertcross
from xarray import DataArray

from constant import (
    INTERPOLATION_INTERVAL,
    LAT_END,
    LAT_START,
    LON_END,
    LON_START,
    Y_MAX,
    Y_MIN,
)
from time_relation.conversion import get_formatted_times


class WrfoutController:
    def __init__(self, wrfout_path: str) -> None:
        self.nc_ds = nc.Dataset(wrfout_path)
        extracted_dt = to_np(getvar(self.nc_ds, "times", timeidx=ALL_TIMES))
        self.formatted_dt = get_formatted_times(extracted_dt)
        self.time_dict = {
            datetime: index for index, datetime in enumerate(self.formatted_dt)
        }

    def get_var_dataset(self, varname: str, datetime: datetime) -> DataArray:
        var_dataset = getvar(
            self.nc_ds, varname, timeidx=self.time_dict[datetime]
        )
        self.var_ds = var_dataset
        return var_dataset

    def get_var_array(self, varname: str, datetime: datetime) -> ndarray:
        var_dataset = self.get_var_dataset(varname, datetime)
        var_array = to_np(var_dataset)
        return var_array

    def get_moisture_flux(self, datetime: datetime) -> None:
        u_wind = self.get_var_array("uvmet", datetime)[0, :, :]
        v_wind = self.get_var_array("uvmet", datetime)[1, :, :]
        mixing_ratio = self.get_var_array("QVAPOR", datetime)
        self.moisture_flux_u = mixing_ratio * u_wind
        self.moisture_flux_v = mixing_ratio * v_wind
        self.var_ds.attrs["description"] = "water vapor flux"


class ArrayExtraction(WrfoutController):
    def get_array_for_shade(
        self, shade_varname: str, datetime: datetime, is_p_coord: bool
    ) -> ndarray:
        if "wv_flux" in shade_varname:
            self.get_moisture_flux(datetime)
            u_data = self.moisture_flux_u
            v_data = self.moisture_flux_v
            wv_flux = (u_data**2 + v_data**2) ** 0.5
            return self.get_vertcross_array(wv_flux, is_p_coord)
        var_array = self.get_var_dataset(shade_varname, datetime)
        return self.get_vertcross_array(var_array, is_p_coord)

    def get_array_for_contour(
        self, contour_varname: str, datetime: datetime, is_p_coord: bool
    ) -> ndarray:
        var_array = self.get_var_dataset(contour_varname, datetime)
        return self.get_vertcross_array(var_array, is_p_coord)

    def get_array_for_vector(
        self,
        u_varname: str,
        v_varname: str,
        datetime: datetime,
        is_p_coord: bool,
    ) -> tuple[ndarray, ndarray]:
        if "wv_flux" in u_varname:
            self.get_moisture_flux(datetime)
            u_component = self.moisture_flux_u
            v_component = self.moisture_flux_v
        else:
            u_array = self.get_var_dataset(u_varname, datetime)
            v_array = self.get_var_dataset(v_varname, datetime)
            if "u_v" in u_array.dims:
                u_component = u_array[0, :, :]
                v_component = u_array[1, :, :]
        delta_lon = LON_END - LAT_START
        delta_lat = LAT_END - LAT_START
        if delta_lat == 0:
            u_array = u_component
        elif delta_lon == 0:
            u_array = v_component
        elif delta_lon < 0:
            raise Exception(
                "Cannot plot vector on vertical cross section. Set start point at left and end point at right."
            )
        else:
            azimuth = np.arctan2(delta_lon, delta_lat)
            u_array = u_component * sin(azimuth) + v_component * cos(azimuth)
        u_vert_array = self.get_vertcross_array(u_array, is_p_coord)
        v_vert_array = self.get_vertcross_array(v_array, is_p_coord)
        return u_vert_array, v_vert_array

    def get_vertcross_array(
        self, var_array: DataArray, is_p_coord: bool
    ) -> ndarray:
        if is_p_coord:
            z = getvar(self.nc_ds, "p") * 0.01
            levels = np.arange(Y_MAX, Y_MIN - 0.001, -INTERPOLATION_INTERVAL)
            print(levels)
        else:
            z = getvar(self.nc_ds, "z")
            levels = np.arange(Y_MIN, Y_MAX, 1)
        start_point = CoordPair(lat=LAT_START, lon=LON_START)
        end_point = CoordPair(lat=LAT_END, lon=LON_END)
        vertcross_array = vertcross(
            var_array,
            z,
            wrfin=self.nc_ds,
            start_point=start_point,
            end_point=end_point,
            levels=levels,
            latlon=True,
            meta=True,
        )
        self.x_coord = np.arange(0, vertcross_array.shape[-1], 1)
        self.y_coord = to_np(vertcross_array.vertical)
        self.x_tick_labels = to_np(vertcross_array.xy_loc)
        return vertcross_array

    def get_terrain_array(self) -> ndarray:
        ter = getvar(self.nc_ds, "ter")
        terrain_line = interpline(
            ter,
            wrfin=self.nc_ds,
            start_point=CoordPair(lat=LAT_START, lon=LON_START),
            end_point=CoordPair(lat=LAT_END, lon=LON_END),
        )
        return to_np(terrain_line)
