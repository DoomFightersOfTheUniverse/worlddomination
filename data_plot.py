#!/usr/bin/env python3
import csv
import os
import random
import numpy as np

def average_days(days):
    length = max(map(len, days))
    avg_day = [0] * length
    for i in range(length):
        count = 0
        sum = 0
        for d in len(days):
            try:
                sum += d[i]
                count += 1
            except:
                pass
        avg_day[i] = sum if count <= 1 else sum / count

def plot(power, threshold):
    time = [i/60.0 for i in range(len(power))]

    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap, BoundaryNorm

    power = np.array(power)
    time = np.array(time)

    mask = power > threshold

    points = np.array([time, power]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    if threshold is not None:
        plt.axhline(y=threshold, color='r', linestyle=':')

    plt.plot(time,power)
    plt.show()

    diff_power = [power[i + 1] - power[i] for i in range(len(power) - 1)]
    plt.plot(time[:-1],diff_power)
    plt.show()

if __name__ == '__main__':
    import data_loader
    line = data_loader.load_file(lines='random')
    power = line.apparent.power_pos

    plot(power, min(power) + 10)
