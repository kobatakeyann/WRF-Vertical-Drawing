import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from constants.configuration import (
    CONTOUR_ADDITION,
    CONTOUR_MULTIPLIER,
    SHADE_ADDITION,
    SHADE_MULTIPLIER,
    VECTOR_X_SPARSITY,
    VECTOR_Y_SPARSITY,
    X_TICKS_INTERVAL,
    vector_legend_plot,
)
from constants.constant import (
    DECIMAL_PLACES,
    VAR_INFO_XLOCATION,
    VAR_INFO_YLOCATION,
    VECTOR_X_MULTIPLIER,
    VECTOR_Y_MULTIPLIER,
    cbar_auto_ticks,
)
from figure.maker.fig_axes import FigureAxesController
from figure.property.fig_property import FigureProperties
from wrf import CoordPair, to_np
from wrfout.handler.type import VertivalCoordinate


class Drawer:
    def __init__(self, props: FigureProperties) -> None:
        self._props = props
        self.fig = plt.figure(figsize=self._props.figsize)
        self.ax = self.fig.add_axes((0.11, 0.15, 0.8, 0.8))

    def plot_shade(
        self,
        ax: FigureAxesController,
        x: np.ndarray,
        y: np.ndarray,
        array: xr.DataArray,
        var_description: str,
    ) -> None:
        ax.plot_shading(
            x,
            y,
            array * SHADE_MULTIPLIER + SHADE_ADDITION,
        )
        ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        ax.set_cbar_label()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION,
            f"shade    :  {var_description}",
        )

    def plot_contour(
        self,
        ax: FigureAxesController,
        x: np.ndarray,
        y: np.ndarray,
        array: xr.DataArray,
        var_description: str,
    ) -> None:
        ax.plot_contour(
            x,
            y,
            array * CONTOUR_MULTIPLIER + CONTOUR_ADDITION,
        )
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.03,
            f"contour :  {var_description}",
        )

    def plot_vector(
        self,
        ax: FigureAxesController,
        x: np.ndarray,
        y: np.ndarray,
        u_component: np.ndarray,
        v_component: np.ndarray,
        var_description: str,
    ) -> None:
        ax.plot_vector(
            x[::VECTOR_X_SPARSITY],
            y[::VECTOR_Y_SPARSITY],
            u_component[::VECTOR_Y_SPARSITY, ::VECTOR_X_SPARSITY]
            * VECTOR_X_MULTIPLIER,
            v_component[::VECTOR_Y_SPARSITY, ::VECTOR_X_SPARSITY]
            * VECTOR_Y_MULTIPLIER,
        )
        if vector_legend_plot:
            ax.plot_legend_vector()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.06,
            f"vector   :  {var_description}",
        )

    def set_clean_lonlat_ticks(
        self,
        ax: FigureAxesController,
        x_ticks_labels: xr.DataArray,
        start_point: CoordPair,
        end_point: CoordPair,
    ) -> None:
        if start_point.lat == end_point.lat:
            label = [
                round(pair.lon, DECIMAL_PLACES)
                for pair in to_np(x_ticks_labels)
            ]
            rotation = 0
        elif start_point.lon == end_point.lon:
            label = [
                round(pair.lat, DECIMAL_PLACES)
                for pair in to_np(x_ticks_labels)
            ]
            rotation = 0
        else:
            label = [
                str(round(pair.lat, DECIMAL_PLACES))
                + ", "
                + str(round(pair.lon, DECIMAL_PLACES))
                for pair in to_np(x_ticks_labels)
            ]
            rotation = 15
        ax.set_x_ticks_label(
            x_label=label, x_ticks_interval=X_TICKS_INTERVAL, rotation=rotation
        )

    def set_xy_label(
        self,
        ax: FigureAxesController,
        start_point: CoordPair,
        end_point: CoordPair,
        vert_coord: VertivalCoordinate,
    ) -> None:
        if start_point.lat == end_point.lat:
            ax.set_x_label("Longitude")
        elif start_point.lon == end_point.lon:
            ax.set_x_label("Latitude")
        else:
            ax.set_x_label("Latitude, Longitude")
        if vert_coord == VertivalCoordinate.PRESSURE:
            ax.set_y_label("Pressure [hPa]")
        else:
            ax.set_y_label("Height [m]")
