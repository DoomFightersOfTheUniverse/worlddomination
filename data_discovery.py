#!/usr/bin/env python3
import csv
import os
import random
import numpy as np
script_dir = str(os.path.dirname(os.path.abspath(__file__)))
lines = None

data_dir = os.path.join(script_dir, os.pardir, 'data')
file_names = ['SN70807705-B-control-EM-2017-05-%02d.csv' % (i,) for i in range(1, 32)]

def read_file(file_path, header_lines=3):
    with open(file_path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        lines = list(spamreader)
        headers = lines[:header_lines]
        data = lines[header_lines:]
        return (headers, data)


def print_row(row):
    print('<' + '>, <'.join(row) + '>')


def column(rows, index, function=str):
    return [function(r[index]) for r in rows]

#def median(power):


def aritmeticalMedium(power):
    sum = 0
    for i in power:
        print(i)
        sum += i
    average = sum/len(power)
    return average


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

if __name__ == '__main__':
    file_name = random.choice(file_names)
    headers, lines = read_file(os.path.join(data_dir, file_name))

    for row in headers:
        print_row(row)

    for row in lines[:5]:
        print_row(row)

    dates = column(lines, 0)
    power = column(lines, 2, float)

    time = [i/60.0 for i in range(len(power))]

    days = [None] * len(file_names)

    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap, BoundaryNorm

    power = np.array(power)
    time = np.array(time)

    # threshold = sum(power) / len(power)
    threshold = min(power)+20
    mask = power > threshold

    points = np.array([time, power]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    # norm = plt.Normalize(power.min(), power.max())

    # plot(time, power, mask)

    # cmap = ListedColormap(['r', 'g'])
    # norm = BoundaryNorm([0, threshold, power.max()], cmap.N)
    # lc = LineCollection(segments, cmap=cmap, norm=norm)
    # lc.set_array(power)
    # lc.set_linewidth(2)
    # # line = .add_collection(lc)
    # plt.colorbar(lc)
    #
    plt.axhline(y=threshold, color='r', linestyle=':')

    # greater_than_threshold = [i for i, val in enumerate(ys) if val>threshold]
    # ax.plot(mask, ys[mask],            linestyle='none', color='r', marker='o')

    plt.plot(time,power)
    # plt.plot(time[mask], power[mask], linestyle='none', color='r', marker='o')
    plt.ylabel('%s.power' % file_name)
    plt.show()

    diff_power = [power[i + 1] - power[i] for i in range(len(power) - 1)]
    plt.plot(time[:-1],diff_power)
    plt.ylabel('%s.diff_power' % file_name)
    plt.show()

    print(aritmeticalMedium(power))
