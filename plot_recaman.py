#!/usr/bin/python3

import sys, getopt
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.collections import PatchCollection

from math import sqrt; from itertools import count, islice
from enum import Enum


color_fwd = "k"
color_bwd = "k"


def add_dmnd(ax, fwd, abv, curr_val, i):
    
    if fwd:
        plt_x = [curr_val, curr_val + i/2.0, curr_val + i]
        if abv:
            plt_y = [0, i/-2.0, 0]
        else:
            plt_y = [0, i/2.0, 0]

        ax.plot(plt_x, plt_y, color_fwd+'-')

    else:
        plt_x = [curr_val - i, curr_val - i/2.0, curr_val]
        if abv:
            plt_y = [0, i/-2.0, 0]
        else:
            plt_y = [0, i/2.0, 0]

        ax.plot(plt_x, plt_y, color_bwd+'-')

    return not abv

def add_sc(ax, fwd, abv, curr_val, i):
    if fwd:
        if not abv:
            sc = Arc((curr_val + i/2, 0), height=i, width=i, theta1=0, theta2=180, angle=0, color=color_fwd)
        else:
            sc = Arc((curr_val + i/2, 0), height=i, width=i, theta1=180, theta2=360, angle=0, color=color_fwd)
    else:
        if not abv:
            sc = Arc((curr_val - i/2, 0), height=i, width=i, theta1=0, theta2=180, angle=0, color=color_bwd)
        else:
            sc = Arc((curr_val - i/2, 0), height=i, width=i, theta1=180, theta2=360, angle=0, color=color_bwd)

    ax.add_patch(sc)
    return not abv

def add_tri(ax, fwd, abv, curr_val, i):
    if fwd:
        plt_x = [curr_val, curr_val + i, curr_val + i]
        # if abv:
        #     plt_y = [0, i/-2.0, 0]
        # else:
        #     plt_y = [0, i/2.0, 0]
        plt_y = [0, i/-2.0, 0]
        ax.plot(plt_x, plt_y, color_fwd+'-')
        plt_y = [0, i/2.0, 0]
        ax.plot(plt_x, plt_y, color_fwd+'-')

    else:
        plt_x = [curr_val - i, curr_val - i, curr_val]
        # if abv:
        #     plt_y = [0, i/-2.0, 0]
        # else:
        #     plt_y = [0, i/2.0, 0]
        plt_y = [0, i/-2.0, 0]
        ax.plot(plt_x, plt_y, color_bwd+'-')
        plt_y = [0, i/2.0, 0]
        ax.plot(plt_x, plt_y, color_bwd+'-')

    return not abv

SHAPES = {
    "TRI"  : add_tri,
    "DMND" : add_dmnd,
    "CIR"  : add_sc
    }

def main(argv):
    
    dmnd = False
    min_iter = -1
    max_iter = -1
    shape = add_tri

    try:
        opts, args = getopt.getopt(argv,"hn:s:",["num=","shape=", "min=", "fc=", "bc="])
    except getopt.GetoptError:
        print('plot_recaman.py [-n <num> -s <shape> --min <min> --fc <forward_color> --bc <backward_color>]')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('plot_recaman.py [-n <num> -s <shape> --min <min> --fc <forward_color> --bc <backward_color>]')
            sys.exit()
        elif opt in ("-n", "--num"):
            max_iter = int(arg)
        elif opt in ("--min"):
            min_iter = arg
        elif opt in ("-s", "--shape"):
            shape = SHAPES.get(arg.upper(), lambda: sys.exit(2))
        elif opt in ("--fc"):
            color_fwd = arg
        elif opt in ("--bc"):
            color_bwd = arg

    # if max_iter or min_iter weren't set by args set them to defaults 
    if max_iter < 0:
        print("Using default iterations number = 100")
        max_iter=100
    if min_iter < 0:
        min_iter = 0

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plot_mixed(min_iter, max_iter, shape, ax)


# mix recaman with another sequence to make some diamonds.
def plot_mixed(min_iter, max_iter, draw, ax):
    taken = [0]
    forward = []
    backward = []
    curr_val = 0
    prev_val = None
    max_val = 0
    
    abv = False

    for i in  range(1, max_iter): 
        prev_val = curr_val

        # print(i, curr_val)

        if (curr_val - i) < 0:
            if i >= min_iter:
                abv = draw(ax, True, abv, curr_val, i)
            curr_val = curr_val + i
            forward.append(i)


        elif (curr_val-i) in taken:
            if i >= min_iter:
                abv = draw(ax, True, abv, curr_val, i)
            curr_val = curr_val + i
            forward.append(i)

        else:
            if i >= min_iter:
                abv = draw(ax, False, abv, curr_val, i)
            curr_val = curr_val - i
            backward.append(i)

        taken.append(curr_val)

        if curr_val > max_val:
            max_val = curr_val
    
    print(max_val, curr_val)
    # print(forward)
    # print(backward)
    # print(taken)

    plt.axis('off')
    plt.xlim((-5, max(taken)+10))
    plt.ylim((-0.5*max(taken), 0.5*max(taken)))
    # plt.savefig("img/recaman_80_tdk.png", transparent=True)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
