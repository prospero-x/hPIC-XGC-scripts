import matplotlib.pyplot as plt
import numpy as np
import sys
import re

filtered_v = []
with open(sys.argv[1], 'r') as f:
    V_pattern = re.compile("^Vel:.*$")
    for line in f.readlines():
        if V_pattern.match(line.strip()):
            v = float(line.strip().split(':')[1])
            filtered_v.append(v)
filtered_v = np.array(filtered_v)

fontsize = 24
_, ax = plt.subplots(figsize=(14,10))
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
ax.hist(filtered_v/1000, bins = 100)

plt.title('Distribution of $\\sqrt{v_x^2 + v_y^2 + v_z^2}$ computed by hpic_1d3v\n'
        + 'Note: $v_{TH}$ = 9.82 km/s from XGC initial condition. OK?', fontsize = fontsize)
plt.xlabel('v (km/s)', fontsize = fontsize)
plt.ylabel('N (#)', fontsize = fontsize)

plt.show()
