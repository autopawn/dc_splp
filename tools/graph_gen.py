import os

import numpy as np

import matplotlib.pyplot as plt

measures={
    "fsols": "Number of final solutions",
    "nfacs": "Instalations in the best solution",
    "vals": "Value of best solution found",
    "times": "Required computation time",
}

problems={
    "splp":"SPLP, $p'$=",
    "pm":"$p$-median, $p$=",
}

RES_FOLDER = raw_input("Results folder: ")

for measure in measures:
    values = {}
    # Iterate over the strategies:
    for strat in os.listdir(RES_FOLDER):

        # Read files:
        fname = os.path.join(RES_FOLDER,strat,measure)
        if os.path.isfile(fname):
            fil = open(fname)
            for lin in fil:
                label,val = lin.strip().split(" ")
                v1,v2,v3,v4 = label.split("_")[1:]
                nn = int(v1[1:])
                ii = int(v2[1:])
                pp = int(v3[1:])
                prob = v4
                val = float(val)
                #
                if prob not in values:
                    values[prob] = {}
                if pp not in values[prob]:
                    values[prob][pp] = {}
                if strat not in values[prob][pp]:
                    values[prob][pp][strat] = {}
                if nn not in values[prob][pp][strat]:
                    values[prob][pp][strat][nn] = {}
                values[prob][pp][strat][nn][ii] = val
            fil.close()

    # Plot means of values:
    for prob in values:
        for pp in values[prob]:
            plt.figure(figsize=(4,3))
            maxy = 0
            for strat in values[prob][pp]:
                xs = sorted(list(values[prob][pp][strat].keys()))
                ys = []
                for x in xs:
                    vals = values[prob][pp][strat][x].values()
                    ys.append(np.mean(vals))
                plt.plot(xs,ys,label=strat)
                maxy = np.maximum(maxy,np.max(ys))
            #
            probname = problems[prob] if prob in problems else prob
            plt.title("%s for %s%d"%(measures[measure],probname,pp))
            plt.ylim((0,maxy))
            plt.legend()
            plt.show()
