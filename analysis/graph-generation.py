import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
from matplotlib.pyplot import cm, rcParams


plt.rc("axes", titlesize=16)
plt.rc("axes", labelsize=16)
plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)
rcParams['axes.titlepad'] = 10


def vectorisation_graphs():
    Applications = ["MiniBude", "Stream", "Cloverleaf", "Tealeaf", "Minisweep"]
    Retired = {
        "128": [1, 1, 1, 1, 1],
        "256": [1, 1, 1, 1, 1],
        "512": [11785149, 3474135, 16290717, 11190734, 9576836],
        "1024": [1, 1, 1, 1, 1],
        "2048": [1, 1, 1, 1, 1],
    }
    Sve = {
        "128": [1, 1, 1, 1, 1],
        "256": [1, 1, 1, 1, 1],
        "512": [6987051, 1950026, 82611, 27148, 190],
        "1024": [1, 1, 1, 1, 1],
        "2048": [1, 1, 1, 1, 1],
    }
    Percent = {
        "128": [i*100/j for i,j in zip(Sve["128"], Retired["128"])],
        "256": [i*100/j for i,j in zip(Sve["256"], Retired["256"])],
        "512": [i*100/j for i,j in zip(Sve["512"], Retired["512"])],
        "1024": [i*100/j for i,j in zip(Sve["1024"], Retired["1024"])],
        "2048": [i*100/j for i,j in zip(Sve["2048"], Retired["2048"])],
    }
    Percent_per_app = {}
    for i in range(len(Applications)):
        Percent_per_app[Applications[i]] = [j[i] for j in Percent.values()]

    print()
    width = 0.14
    ind = np.arange(5)
    fig, ax = plt.subplots()
    #hatches = ['/', '.', 'o', '\\', 'x']
    hatches = ['', '', '', '', '']
    colours = []
    cmap = plt.get_cmap('viridis')
    for i in range(5):
        colours.append(cmap(i*75))
    minibude_bar = plt.bar(ind, Percent_per_app["MiniBude"], width, edgecolor="black", color=colours[0], hatch=hatches[0])
    stream_bar = plt.bar(ind+width, Percent_per_app["Stream"], width, edgecolor="black", color=colours[1], hatch=hatches[1])
    clover_bar = plt.bar(ind+width*2, Percent_per_app["Cloverleaf"], width, edgecolor="black", color=colours[2], hatch=hatches[2])
    tea_bar = plt.bar(ind+width*3, Percent_per_app["Tealeaf"], width, edgecolor="black", color=colours[3], hatch=hatches[3])
    sweep_bar = plt.bar(ind+width*4, Percent_per_app["Minisweep"], width, edgecolor="black", color=colours[4], hatch=hatches[4])

    ax.bar_label(minibude_bar, fmt='{:,.1f}')
    ax.bar_label(stream_bar, fmt='{:,.1f}')
    ax.bar_label(clover_bar, fmt='{:,.1f}')
    ax.bar_label(tea_bar, fmt='{:,.1f}')
    ax.bar_label(sweep_bar, fmt='{:,.1f}') #,fontsize=8)
    plt.xlabel("Vector Length")
    plt.ylabel("% Vectorised Instructions Retired")
    plt.xticks(ind+width*2, [128, 256, 512, 1024, 2048])
    #ax.legend(Applications)

    ax.legend(Applications, loc="upper left", fontsize=10)
    #plt.grid()
    plt.show()



vectorisation_graphs()