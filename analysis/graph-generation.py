import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
from matplotlib.pyplot import cm, rcParams
import seaborn as sns
import pandas as pd
import os


plt.rc("axes", titlesize=20)
plt.rc("axes", labelsize=20)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=18)
rcParams['axes.titlepad'] = 10


def vectorisation_graphs():
    Applications = ["MiniBude", "Stream", "Tealeaf", "Minisweep"]
    Retired = {
        "128": [36413576, 22808568, 11267343, 9576770],
        "256": [19995969, 12958891, 11248657, 9577464],
        "512": [11785149, 6635444, 11191132, 9576836],
        "Hardware (512)": [13465009, 8250224, 12903957, 11289854],
        "1024": [7681752, 3474561, 11162121, 9576520],
        "2048": [5631533, 1893587, 11248635, 9576309],
    }
    Sve = {
        "128": [26328628, 13500025, 80014, 0],
        "256": [13434271, 7800026, 54230, 359],
        "512": [6987051, 3900026, 27148, 190],
        "Hardware (512)": [7226017, 4475173, 45518, 538],
        "1024": [3763441, 1950026, 13602, 105],
        "2048": [2151624, 975026, 4809, 55],
    }
    Percent = {
        "128": [i*100/j for i,j in zip(Sve["128"], Retired["128"])],
        "256": [i*100/j for i,j in zip(Sve["256"], Retired["256"])],
        "512": [i*100/j for i,j in zip(Sve["512"], Retired["512"])],
        "Hardware (512)": [i*100/j for i,j in zip(Sve["Hardware (512)"], Retired["Hardware (512)"])],
        "1024": [i*100/j for i,j in zip(Sve["1024"], Retired["1024"])],
        "2048": [i*100/j for i,j in zip(Sve["2048"], Retired["2048"])],
    }
    Percent_per_app = {}
    for i in range(len(Applications)):
        Percent_per_app[Applications[i]] = [j[i] for j in Percent.values()]

    print()
    width = 0.2
    ind = np.arange(6)
    fig, ax = plt.subplots()
    fig.set_size_inches(28,16)
    hatches = ['', '', '', '', '']
    colours = []
    cmap = plt.get_cmap('tab20c')
    for i in range(4):
        colours.append(cmap(i*4))
    minibude_bar = plt.bar(ind, Percent_per_app["MiniBude"], width, edgecolor="black", color=colours[0], hatch=hatches[0])
    stream_bar = plt.bar(ind+width, Percent_per_app["Stream"], width, edgecolor="black", color=colours[1], hatch=hatches[1])
    tea_bar = plt.bar(ind+width*2, Percent_per_app["Tealeaf"], width, edgecolor="black", color=colours[2], hatch=hatches[2])
    sweep_bar = plt.bar(ind+width*3, Percent_per_app["Minisweep"], width, edgecolor="black", color=colours[3], hatch=hatches[3])

    ax.bar_label(minibude_bar, fmt='{:,.1f}',fontsize=15, rotation=45)
    ax.bar_label(stream_bar, fmt='{:,.1f}',fontsize=15, rotation=45)
    ax.bar_label(tea_bar, fmt='{:,.1f}',fontsize=15, rotation=45)
    ax.bar_label(sweep_bar, fmt='{:,.1f}',fontsize=15, rotation=45)
    plt.xlabel("Vector Length (bits)", fontsize=28)
    plt.ylabel("% Vectorised Instructions Retired", fontsize=28)
    plt.xticks(ind+width*2, [128, 256, 512, "Hardware (512)", 1024, 2048], fontsize=16)

    ax.legend(["miniBUDE", "STREAM", "TeaLeaf", "Minisweep"], loc="upper right", fontsize=18)
    plt.subplots_adjust(left=0.475, bottom=0.305, right=0.9, top=0.88, wspace=0, hspace=0)
    #plt.show()
    plt.savefig("VectorisedGraphFinal.pdf", format="pdf", bbox_inches="tight")



def heatmaps():
    curdir = "C:/Users/Joseph/Documents/simeng-parameter-study/analysis"
    data = "model_results.csv"

    data_path = os.path.join(curdir, data)
    df = pd.read_csv(data_path)
    accs = ["perc_acc","one_perc","two_perc","five_perc","ten_perc","twentyfive_perc"]
    df.loc['Mean'] = df.mean()
    #df2 = df.sort_values(by = 'Mean', axis=1, ascending=False)
    #df2 = df.loc[:, df.loc['Mean'].abs().sort_values(ascending=False).index]
    df2 = df[["ROB", "l1_clock", "FloatingPoint/SVE-Count", "l1_latency", "l2_size", "clw", \
              "GeneralPurpose-Count", "ram_timing", "Fetch-Block-Size", "Load"]]
    #df2 = df2.drop(accs, axis=1)
    #df2 = df2.iloc[:,:10]
    df2.index = ["MiniBude", "Stream", "Tealeaf", "Minisweep", "Mean"]
    df2 = df2.rename(columns={"FloatingPoint/SVE-Count":"FP/SVE-Count", "GeneralPurpose-Count":"GP-Count", \
                              "Vector-Length": "Vector Length", "l1_clock": "L1 Clock", "l1_latency": "L1 latency", \
                                "l2_size": "L2 Size", "clw": "Cache-Line-Width", "ram_timing": "RAM Timing"})
    df2 = df2.rename(index={"MiniBude":"miniBUDE", "Stream":"STREAM", "Tealeaf":"TeaLeaf"})

    plt.figure(figsize=(30,16))
    plt.subplots_adjust(left=0.44, bottom=0.5, right=0.7, top=0.88, wspace=0, hspace=0)
    sns.heatmap(df2, annot=True, fmt=".2f", vmin=0, vmax=50)
    plt.yticks(rotation=0)
    plt.savefig("Heatmap128Final.pdf", format="pdf", bbox_inches="tight")
    #plt.show()

def accuracy():
    curdir = "C:/Users/Joseph/Documents/simeng-parameter-study/analysis"
    data = "model_results.csv"

    data_path = os.path.join(curdir, data)
    df = pd.read_csv(data_path)
    accs = ["one_perc","two_perc","five_perc","ten_perc", "twentyfive_perc"]
    df2 = df.loc[:, df.columns.intersection(accs)]
    #perc_acc_col = df2.pop("perc_acc")
    #df2.insert(4, "perc_acc", perc_acc_col)
    Applications = ["MiniBude", "Stream", "Tealeaf", "Minisweep"]
    df2.index = Applications
    print(df2)

    width = 0.2
    ind = np.arange(5)
    fig, ax = plt.subplots()
    fig.set_size_inches(28,16)
    hatches = ['', '', '', '']
    colours = []
    cmap = plt.get_cmap('tab20c')
    for i in range(4):
        colours.append(cmap(i*4))
    minibude_bar = plt.bar(ind, df2.iloc[0], width, edgecolor="black", color=colours[0], hatch=hatches[0])
    stream_bar = plt.bar(ind+width, df2.iloc[1], width, edgecolor="black", color=colours[1], hatch=hatches[1])
    tea_bar = plt.bar(ind+width*2, df2.iloc[2], width, edgecolor="black", color=colours[2], hatch=hatches[2])
    sweep_bar = plt.bar(ind+width*3, df2.iloc[3], width, edgecolor="black", color=colours[3], hatch=hatches[3])

    ax.bar_label(minibude_bar, fmt='{:,.1f}',fontsize=13, rotation=45)
    ax.bar_label(stream_bar, fmt='{:,.1f}',fontsize=13, rotation=45)
    ax.bar_label(tea_bar, fmt='{:,.1f}',fontsize=13, rotation=45)
    ax.bar_label(sweep_bar, fmt='{:,.1f}',fontsize=13, rotation=45) #,fontsize=8)
    plt.xlabel("Confidence Interval")
    plt.ylabel("% of predictions")
    plt.xticks(ind+width*1.5, ["1%", "2%", "5%", "10%", "25%"])

    ax.legend(["miniBUDE","STREAM","TeaLeaf","Minisweep"], loc="upper left", fontsize=14)

    plt.subplots_adjust(left=0.525, bottom=0.4, right=0.9, top=0.88, wspace=0, hspace=0)
    #plt.show()
    plt.savefig("AccuracyGraphFinal.pdf", format="pdf", bbox_inches="tight")


config_options = ['Vector-Length','Streaming-Vector-Length','Fetch-Block-Size','Loop-Buffer-Size', \
              'Loop-Detection-Threshold','Heap-Size','Stack-Size','GeneralPurpose-Count', \
              'FloatingPoint/SVE-Count','Predicate-Count','Conditional-Count','Commit','FrontEnd', \
              'LSQ-Completion','ROB','Load','Store','Access-Latency','Load-Bandwidth','Store-Bandwidth', \
              'Permitted-Requests-Per-Cycle','Permitted-Loads-Per-Cycle','Permitted-Stores-Per-Cycle', \
              'clw','core_clock','l1_latency','l1_clock','l1_associativity','l1_size','l2_latency', \
              'l2_clock','l2_associativity','l2_size','ram_timing','ram_clock','ram_size']
    
def clean_data(df, cycle_options):
        # Drop rows with -1 in cycle values
        dropped_rows = []
        for index, row in df.iterrows():
            for i in cycle_options:
                if row[i] == -1:
                    dropped_rows.append(index)
        df.drop(dropped_rows, inplace=True)

        # Exclude unchanged values, and update the config list to show this
        unchanged_options = ['Streaming-Vector-Length', 'Heap-Size', 'Stack-Size', 'Access-Latency', \
                            'core_clock', 'ram_size']
        df.drop(columns=unchanged_options, inplace=True)
        for i in unchanged_options:
            if i in config_options:
                config_options.remove(i)
        return df

def vl_graph():
    #ENTER PATH TO CUR DIRECTORY WHERE THIS FILE IS
    curdir = "~/path/to/cur/dir"
    data = "aarch64-results.csv"
    data_path = os.path.join(curdir, data)
    df = pd.read_csv(data_path)

    def clean_data(df, cycle_options):
        # Drop rows with -1 in cycle values
        dropped_rows = []
        for index, row in df.iterrows():
            for i in cycle_options:
                if row[i] == -1:
                    dropped_rows.append(index)
        for index, row in df.iterrows():
            if row["Load-Bandwidth"] < 256:
                dropped_rows.append(index)
        df.drop(dropped_rows, inplace=True)

        # Exclude unchanged values, and update the config list to show this
        unchanged_options = ['Streaming-Vector-Length', 'Heap-Size', 'Stack-Size', 'Access-Latency', \
                            'core_clock', 'ram_size']
        df.drop(columns=unchanged_options, inplace=True)
        for i in unchanged_options:
            if i in config_options:
                config_options.remove(i)
        return df
    
    df = clean_data(df, ["minibude_cycles", "tealeaf_cycles", "minisweep_cycles"])
    df2 = clean_data(df2, ["stream_cycles"])

    avg128 = df["minibude_cycles"][df["Vector-Length"] == 128].mean()
    avg_cycles = []
    vls = [128, 256, 512, 1024, 2048]
    for i in vls:
        avg_cycles.append(avg128 / df["minibude_cycles"][df["Vector-Length"] == i].mean())
        
    
    stream128 = df2["stream_cycles"][df2["Vector-Length"] == 128].mean()
    avg_cycles_stream = []
    for i in vls:
        avg_cycles_stream.append(stream128 / df2["stream_cycles"][df2["Vector-Length"] == i].mean())

    tea128 = df["tealeaf_cycles"][df["Vector-Length"] == 128].mean()
    avg_cycles_tea = []
    for i in vls:
        avg_cycles_tea.append(tea128 / df["tealeaf_cycles"][df["Vector-Length"] == i].mean())

    sweep128 = df["minisweep_cycles"][df["Vector-Length"] == 128].mean()
    avg_cycles_sweep = []
    for i in vls:
        avg_cycles_sweep.append(sweep128 / df["minisweep_cycles"][df["Vector-Length"] == i].mean())

    colours = []
    cmap = plt.get_cmap('tab20c')
    for i in range(4):
        colours.append(cmap(i*4))

    fig, ax = plt.subplots()
    fig.set_size_inches(28,16)
    ax.set_xscale('log', base=2)
    ax.set_xticklabels(vls)

    plot_linewidth = 3
    plt.plot(vls, avg_cycles, '-o', color=colours[0], linewidth=plot_linewidth)
    plt.plot(vls, avg_cycles_stream, '-o', color=colours[2], linewidth=plot_linewidth)
    plt.plot(vls, avg_cycles_tea, '-o', color=colours[1], linewidth=plot_linewidth)
    plt.plot(vls, avg_cycles_sweep, '-o', color=colours[3], linewidth=plot_linewidth)
    plt.xticks(vls)
    ax.legend(["miniBUDE", "STREAM", "TeaLeaf", "Minisweep"], loc="upper left", fontsize=10)
    plt.xlabel("Vector Length")
    plt.ylabel("Mean speedup against VL=128 mean")
    plt.subplots_adjust(left=0.575, bottom=0.45, right=0.9, top=0.88, wspace=0, hspace=0)
    plt.grid()
    #plt.show()
    plt.savefig("VLGraphFinal.pdf", format="pdf", bbox_inches="tight")



def rob_graph():
    #ENTER PATH TO CUR DIRECTORY WHERE THIS FILE IS
    curdir = "~/path/to/cur/dir"
    data = "aarch64-results.csv"
    data_path = os.path.join(curdir, data)
    df = pd.read_csv(data_path)

    df = clean_data(df, ["minibude_cycles", "tealeaf_cycles", "minisweep_cycles"])
    df2 = clean_data(df2, ["stream_cycles"])

    avg_low = df["minibude_cycles"][df["ROB"] <= 10].mean()
    avg_cycles = []
    robs = [i for i in range(8, 512+1, 4)]
    for i in robs:
        avg_cycles.append(avg_low / df["minibude_cycles"][df["ROB"] == i].mean())
        
    
    avg_low = df2["stream_cycles"][df2["ROB"] <= 10].mean()
    avg_cycles_stream = []
    for i in robs:
        avg_cycles_stream.append(avg_low / df2["stream_cycles"][df2["ROB"] == i].mean())

    avg_low = df["tealeaf_cycles"][df["ROB"] <= 10].mean()
    avg_cycles_tea = []
    for i in robs:
        avg_cycles_tea.append(avg_low / df["tealeaf_cycles"][df["ROB"] == i].mean())

    avg_low = df["minisweep_cycles"][df["ROB"] <= 10].mean()
    avg_cycles_sweep = []
    for i in robs:
        avg_cycles_sweep.append(avg_low / df["minisweep_cycles"][df["ROB"] == i].mean())

    colours = []

    cmap = plt.get_cmap('tab20c')
    for i in range(4):
        colours.append(cmap(i*4))

    fig, ax = plt.subplots()
    fig.set_size_inches(28,16)

    xticklabels = [8] + [i for i in range(32, 512+1, 32)]
    ax.set_xticklabels(xticklabels)

    plot_linewidth = 3
    plt.plot(robs, avg_cycles, '-o', color=colours[0], linewidth=plot_linewidth)
    plt.plot(robs, avg_cycles_stream, '-o', color=colours[2], linewidth=plot_linewidth)
    plt.plot(robs, avg_cycles_tea, '-o', color=colours[1], linewidth=plot_linewidth)
    plt.plot(robs, avg_cycles_sweep, '-o', color=colours[3], linewidth=plot_linewidth)
    plt.xticks(xticklabels, rotation=45, ha="right")
    ax.legend(["miniBUDE", "STREAM", "TeaLeaf", "Minisweep"], loc="upper left", fontsize=16)
    plt.xlabel("Reorder Buffer Size", fontsize=24)
    plt.ylabel("Mean speedup against ROB=8 mean", fontsize=24)
    plt.subplots_adjust(left=0.44, bottom=0.295, right=0.9, top=0.88, wspace=0, hspace=0)
    plt.grid()
    #plt.show()
    plt.savefig("ROBGraphFinal.pdf", format="pdf", bbox_inches="tight")

def fp_graph():
    #ENTER PATH TO CUR DIRECTORY WHERE THIS FILE IS
    curdir = "~/path/to/cur/dir"
    data = "aarch64-results.csv"
    data_path = os.path.join(curdir, data)
    df = pd.read_csv(data_path)
    
    df = clean_data(df, ["minibude_cycles", "tealeaf_cycles", "minisweep_cycles"])
    df2 = clean_data(df2, ["stream_cycles"])

    avg_low = df["minibude_cycles"][df["FloatingPoint/SVE-Count"] <= 38].mean()
    avg_cycles = []
    robs = [38, 39] + [i for i in range(40, 512+1, 8)]
    for i in robs:
        avg_cycles.append(avg_low / df["minibude_cycles"][df["FloatingPoint/SVE-Count"] == i].mean())
        
    
    avg_low = df2["stream_cycles"][df2["FloatingPoint/SVE-Count"] <= 38].mean()
    avg_cycles_stream = []
    for i in robs:
        avg_cycles_stream.append(avg_low / df2["stream_cycles"][df2["FloatingPoint/SVE-Count"] == i].mean())

    avg_low = df["tealeaf_cycles"][df["FloatingPoint/SVE-Count"] <= 38].mean()
    avg_cycles_tea = []
    for i in robs:
        avg_cycles_tea.append(avg_low / df["tealeaf_cycles"][df["FloatingPoint/SVE-Count"] == i].mean())

    avg_low = df["minisweep_cycles"][df["FloatingPoint/SVE-Count"] <= 38].mean()
    avg_cycles_sweep = []
    for i in robs:
        avg_cycles_sweep.append(avg_low / df["minisweep_cycles"][df["FloatingPoint/SVE-Count"] == i].mean())

    colours = []
    cmap = plt.get_cmap('tab20c')
    for i in range(4):
        colours.append(cmap(i*4))

    xticklabels = [38] + [i for i in range(64, 512+1, 32)]
    fig, ax = plt.subplots()
    fig.set_size_inches(28,16)

    import matplotlib.ticker as ticker
    ax.set_xticklabels(xticklabels)

    plot_linewidth = 3
    plt.plot(robs, avg_cycles, '-o', color=colours[0], linewidth=plot_linewidth)
    plt.plot(robs, avg_cycles_stream, '-o', color=colours[2], linewidth=plot_linewidth)
    plt.plot(robs, avg_cycles_tea, '-o', color=colours[1], linewidth=plot_linewidth)
    plt.plot(robs, avg_cycles_sweep, '-o', color=colours[3], linewidth=plot_linewidth)
    plt.xticks(xticklabels, rotation=45, ha="right")
    ax.legend(["miniBUDE", "STREAM", "TeaLeaf", "Minisweep"], loc="upper left", fontsize=16)
    plt.xlabel("FloatingPoint/SVE-Count", fontsize=24)
    plt.ylabel("Mean speedup against ROB=8 mean", fontsize=24)
    plt.subplots_adjust(left=0.44, bottom=0.295, right=0.9, top=0.88, wspace=0, hspace=0)
    plt.grid()
    #plt.show()
    plt.savefig("FPGraphFinal.pdf", format="pdf", bbox_inches="tight")


#CHOOSE WHAT GRAPH TO GENERATE HERE

#vectorisation_graphs()
#heatmaps()
#accuracy()
#vl_graph()
#rob_graph()
#fp_graph()