from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from wrf import to_np

from arangement.dataset import ArrayExtraction
from constant import (
    CONTOUR_ADDITION,
    CONTOUR_MULTIPLIER,
    CONTOUR_VARNAME,
    DECIMAL_PLACES,
    GIF_NAME,
    LAT_END,
    LAT_START,
    LON_END,
    LON_START,
    MP4_NAME,
    SHADE_ADDITION,
    SHADE_MULTIPLIER,
    SHADE_VARNAME,
    U_VEXTOR_VARNAME,
    V_VEXTOR_VARNAME,
    VAR_INFO_XLOCATION,
    VAR_INFO_YLOCATION,
    VECTOR_X_MULTIPLIER,
    VECTOR_X_SPARSITY,
    VECTOR_Y_MULTIPLIER,
    VECTOR_Y_SPARSITY,
    Y_MAX,
    Y_MIN,
    cbar_auto_ticks,
    is_p_coord,
    vector_legend_plot,
)
from figure.axes_method import AxesMethod
from figure.calculation import calculate_figsize
from figure.fig_text import TextAquisition
from gif.gif import make_gif_from_imgs
from mp4.video import make_mp4_from_imgs
from util.path import generate_path


class WrfoutVerticalPlot:
    def __init__(self, wrfout_path: str) -> None:
        self.wrfout = ArrayExtraction(wrfout_path)
        self.save_rootdir = generate_path(f"/img/{Path(wrfout_path).stem}")

    def plot_shade(self, ax: AxesMethod, datetime: datetime) -> None:
        shade_array = self.wrfout.get_array_for_shade(
            SHADE_VARNAME, datetime, is_p_coord
        )
        shade_array = np.ma.filled(shade_array, np.nan)
        ax.plot_shading(
            self.wrfout.x_coord,
            self.wrfout.y_coord,
            shade_array * SHADE_MULTIPLIER + SHADE_ADDITION,
        )
        ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        ax.set_cbar_label()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION,
            f"shade    :  {self.wrfout.var_ds.description}",
        )
        self.save_dir += f"_{SHADE_VARNAME}_"

    def plot_contour(self, ax: AxesMethod, datetime: datetime) -> None:
        contour_array = self.wrfout.get_array_for_contour(
            CONTOUR_VARNAME, datetime, is_p_coord
        )
        ax.plot_contour(
            self.wrfout.x_coord,
            self.wrfout.y_coord,
            contour_array * CONTOUR_MULTIPLIER + CONTOUR_ADDITION,
        )
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.03,
            f"contour :  {self.wrfout.var_ds.description}",
        )
        self.save_dir += f"_{CONTOUR_VARNAME}_"

    def plot_vector(self, ax: AxesMethod, datetime: datetime) -> None:
        u_array, v_array = self.wrfout.get_array_for_vector(
            U_VEXTOR_VARNAME, V_VEXTOR_VARNAME, datetime, is_p_coord
        )
        if is_p_coord:
            v_array = v_array * -1
        ax.plot_vector(
            self.wrfout.x_coord[::VECTOR_X_SPARSITY],
            self.wrfout.y_coord[::VECTOR_Y_SPARSITY],
            u_array[::VECTOR_Y_SPARSITY, ::VECTOR_X_SPARSITY]
            * VECTOR_X_MULTIPLIER,
            v_array[::VECTOR_Y_SPARSITY, ::VECTOR_X_SPARSITY]
            * VECTOR_Y_MULTIPLIER,
        )
        if vector_legend_plot:
            ax.plot_legend_vector()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.06,
            f"vector   :  {self.wrfout.var_ds.description}",
        )
        self.save_dir += f"_{U_VEXTOR_VARNAME}_"

    def set_x_ticks(self, ax: AxesMethod) -> None:
        label_bases = self.wrfout.x_tick_labels
        if LAT_START == LAT_END:
            label = [
                round(pair.lon, DECIMAL_PLACES) for pair in to_np(label_bases)
            ]
            rotation = 0
        elif LON_START == LON_END:
            label = [
                round(pair.lat, DECIMAL_PLACES) for pair in to_np(label_bases)
            ]
            rotation = 0
        else:
            label = [
                str(round(pair.lat, DECIMAL_PLACES))
                + ", "
                + str(round(pair.lon, DECIMAL_PLACES))
                for pair in to_np(label_bases)
            ]
            rotation = 15
        ax.set_x_ticks_label(label, rotation)

    def fill_terrain_space(self, ax: AxesMethod) -> None:
        terrain_array = self.wrfout.get_terrain_array()
        ax.fill_designated_area(self.wrfout.x_coord, terrain_array)

    def set_xy_label(self, ax: AxesMethod) -> None:
        if LAT_START == LAT_END:
            ax.set_x_label("Longitude")
        elif LON_START == LON_END:
            ax.set_x_label("Latitude")
        else:
            ax.set_x_label("Latitude, Longitude")
        if is_p_coord:
            ax.set_y_label("Pressure [hPa]")
        else:
            ax.set_y_label("Height [m]")

    def make_figure(
        self,
        datetime: datetime,
        shade_plot=False,
        contour_plot=False,
        vector_plot=False,
    ) -> None:

        fig = plt.figure(figsize=calculate_figsize())
        ax = fig.add_axes((0.11, 0.16, 0.8, 0.8))
        target_ax = AxesMethod(ax)
        if is_p_coord:
            coord = "p_coord"
        else:
            coord = "z_coord"
        self.save_dir = f"{self.save_rootdir}/vertical/{LAT_START}-{LAT_END}_{LON_START}-{LON_END}/{coord}/{Y_MAX}_{Y_MIN}/"
        if shade_plot:
            self.plot_shade(target_ax, datetime)
        if contour_plot:
            self.plot_contour(target_ax, datetime)
        if vector_plot:
            self.plot_vector(target_ax, datetime)
        # plot terrain
        if not is_p_coord:
            self.fill_terrain_space(target_ax)
        # set y range
        target_ax.set_y_range()
        # set ticks and labels
        self.set_x_ticks(target_ax)
        self.set_xy_label(target_ax)
        # set title
        text = TextAquisition(datetime)
        target_ax.set_title(text.get_title_text())
        # invert for pressure coordinate
        if is_p_coord:
            target_ax.invert_yaxis()
        # save figure
        filename = text.get_filename()
        target_ax.save_figure(
            fig=fig, save_dir=self.save_dir, filename=filename
        )
        plt.cla()
        plt.close()

    def make_continuous_figs(
        self,
        shade_plot=False,
        contour_plot=False,
        vector_plot=False,
    ) -> None:
        for datetime in self.wrfout.formatted_dt:
            print(f"Now making {datetime} figure …")
            self.make_figure(
                datetime,
                shade_plot=shade_plot,
                contour_plot=contour_plot,
                vector_plot=vector_plot,
            )
        print("Now making gif …")
        make_gif_from_imgs(self.save_dir, f"{self.save_dir}/{GIF_NAME}.gif")
        print("Now making mp4 …")
        make_mp4_from_imgs(self.save_dir, f"{self.save_dir}/{MP4_NAME}.mp4")
        print("Successfully Completed!")
