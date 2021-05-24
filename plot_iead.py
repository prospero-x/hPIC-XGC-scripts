# Simple plot of IEAD
# python2 iead.py <filename>
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
filename = sys.argv[1]
Te_eV    = float(sys.argv[2])
IEAD   = np.genfromtxt(filename,delimiter=' ')
energy = np.linspace(0.0,24.0*Te_eV,240)
angles = np.linspace(0,90,90)
E,A = np.meshgrid(angles,energy)

fontsize = 24
fig, ax = plt.subplots(figsize=(14,10))
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
cs = ax.contourf(E, A, IEAD)
fig.colorbar(cs)
#plt.clabel(CS, inline = 1, fontsize = 30)

plt.ylim([0, 120])
plt.xlabel('Angle [deg]', fontsize = fontsize)
plt.ylabel('Energy [eV]', fontsize = fontsize)
plt.title('hPIC - Ion Energy Angle Distribution', fontsize = fontsize)
plt.show()
