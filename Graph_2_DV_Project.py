import warnings

warnings.filterwarnings("ignore")
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Patch
import math
from matplotlib.ticker import FuncFormatter
import mpltex

path = os.getcwd()
ds_1 = pd.read_excel(path + '/datasets/fy2020_table3.xlsx', sheet_name='Table 3')
ds_1.columns = ds_1.columns.astype(str)
years = ds_1.columns[1:11].values  # Remove Region
regions = sorted(ds_1['Region'].values[1:])
color_map = {
    'Africa': '#71C2B9',
    'Asia': '#71d8f5',
    'Australia': '#DEC4F2',
    'Canada': '#fa6f5a',
    'Europe': '#9BCD78',
    'South America': '#f7ae34',
}
# ----------------------------- GRAPH 2 - BUBBLE CHART -------------------------------------#
# Transform the dataset in a format that would be easy to build the graph over-years
ds_1_T = pd.read_excel(path + '/datasets/fy2020_table3 _transposed.xlsx', sheet_name='Table 3')


def animate(num, region_data, lines):
    pos = 0
    for i in region_data:
        # immigrant = ds_1_T[ds_1_T['Region'] == i]['Immigrants'].values
        retrieved_data = region_data[i]
        x = retrieved_data.iloc[0:num]['Year'].values
        y = retrieved_data.iloc[0:num]['Immigrants'].values
        lines[pos].set_data(x, y)
        # index = num if num < 10 else 9
        lines[pos].set_linewidth(2)
        pos += 1

     # Add Covid label
    if num > 8:
        plt.annotate('COVID!', xy=(2019, 380000), xytext=(2019, 425000),
                     horizontalalignment="center",
                     arrowprops=dict(arrowstyle='->', color="gray"),
                     fontsize=9,
                     fontweight='bold',
                     color='#4d4a44'
        )
    return lines


def get_x_y():
    dict_df = {}
    for region in regions:
        dict_df[region] = ds_1_T[ds_1_T['Region'] == region][['Year', 'Immigrants']]
    return dict_df


def ax_formatter(x, pos):
    v = math.floor(x / 1000)
    if v > 0:
        return f'{v}K'
    return f'{v}'


def set_line_settings(axes, lines):
    # Get label names
    labels = []
    for line in lines:
        labels.append(line.get_label())

    # Set legend body in top of the graph
    box = axes.get_position()
    axes.set_position([box.x0, box.y0, box.width * 0.95, box.height])
    handles = [
        Patch(facecolor=color, label=label)
        for label, color in zip(labels, color_map.values())
    ]
    axes.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=6, frameon=False,
                handlelength=1.5,
                handleheight=1.5,
                borderaxespad=-1)
    # Set y label
    axes.set_ylabel("Number of Immigrants", labelpad=20)
    # Set y limits and format the y ticks label
    axes.set_ylim(0, ds_1_T['Immigrants'].max())
    axes.yaxis.set_major_formatter(FuncFormatter(ax_formatter))
    # ax_i.yaxis.set_ticks(np.arange(0, ds_1_T['Immigrants'].max(), 10000))
    # Set x limit
    axes.set_xlim(2011, 2020)
    # Set grid only for y
    axes.yaxis.grid(color='#E7E7E7')
    # Hide all frames
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    # Remove ticks
    axes.tick_params(left=False, bottom=False)
    # Add padding to x axis
    axes.tick_params(axis='x', pad=15)
    # Set title
    plt.title('U.S. Immigration Trends Over Years',
              fontdict={
                  'fontsize': 20,
                  'fontweight': 'bold',
              },
              pad=50
              )
    # Set source
    plt.annotate('SOURCE: U.S Departament of Homeland Security', (0, 0), (-60, -40),
                 fontsize=7,
                 fontweight='bold',
                 xycoords='axes fraction',
                 textcoords='offset points',
                 va='top',
                 color='#4d4a44'
                 )
fig, ax = plt.subplots(figsize=(12, 8))

# Build lines
linestyles = mpltex.linestyle_generator(colors=color_map.values(), lines=['-'], hollow_styles=[], markers=[">"])
africa = ax.plot([], [], color_map['Africa'], label="Africa", **next(linestyles))[0]
asia = ax.plot([], [], color_map['Asia'], label="Asia", **next(linestyles))[0]
australia = ax.plot([], [], color_map['Australia'], label="Australia", **next(linestyles))[0]
canada = ax.plot([], [], color_map['Canada'], label="Canada", **next(linestyles))[0]
europe = ax.plot([], [], color_map['Europe'], label="Europe", **next(linestyles))[0]
south_america = ax.plot([], [], color_map['South America'], label="South America", **next(linestyles))[0]

# Change appearance of lines
lines_settings = [africa, asia, australia, canada, europe, south_america]
set_line_settings(ax, lines_settings)

# Get data and animate it
data = get_x_y()
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(data, lines_settings), interval=700, blit=False)
ani.save('line_graph.gif', writer='pillow')

print('Open gif for graph 2')
