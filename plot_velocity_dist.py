import matplotlib.pyplot as plt
import numpy as np
import sys
import re


def plot_vpara_dist():
    Npara_pattern = re.compile("^Npara:.*$")
    Vpara_pattern = re.compile("^Vpara.*$")
    Npara = []
    Vpara = []
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            if Npara_pattern.match(line.strip()):
                N = float(line.strip().split(':')[1])
                Npara.append(N)

            elif Vpara_pattern.match(line.strip()):
                v = float(line.strip().split(":")[1])
                Vpara.append(v)

    Vpara = np.array(Vpara) / 1000
    print(f"sum: {sum(Npara)}")
    plot(Vpara, Npara, label = '$V_{||}$')


def plot_vperp_dist():
    Nperp_pattern = re.compile("^Nperp:.*$")
    Vperp_pattern = re.compile("^Vperp.*$")
    Nperp = []
    Vperp = []
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            if Nperp_pattern.match(line.strip()):
                N = float(line.strip().split(':')[1])
                Nperp.append(N)

            elif Vperp_pattern.match(line.strip()):
                v = float(line.strip().split(":")[1])
                Vperp.append(v)

    Vperp = np.array(Vperp)/1000
    print(f"sum: {sum(Nperp)}")
    plot(Vperp, Nperp, label = '$V_{\\perp}$')


def plot_vpara_CDF():
    CDF_pattern = re.compile("^CDF_vpar:.*$")
    Vpara_pattern = re.compile("^Vpara.*$")
    CDF = []
    Vpara = []
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            if CDF_pattern.match(line.strip()):
                C = float(line.strip().split(':')[1])
                CDF.append(C)

            elif Vpara_pattern.match(line.strip()):
                v = float(line.strip().split(":")[1])
                Vpara.append(v)

    Vpara = np.array(Vpara)/1000
    print(f"i_f_sum: {sum(CDF):2.4e}")
    plot(Vpara, CDF, label = '$V_{||}$')


def plot_vperp_CDF():
    CDF_pattern = re.compile("^CDF_vper:.*$")
    Vperp_pattern = re.compile("^Vperp.*$")
    CDF = []
    Vperp = []
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            if CDF_pattern.match(line.strip()):
                C = float(line.strip().split(':')[1])
                CDF.append(C)

            elif Vperp_pattern.match(line.strip()):
                v = float(line.strip().split(":")[1])
                Vperp.append(v)

    Vperp = np.array(Vperp)/1000
    print(f"i_f_sum: {sum(CDF):2.4e}")
    plot(Vperp, CDF, label = '$V_{\\perp}$')


def plot(x, y, label):
    fontsize = 24
    _, ax = plt.subplots(figsize=(14,10))
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
    #ax.semilogy(x, y, '^', label = label)
    ax.plot(x, y, '^', label = label)

    plt.title('Marginal Distribution of velocities Coming from XGC', fontsize = fontsize)
    plt.xlabel('v (km/s)', fontsize = fontsize)
    plt.ylabel('N (m$^{-3}$)', fontsize = fontsize)
    plt.legend(prop= dict(size=fontsize))

    plt.show()


if __name__ == '__main__':
    if sys.argv[2] == 'para':
        plot_vpara_dist()
    elif sys.argv[2] == 'perp':
        plot_vperp_dist()
    elif sys.argv[2] == 'CDF_para':
        plot_vpara_CDF()
    elif sys.argv[2] == 'CDF_perp':
        plot_vperp_CDF()

