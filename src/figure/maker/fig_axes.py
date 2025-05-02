import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import xarray as xr
from constants.configuration import (
    CBAR_UNIT,
    CONTOUR_COLOR,
    TITLE_SIZE,
    VECTOR_COLOR,
    VECTOR_LEDEND_VALUE,
    VECTOR_LEGEND_NAME,
    VECTOR_REDUCTION_SCALE,
    Y_LEVELS_BOTTOM,
    Y_LEVELS_TOP,
    plot_contour_label,
)
from constants.constant import (
    CBAR_EXTENTION,
    CBAR_LABEL_LOCATION,
    CBAR_LABEL_SIZE,
    CBAR_TICKS_BASE,
    CBAR_TICKS_INTERVAL,
    CONTOUR_LABEL_SIZE,
    CONTOUR_WIDTH,
    LABEL_FONTSIZE,
    TERRAIN_COLOR,
    TICKS_FONTSIZE,
    VECTOR_HEADAXIS_LENGTH,
    VECTOR_HEADLENGTH,
    VECTOR_HEADWIDTH,
    VECTOR_WIDTH,
)
from figure.property.fig_property import FigureProperties
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable


class FigureAxesController:
    def __init__(self, ax: Axes, props: FigureProperties) -> None:
        self.ax = ax
        self._props = props

    def plot_shading(
        self,
        x_coord: np.ndarray,
        y_coord: np.ndarray,
        array: xr.DataArray,
    ) -> None:
        self.shade = self.ax.contourf(
            x_coord,
            y_coord,
            array,
            levels=self._props.cbar_levels,
            cmap=self._props.colormap,
            extend=CBAR_EXTENTION,
        )

    def plot_colorbar(self, is_auto_ticks=True) -> None:
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.2, axes_class=Axes)
        plt.gcf().add_axes(cax)
        if is_auto_ticks:
            self.cbar = plt.colorbar(
                self.shade, cax=cax, orientation="vertical"
            )
        else:
            ticks = mticker.IndexLocator(
                base=CBAR_TICKS_BASE, offset=CBAR_TICKS_INTERVAL
            )
            self.cbar = plt.colorbar(
                self.shade, cax=cax, ticks=ticks, orientation="vertical"
            )

    def set_cbar_label(self) -> None:
        self.cbar.set_label(
            CBAR_UNIT,
            labelpad=CBAR_LABEL_LOCATION,
            y=1.08,
            rotation=0,
            fontsize=CBAR_LABEL_SIZE,
        )

    def plot_contour(
        self, x_coord: np.ndarray, y_coord: np.ndarray, array: xr.DataArray
    ) -> None:
        self.contour = self.ax.contour(
            x_coord,
            y_coord,
            array,
            levels=self._props.contour_levels,
            linewidths=CONTOUR_WIDTH,
            colors=CONTOUR_COLOR,
        )
        if plot_contour_label:
            self.ax.clabel(
                self.contour,
                levels=self._props.clabel_levels,
                fmt="%.{0[0]}f".format([0]),
                fontsize=CONTOUR_LABEL_SIZE,
            )

    def plot_vector(
        self,
        x_coord: np.ndarray,
        y_coord: np.ndarray,
        u_component: np.ndarray,
        v_component: np.ndarray,
    ) -> None:
        self.vector = self.ax.quiver(
            x_coord,
            y_coord,
            u_component,
            v_component,
            scale=VECTOR_REDUCTION_SCALE,
            color=VECTOR_COLOR,
            width=VECTOR_WIDTH,
            headwidth=VECTOR_HEADWIDTH,
            headlength=VECTOR_HEADLENGTH,
            headaxislength=VECTOR_HEADAXIS_LENGTH,
        )

    def plot_legend_vector(self) -> None:
        self.ax.quiverkey(
            self.vector,
            0.92,
            -0.08,
            VECTOR_LEDEND_VALUE,
            VECTOR_LEGEND_NAME,
            labelpos="E",
            coordinates="axes",
        )

    def fill_terrain_area(
        self, x_coord: np.ndarray, area_array: np.ndarray
    ) -> None:
        self.ax.fill_between(x_coord, 0, area_array, facecolor=TERRAIN_COLOR)

    def set_y_range(self) -> None:
        self.ax.set_ylim(Y_LEVELS_BOTTOM, Y_LEVELS_TOP)
        pass

    def invert_yaxis(self) -> None:
        self.ax.invert_yaxis()

    def set_x_ticks_label(
        self, x_label: list, x_ticks_interval: float, rotation: int
    ) -> None:
        loc = np.arange(0, len(x_label), 1)[::x_ticks_interval]
        self.ax.set_xticks(loc)
        self.ax.set_xticklabels(
            x_label[::x_ticks_interval],
            rotation=rotation,
            fontsize=TICKS_FONTSIZE,
        )

    def set_x_label(self, x_label: str) -> None:
        self.ax.set_xlabel(x_label, fontsize=LABEL_FONTSIZE)

    def set_y_label(self, y_label: str) -> None:
        self.ax.set_ylabel(y_label, fontsize=LABEL_FONTSIZE)

    def set_title(self, title_name: str) -> None:
        self.ax.set_title(title_name, fontsize=TITLE_SIZE)

    def plot_text(self, x_loc: float, y_loc: float, text: str) -> None:
        self.ax.text(
            x_loc,
            y_loc,
            text,
            size=8,
            color="black",
            transform=self.ax.transAxes,
        )

    def save_figure(
        self, fig: Figure, save_dir: str, filename: str, dpi: int
    ) -> None:
        os.makedirs(save_dir, exist_ok=True)
        out_path = os.path.join(save_dir, filename)
        fig.savefig(out_path, dpi=dpi)
