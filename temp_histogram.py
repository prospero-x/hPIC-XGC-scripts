import matplotlib.pyplot as plt
import numpy as np
import sys

temps = np.genfromtxt(sys.argv[1])

plt.hist(temps, log = True)
plt.show()
