import matplotlib.pyplot as plt
import numpy as np
import sys


if len(sys.argv) < 5:
    print('usage: python plot_xgc_mesh.py <mesh.csv> rmin rmax zmin zmax')
    sys.exit(0)

mesh = np.genfromtxt(sys.argv[1], delimiter=',')

rmin = float(sys.argv[2])
rmax = float(sys.argv[3])
zmin = float(sys.argv[4])
zmax = float(sys.argv[5])

nodes_of_interest = []
for i, node in enumerate(mesh):
    r, z = node
    if rmin <= r and r <= rmax and zmin <= z and z <= zmax:
        nodes_of_interest.append(node)
        print(i)

nodes_of_interest = np.array(nodes_of_interest)

plt.figure(figsize=(14,12))
plt.scatter(
    mesh[:,0],
    mesh[:,1],
    color = 'tab:blue',
    marker = '.',
)

plt.ylim([-1.3, -1.1])
plt.xlim([1.3, 1.6])
if len(nodes_of_interest) > 1:
    plt.scatter(
    nodes_of_interest[:,0],
    nodes_of_interest[:,1],
    color = 'red',
    marker = '.',
    s = 150,
    label = 'nodes of Interest'
)
plt.legend()
plt.show()
