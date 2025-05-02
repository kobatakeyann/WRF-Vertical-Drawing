from datetime import datetime
from typing import cast

import numpy as np
import xarray as xr
from wrf import CoordPair, getvar, interpline, vertcross
from wrfout.handler.type import VectorComponent, VertivalCoordinate
from wrfout.loader.nc_dataset import WrfoutNetcdfDataset


class BaseExtractor:
    def __init__(self, loader: WrfoutNetcdfDataset) -> None:
        self.loader = loader
        self.loader.load()

    def get_var_dataarray(
        self, varname: str, datetime: datetime
    ) -> xr.DataArray:
        var_dataarray = cast(
            xr.DataArray,
            getvar(
                self.loader.dataset,
                varname,
                timeidx=self.loader.datetime_index_map[datetime],
            ),
        )
        return var_dataarray

    def get_vertcross_array(
        self,
        var_array: xr.DataArray,
        start_point: CoordPair,
        end_point: CoordPair,
        vertical_coord: VertivalCoordinate,
        levels: np.ndarray,
    ) -> xr.DataArray:
        if vertical_coord == VertivalCoordinate.PRESSURE:
            z = getvar(self.loader.dataset, "p") * 0.01
        elif vertical_coord == VertivalCoordinate.HEIGHT:
            z = getvar(self.loader.dataset, "z")
        else:
            raise ValueError("Invalid vertical coordinate type")
        return vertcross(
            var_array,
            z,
            wrfin=self.loader.dataset,
            start_point=start_point,
            end_point=end_point,
            levels=levels,
            latlon=True,
            meta=True,
        )


class VariableExtractor(BaseExtractor):
    def get_var_array(
        self,
        varname: str,
        datetime: datetime,
        start_point: CoordPair,
        end_point: CoordPair,
        vertical_coord: VertivalCoordinate,
        levels: np.ndarray,
    ) -> xr.DataArray | VectorComponent:
        if varname == "wv_flux":
            wv_flux_uv = self._calc_moisture_flux(datetime)
            u_component, v_component = wv_flux_uv.u, wv_flux_uv.v
            u_vert_array = super().get_vertcross_array(
                u_component,
                start_point,
                end_point,
                vertical_coord,
                levels=levels,
            )
            v_vert_array = super().get_vertcross_array(
                v_component,
                start_point,
                end_point,
                vertical_coord,
                levels=levels,
            )
            return VectorComponent(u_vert_array, v_vert_array)
        var_dataarray = super().get_var_dataarray(varname, datetime)
        return super().get_vertcross_array(
            var_dataarray,
            start_point,
            end_point,
            vertical_coord,
            levels=levels,
        )

    def _calc_moisture_flux(self, datetime: datetime) -> VectorComponent:
        wind_u = super().get_var_dataarray("uvmet", datetime)[0, :, :]
        wind_v = super().get_var_dataarray("uvmet", datetime)[1, :, :]
        mixing_ratio = self.get_var_dataarray("QVAPOR", datetime)
        return VectorComponent(
            mixing_ratio * 1000 * wind_u,
            mixing_ratio * 1000 * wind_v,
        )

    def get_terrain_array(
        self,
        start_point: CoordPair,
        end_point: CoordPair,
    ) -> np.ndarray:
        ter = getvar(self.loader.dataset, "ter")
        return interpline(
            ter,
            wrfin=self.loader.dataset,
            start_point=start_point,
            end_point=end_point,
            latlon=True,
        )
