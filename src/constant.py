# wrfout file path
WRFOUT_PATH = "/data/wrfout/netcdf/wrfout_nestingtest_d02_2023-08-21_00:00:00"
# time step
WRFOUT_INTERVAL = 10

# start and end points of vertical cross section
LAT_START = 32.75
LAT_END = 33.5
LON_START = 130
LON_END = 130.75

# y-axis
is_p_coord = False  # pressure or height coordinate
# range: [hpa] for pressure coordinate, [m] for height coordinate
Y_MAX = 3000
Y_MIN = 0
INTERPOLATION_INTERVAL = 50

# title
TITLE = "vertical cross section"
TITLE_SIZE = 10

# ticks and labels
DECIMAL_PLACES = 2
X_TICKS_INTERVAL = 10
LABEL_FONTSIZE = 12
TICKS_FONTSIZE = 7

# for shade
shade_plot = True
SHADE_VARNAME = "QVAPOR"
SHADE_MIN = 10
SHADE_MAX = 20
SHADE_INTERVAL = 0.5
SHADE_MULTIPLIER = 1000
SHADE_ADDITION = 0
TERRAIN_COLOR = "sienna"
# color bar
COLOR_MAP_NAME = "Blues"
CBAR_EXTENTION = "both"
paint_all = True
WHITE_PART_NUM_FROM_MIDDLE = 2
CBAR_TICKS_INTERVAL = 20
CBAR_TICKS_BASE = 1
CBAR_UNIT = r"[$\mathrm{g\,kg^{-1}}$]"
CBAR_LABEL_SIZE = 10
CBAR_LABEL_LOCATION = 3
cbar_auto_ticks = True


# for contour
contour_plot = False
CONTOUR_VARNAME = "wa"
CONTOUR_MIN = 1
CONTOUR_MAX = 5
CONTOUR_INTERVAL = 1
CONTOUR_MULTIPLIER = 1
CONTOUR_ADDITION = 0
CONTOUR_WIDTH = 0.5
CONTOUR_COLOR = "red"
CONTOUR_LABEL_SIZE = 5
plot_contour_label = False
CONTOUR_LABEL_INTERVAL = 1


# for vector
vector_plot = True
U_VEXTOR_VARNAME = "uvmet"
V_VEXTOR_VARNAME = "wa"
VECTOR_X_SPARSITY = 5
VECTOR_Y_SPARSITY = 100
VECTOR_REDUCTION_SCALE = 50
VECTOR_COLOR = "lightslategray"  # "lightslategray"
VECTOR_X_MULTIPLIER = 1
VECTOR_Y_MULTIPLIER = 10
# vector arrow shape
VECTOR_WIDTH = 0.004
VECTOR_LINEWIDTH = 1.5
VECTOR_HEADWIDTH = 4.0
VECTOR_HEADLENGTH = 5
VECTOR_HEADAXIS_LENGTH = 4
# vector legend
vector_legend_plot = True
VECTOR_LEDEND_VALUE = 5
VECTOR_LEDEND_SIZE = 8
VECTOR_LEGEND_NAME = f"{VECTOR_LEDEND_VALUE} " + r"[$\mathrm{m\,s^{-1}}$]"


# for var info
VAR_INFO_XLOCATION = -0.05
VAR_INFO_YLOCATION = -0.125


# for GIF and MP4
GIF_INTERVAL_TIME = 150
GIF_NAME = TITLE
MP4_FPS = 5.0
MP4_NAME = TITLE
