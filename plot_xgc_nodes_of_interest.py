import matplotlib.pyplot as plt
import numpy as np
import sys


if len(sys.argv) < 3:
    print('usage: python plot_xgc_mesh.py <mesh.csv> <nodes_of_interest.csv>')
    sys.exit(0)

mesh = np.genfromtxt(sys.argv[1], delimiter=',')
nodes_of_interest = np.genfromtxt(sys.argv[2], dtype = np.int_)
coords_of_interest = [(mesh[node][0], mesh[node][1], node) for node in nodes_of_interest]
coords_of_interest.sort(key = lambda coord: coord[0])

fontsize = 20
fig, ax = plt.subplots(figsize=(12,8))
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)

plt.scatter(
    mesh[:,0],
    mesh[:,1],
    color = 'tab:blue',
    marker = '.',
)

plt.ylim([-1.3, -1.1])
plt.xlim([1.3, 1.6])
plt.ylabel('Z', fontsize = fontsize)
plt.xlabel('R', fontsize = fontsize)
plt.title('XGC Nodes of Interest. Each node configures one hPIC simulation', fontsize = fontsize)
for r, z, node in coords_of_interest:
    plt.scatter(r, z, marker = '.', s = 300, label = f'Node {node}')
plt.legend(prop=dict(size=fontsize))
plt.show()
