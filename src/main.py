from constant import WRFOUT_PATH, contour_plot, shade_plot, vector_plot
from dataset_info import WrfoutInfoOutput
from figure.plot import WrfoutVerticalPlot
from util.path import generate_path

if __name__ == "__main__":
    wrfout_path = generate_path(WRFOUT_PATH)
    info = WrfoutInfoOutput(wrfout_path)
    info.output_dataset_information()
    palette = WrfoutVerticalPlot(wrfout_path)
    palette.make_continuous_figs(
        shade_plot=shade_plot,
        contour_plot=contour_plot,
        vector_plot=vector_plot,
    )
