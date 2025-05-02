from wrfout.handler.type import VertivalCoordinate

# Configuration file for plotting WRF data

### start and end points of vertical cross section ###
# set start point at left and end point at right.
LAT_START = 33.7
LAT_END = 33.7
LON_START = 130.5
LON_END = 131.1

### vertical axis ###
VERTICAL_COORDINATE = VertivalCoordinate.HEIGHT  # PRESSURE or HEIGHT
# level range
# [hpa] for pressure coordinate
# [m] for height coordinate
Y_LEVELS_TOP = 1500
Y_LEVELS_BOTTOM = 0
INTERPOLATION_INTERVAL = 10

### figure size
FIG_SIZE = (13, 9)

### title
TITLE = "vertical cross section"
TITLE_SIZE = 14

### ticks interval
X_TICKS_INTERVAL = 10


### shade
# Additional variable name: "wv_flux"
shade_plot = True
SHADE_VARNAME = "th"
SHADE_MAX = 310
SHADE_MIN = 290
SHADE_INTERVAL = 1
SHADE_MULTIPLIER = 1
SHADE_ADDITION = 0
# colormap
COLOR_MAP_NAME = "jet"
CBAR_UNIT = "[K]"

### contour
contour_plot = True
CONTOUR_VARNAME = "rh"
CONTOUR_MAX = 100
CONTOUR_MIN = 0
CONTOUR_INTERVAL = 10
CONTOUR_MULTIPLIER = 1
CONTOUR_ADDITION = 0
CONTOUR_COLOR = "brown"
plot_contour_label = True
CONTOUR_LABEL_INTERVAL = 10

### vector
vector_plot = True
U_VEXTOR_VARNAME = "uvmet"
V_VEXTOR_VARNAME = "wa"
VECTOR_X_SPARSITY = 2
VECTOR_Y_SPARSITY = 8
VECTOR_REDUCTION_SCALE = 100
VECTOR_COLOR = "lightslategray"

### vector legend
vector_legend_plot = True
VECTOR_LEDEND_VALUE = 5
VECTOR_LEDEND_SIZE = 8
VECTOR_LEGEND_NAME = f"{VECTOR_LEDEND_VALUE} " + r"[$\mathrm{m\,s^{-1}}$]"

### gif and mp4
GIF_INTERVAL_TIME = 300
GIF_NAME = "vertical_cross_section"
MP4_FPS = 4.0
MP4_NAME = "vertical_cross_section"
