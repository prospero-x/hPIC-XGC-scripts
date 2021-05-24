import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys



if len(sys.argv) < 2:
    print('usage: python plot_xgc_mesh.py <mesh.csv>')

mesh = np.genfromtxt(sys.argv[1], delimiter=',')

r_range = max(mesh[:,0]) - min(mesh[:,0])
z_range = max(mesh[:,1]) - min(mesh[:,1])

fontsize = 20
rwidth = 7
zheight = rwidth / r_range * z_range
fig, ax = plt.subplots(figsize=(rwidth, zheight))
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.scatter(
    mesh[:,0],
    mesh[:,1],
    color = 'tab:blue',
    marker = '.',
)

# Add rectangle to correspond to the zoomed-in nodes-of-interest plot
nodes_of_interest_plot_xlim = [1.3, 1.6]
nodes_of_interest_plot_ylim = [-1.3, -1.1]

rect_bottom_left = (nodes_of_interest_plot_xlim[0], nodes_of_interest_plot_ylim[0])
rect_width = nodes_of_interest_plot_xlim[1] - nodes_of_interest_plot_xlim[0]
rect_height = nodes_of_interest_plot_ylim[1] - nodes_of_interest_plot_ylim[0]
rect = patches.Rectangle(
    rect_bottom_left,
    rect_width,
    rect_height,
    linewidth=5,
    edgecolor='r',
    facecolor='none',
)

ax.add_patch(rect)

plt.ylabel('Z', fontsize = fontsize)
plt.xlabel('R', fontsize = fontsize)
plt.title('DIII-D Mesh', fontsize = fontsize)
plt.show()
