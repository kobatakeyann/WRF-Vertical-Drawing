from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from calculation.component_conversion import (
    xy_components_to_cross_section_component,
)
from constants.configuration import (
    CONTOUR_VARNAME,
    GIF_INTERVAL_TIME,
    GIF_NAME,
    INTERPOLATION_INTERVAL,
    LAT_END,
    LAT_START,
    LON_END,
    LON_START,
    MP4_FPS,
    MP4_NAME,
    SHADE_VARNAME,
    TITLE,
    U_VEXTOR_VARNAME,
    V_VEXTOR_VARNAME,
    VERTICAL_COORDINATE,
    Y_LEVELS_BOTTOM,
    Y_LEVELS_TOP,
    contour_plot,
    shade_plot,
    vector_plot,
)
from constants.constant import IMAGE_DPI, TERRAIN_COLOR
from figure.maker.fig_axes import FigureAxesController
from figure.maker.maker import Drawer
from figure.property.fig_property import FigureProperties
from gif.gif import imgs_to_gif
from mp4.video import imgs_to_mp4
from time_relation.padding import PaddedDatetime
from util.path import generate_path
from wrf import CoordPair, to_np
from wrfout.handler.extraction import VariableExtractor
from wrfout.handler.type import VectorComponent, VertivalCoordinate
from wrfout.information.outputter import WrfoutInformationOutputter
from wrfout.loader.nc_dataset import WrfoutNetcdfDataset


def main():
    # Specify the path to the Wrfout file
    wrfout_path = generate_path("/data/wrfout/high_20220728_d02")

    ### output the information of the Wrfout file
    writer = WrfoutInformationOutputter(wrfout_path)
    writer.output_to_file()

    ### Vizualize
    # create an instance for visualization
    props = FigureProperties()

    # create instances for variable extraction
    loader = WrfoutNetcdfDataset(wrfout_path)
    extractor = VariableExtractor(loader=loader)

    # set latitude and longitude range
    start_point = CoordPair(lat=LAT_START, lon=LON_START)
    end_point = CoordPair(lat=LAT_END, lon=LON_END)

    # set vertical levels
    if VERTICAL_COORDINATE == VertivalCoordinate.PRESSURE:
        vertical_levels = np.arange(
            Y_LEVELS_BOTTOM, Y_LEVELS_TOP - 0.001, -INTERPOLATION_INTERVAL
        )
    elif VERTICAL_COORDINATE == VertivalCoordinate.HEIGHT:
        vertical_levels = np.arange(
            Y_LEVELS_BOTTOM, Y_LEVELS_TOP + 0.001, INTERPOLATION_INTERVAL
        )
    else:
        raise ValueError(
            "Invalid vertical coordinate type. Choose either 'PRESSURE' or 'HEIGHT'."
        )

    # plot at each datetime
    for datetime in loader.datetime_index_map.keys():
        print(f"Now making {datetime} figure …")
        drawer = Drawer(props)
        target_ax = FigureAxesController(ax=drawer.ax, props=props)

        # shade plot
        if shade_plot:
            shade_array = extractor.get_var_array(
                varname=SHADE_VARNAME,
                datetime=datetime,
                start_point=start_point,
                end_point=end_point,
                vertical_coord=VERTICAL_COORDINATE,
                levels=vertical_levels,
            )
            # case of water vapor flux
            if isinstance(shade_array, VectorComponent):
                shade_array = cast(
                    xr.DataArray, np.sqrt(shade_array.u**2 + shade_array.v**2)
                )
                description = "water vapor flux"
            else:
                description = shade_array.description

            # get x, y coordinates
            x_coord = np.arange(0, shade_array.shape[1], 1)
            y_coord = to_np(shade_array.vertical)
            x_ticks_labels = to_np(shade_array.xy_loc)

            # panint terrain area for p-coord
            if VERTICAL_COORDINATE == VertivalCoordinate.PRESSURE:
                target_ax.ax.fill_between(
                    x_coord, y_coord.min(), y_coord.max(), color=TERRAIN_COLOR
                )

            # plot shade
            drawer.plot_shade(
                target_ax,
                x=x_coord,
                y=y_coord,
                array=shade_array,
                var_description=description,
            )

        # contour plot
        if contour_plot:
            contour_array = extractor.get_var_array(
                varname=CONTOUR_VARNAME,
                datetime=datetime,
                start_point=start_point,
                end_point=end_point,
                vertical_coord=VERTICAL_COORDINATE,
                levels=vertical_levels,
            )
            # case of water vapor flux
            if isinstance(contour_array, VectorComponent):
                contour_array = cast(
                    xr.DataArray,
                    np.sqrt(contour_array.u**2 + contour_array.v**2),
                )
                description = "water vapor flux"
            else:
                description = contour_array.description

            # get x, y coordinates
            x_coord = np.arange(0, contour_array.shape[1], 1)
            y_coord = to_np(contour_array.vertical)
            x_ticks_labels = to_np(contour_array.xy_loc)

            # plot contour
            drawer.plot_contour(
                target_ax,
                x=x_coord,
                y=y_coord,
                array=contour_array,
                var_description=description,
            )

        if vector_plot:
            content = extractor.get_var_array(
                varname=U_VEXTOR_VARNAME,
                datetime=datetime,
                start_point=start_point,
                end_point=end_point,
                vertical_coord=VERTICAL_COORDINATE,
                levels=vertical_levels,
            )
            # case of water vapor flux
            if isinstance(content, VectorComponent):
                u_array = content.u
                v_array = content.v
                description = "horizontal water vapor flux"
            # case of array containing u and v components
            elif "u_v" in content.dims:
                u_array = content[0, :, :]
                v_array = content[1, :, :]
                description = "horizontal and vertical wind"
            # case of array containing only single component
            else:
                u_array = content
                v_array = cast(
                    xr.DataArray,
                    extractor.get_var_array(
                        varname=V_VEXTOR_VARNAME,
                        datetime=datetime,
                        start_point=start_point,
                        end_point=end_point,
                        vertical_coord=VERTICAL_COORDINATE,
                        levels=vertical_levels,
                    ),
                )
                description = "horizontal and vertical wind"

            # get x, y coordinates
            x_coord = np.arange(0, u_array.shape[1], 1)
            y_coord = to_np(u_array.vertical)
            x_ticks_labels = to_np(u_array.xy_loc)

            # convert to cross-section component
            x_component = xy_components_to_cross_section_component(
                u_array,
                v_array,
                start_point,
                end_point,
            )
            y_component = cast(
                np.ndarray,
                extractor.get_var_array(
                    varname=V_VEXTOR_VARNAME,
                    datetime=datetime,
                    start_point=start_point,
                    end_point=end_point,
                    vertical_coord=VERTICAL_COORDINATE,
                    levels=vertical_levels,
                ),
            )

            # plot vector
            drawer.plot_vector(
                target_ax,
                x=x_coord,
                y=y_coord,
                u_component=x_component,
                v_component=y_component,
                var_description=description,
            )

        # reverse y-axis when p-coord
        if VERTICAL_COORDINATE == VertivalCoordinate.PRESSURE:
            target_ax.invert_yaxis()

        # paint terrain area for h-coord
        if VERTICAL_COORDINATE == VertivalCoordinate.HEIGHT:
            terrain_array = extractor.get_terrain_array(
                start_point=start_point,
                end_point=end_point,
            )
            target_ax.fill_terrain_area(
                x_coord=x_coord, area_array=terrain_array
            )

        # set ticks and labels
        drawer.set_clean_lonlat_ticks(
            target_ax,
            x_ticks_labels=x_ticks_labels,
            start_point=start_point,
            end_point=end_point,
        )
        drawer.set_xy_label(
            target_ax,
            start_point=start_point,
            end_point=end_point,
            vert_coord=VERTICAL_COORDINATE,
        )

        # title
        padded_dt = PaddedDatetime(datetime)
        filename = f"{padded_dt.year}{padded_dt.month}{padded_dt.day}_{padded_dt.hour}{padded_dt.minute}JST.jpg"
        saving_rootdir = generate_path(f"/img/{Path(wrfout_path).stem}")
        if LAT_START == LAT_END:
            section_location = f"{LON_START}-{LON_END}°E at {LAT_START}°N"
        elif LON_START == LON_END:
            section_location = f"{LAT_START}-{LAT_END}°N at {LON_START}°E"
        else:
            section_location = (
                f"{LAT_START}°N,{LON_START}°E - {LAT_END}°N,{LON_END}°E"
            )
        title = f"{padded_dt.year}/{padded_dt.month}/{padded_dt.day} {padded_dt.hour}{padded_dt.minute}JST  {section_location}   {TITLE}"
        if VERTICAL_COORDINATE == VertivalCoordinate.HEIGHT:
            saving_dir = f"{saving_rootdir}/vertical/{LON_START}_{LON_END}_{LAT_START}_{LAT_END}/h_coord/"
        else:
            saving_dir = f"{saving_rootdir}/vertical/{LON_START}_{LON_END}_{LAT_START}_{LAT_END}/p_coord/"
        target_ax.set_title(title)

        # directory arrangement
        if shade_plot:
            saving_dir += f"_{SHADE_VARNAME}"
        if contour_plot:
            saving_dir += f"_{CONTOUR_VARNAME}"
        if vector_plot:
            saving_dir += f"_{U_VEXTOR_VARNAME}"
        # save
        target_ax.save_figure(
            fig=drawer.fig,
            save_dir=saving_dir,
            filename=filename,
            dpi=IMAGE_DPI,
        )
        plt.cla()
        plt.close()

    # make gif
    print("Now making gif …")
    imgs_to_gif(
        imgs_dir_path=saving_dir,
        saved_gif_path=f"{saving_dir}/{GIF_NAME}.gif",
        gif_interval_time=GIF_INTERVAL_TIME,
    )
    # make mp4
    print("Now making mp4 …")
    imgs_to_mp4(
        imgs_dir_path=saving_dir,
        saved_mp4_path=f"{saving_dir}/{MP4_NAME}.mp4",
        fps=MP4_FPS,
        extension="jpg",
    )
    print("Successfully Completed!")


if __name__ == "__main__":
    main()
