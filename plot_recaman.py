#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.collections import PatchCollection

from math import sqrt; from itertools import count, islice


color_fwd = "k"
color_bwd = "k"

def get_max(argv):
    try:
        max_iter = int(argv[1])
    except Exception as e:
        print(e)
        exit(1)
    return max_iter

def get_dmnd(argv):
    dmnd = False

    try:
        if not type(argv[2]) == str:
            print("non-string argument provided")
            exit(1)
        else:
            if argv[2] == "-d":
                dmnd = True
    except Exception as e:
        print(e)
        exit(1)

    return dmnd
        

def main(argv):
    
    dmnd = False
    if len(argv) < 2:
        print("Using default iterations number = 100")
        max_iter=100
    elif len(argv) == 2:
        max_iter = get_max(argv)
    else:
        max_iter = get_max(argv)
        dmnd = get_dmnd(argv)


    plot_mixed(max_iter, dmnd)


# mix recaman with another sequence to make some diamonds.
def plot_mixed(max_iter, dmnd):
    taken = [0]
    forward = []
    backward = []
    curr_val = 0
    prev_val = None

    fig = plt.figure()
    ax = fig.add_subplot(111)

    abv = False

    for i in  range(1,max_iter): 
        prev_val = curr_val

        # print(i, curr_val)

        if (curr_val - i) < 0:
            if dmnd:
                abv = add_dmnd(ax, True, abv, curr_val, i)
            else:
                abv = add_sc(ax, True, abv, curr_val, i)
            curr_val = curr_val + i
            forward.append(i)


        elif (curr_val-i) in taken:
            if dmnd:
                abv = add_dmnd(ax, True, abv, curr_val, i)
            else: 
                abv = add_sc(ax, True, abv, curr_val, i)
            curr_val = curr_val + i
            forward.append(i)

        else:
            if dmnd:
                abv = add_dmnd(ax, False, abv, curr_val, i)
            else: 
                abv = add_sc(ax, False, abv, curr_val, i)
            curr_val = curr_val - i
            backward.append(i)

        taken.append(curr_val)
    

    # print(forward)
    # print(backward)

    plt.axis('off')
    plt.xlim((-5, max(taken)+10))
    plt.ylim((-0.5*max(taken), 0.5*max(taken)))
    plt.show()

    # not_taken = []
    # for i in range(0,max_iter):
    #     if i not in taken:
    #         not_taken.append(i)

    # plt.plot([x for x in range(len(not_taken))],not_taken, 'r*')
    # plt.show()



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


if __name__ == "__main__":
    main(sys.argv)
