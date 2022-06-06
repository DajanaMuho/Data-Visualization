import warnings

warnings.filterwarnings("ignore")
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.patches import Patch
from textwrap import fill

# PERSONS OBTAINING LAWFUL PERMANENT RESIDENT STATUS BY TYPE AND MAJOR CLASS OF ADMISSION: FISCAL YEARS 2011 TO 2020
path = os.getcwd()
ds = pd.read_excel(path + '/datasets/fy2020_table6_transposed.xlsx', sheet_name='Table 6')
ds.columns = ds.columns.astype(str)
years = ds.columns[2:].values  # Remove Type, Parent column
types = ds['Type']

# ----------------------------- GRAPH 3 - PIE CHART /  Sunburst Charts -------------------------------------#
# Lets take only for 2020 the parent data
parents = ds[(ds['Type'] == 'Immediate relatives of U.S. citizens') |
             (ds['Type'] == 'Family-sponsored preferences') |
             (ds['Type'] == 'Employment-based preferences') |
             (ds['Type'] == 'Other')
             ]
children = ds[(ds['Parent'] == 'Immediate relatives of U.S. citizens') |
              (ds['Parent'] == 'Family-sponsored preferences') |
              (ds['Parent'] == 'Employment-based preferences') |
              (ds['Parent'] == 'Other')
              ]

# Set colors
cmp = plt.get_cmap("tab20c")
a, b, c, d = [plt.cm.RdPu,  plt.cm.PuBuGn, plt.cm.Blues, plt.cm.Purples]
outer_colors = [a(0.7), b(0.7), c(0.7), d(0.7)]
inner_colors = [a(0.6), a(0.5), a(0.4),
                b(0.6), b(0.5), b(0.4), b(0.3),
                c(0.6), c(0.5), c(0.4),
                d(0.6), d(0.5), d(0.4), d(0.3),
                ]
labels_parent = parents['Type'].values
labels = []
for lab in labels_parent:
    labels.append(lab)
    children_lab = ds[ds['Parent'] == lab]['Type']
    for ch in children_lab:
        labels.append(ch)

outer_label = np.array([fill(label, 25) for label in labels_parent])
formatted_label = np.array([fill(label, 30) for label in labels])
# Plot the inner and outerpie
fig, ax = plt.subplots(figsize=(12, 8))
size = 0.4
radius = 1
circle_r = 0.105
# explosion
explode_1 = [0.04] * len(parents)
explode_2 = [0.05] * len(children)


def get_legend(x, y, labels_data, colors, fontsize=9):
    handles = [
        Patch(facecolor=color, label=label)
        for label, color in zip(labels_data, colors)
    ]
    legend = plt.legend(handles=handles, loc='center right', frameon=False, ncol=1,
                        bbox_to_anchor=(x, y),  # horizontal, vertical
                        handlelength=1.5,
                        handleheight=1.5,
                        borderaxespad=-1,
                        fontsize=fontsize,
                        labelcolor='white',
                        )
    return legend


def set_legend():
    legend1 = get_legend(1.05, 0.95, formatted_label[:1], [outer_colors[0]])
    plt.gca().add_artist(legend1)
    legend2 = get_legend(0.95, 0.85, formatted_label[1: 4], inner_colors[0:3])
    plt.gca().add_artist(legend2)

    legend3 = get_legend(1.07, 0.75, formatted_label[4:5], [outer_colors[1]])
    plt.gca().add_artist(legend3)
    legend4 = get_legend(1.1, 0.55, formatted_label[5:9], inner_colors[3:7])
    plt.gca().add_artist(legend4)

    legend5 = get_legend(1.09, 0.35, formatted_label[9:10], [outer_colors[2]])
    plt.gca().add_artist(legend5)
    legend6 = get_legend(1.095, 0.22, formatted_label[10: 13], inner_colors[7:10])
    plt.gca().add_artist(legend6)

    legend7 = get_legend(0.92, 0.1, formatted_label[13: 14], [outer_colors[3]])
    plt.gca().add_artist(legend7)
    legend8 = get_legend(1.06, 0., formatted_label[14:], inner_colors[10:])
    plt.gca().add_artist(legend8)


def animate(i):
    # Selecting inner, outer circles
    plt.text(-.15, -0.05, years[i], fontsize=18, weight='bold')
    x1 = parents[years[i]]
    x2 = children[years[i]]

    plt.cla()
    ax.axis('equal')

    patches1, texts1, pcts1 = plt.pie(x1,
                                      labels=outer_label,
                                      colors=outer_colors,
                                      autopct='%1.1f%%',
                                      radius=radius,
                                      wedgeprops=dict(width=size, edgecolor='white'),  # creates donut pie
                                      pctdistance=0.75,
                                      explode=explode_1,
                                      )
    for k, patch in enumerate(patches1):
        texts1[k].set_color(patch.get_facecolor())
    plt.setp(pcts1, color='white', fontweight='bold', fontsize=12)
    plt.setp(texts1, fontweight=600)

    patches2, texts2, pcts2 = plt.pie(x2,
                                      colors=inner_colors,
                                      autopct='%1.1f%%',
                                      radius=radius - size,
                                      wedgeprops=dict(width=size, edgecolor='white'),
                                      pctdistance=0.75,
                                      explode=explode_2,
                                      rotatelabels=True,
                                      )
    for label_val, pct_text in zip(texts2, pcts2):
        pct_text.set_rotation(label_val.get_rotation())
    plt.setp(pcts2, color='black', fontweight='bold', fontsize=8)

    # Add centre circle
    centre_circle = plt.Circle((0, 0), circle_r, fc='black')
    plt.text(-.15, -0.05, years[i], fontsize=18, weight='bold', color='white')
    plt.gcf().gca().add_artist(centre_circle)

    # Add title
    ax.set_title('Why do people immigrate to USA ?', fontsize=20, pad=15, weight='bold', color='white')
    # Set legend
    set_legend()
    # Set background image
    fig.patch.set_facecolor('black')



ani = animation.FuncAnimation(fig, animate, frames=len(years), interval=1000)
ani.save('pie_graph.gif', writer='pillow')

print('Check graph 3')
