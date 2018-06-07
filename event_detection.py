import data_analysis as ld
import random, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

#gives the power of the Base Consumption Zone, the background power that is
#always used
#ideas: Otsu's method
# - minimum
OFFSET = 15.0
DIFF_THRESHOLD = 50.0

def BCZ(data):
    return min(data) + OFFSET

def ed_diff(data, threshold=DIFF_THRESHOLD):
    events = []
    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        if abs(diff) > threshold:
            events.append((i,diff))
    return events

class DataPart:#Event
    def __init__(self, start_time, data, threshold):
        self.start_time = start_time
        self.data = data
        self.threshold = threshold

def ed_split_where_less_than_threshold(data, threshold):
    parts = []
    start = None
    state = 'find_start'
    for i in range(len(data)):
        val = data[i]
        new_state = state
        if state == 'find_start':
            if val > threshold:
                start = max(i - 1, 0)
                new_state = 'find_end'
        if state == 'find_end':
            if val <= threshold:
                end = min(len(data), i + 1)
                parts.append(DataPart(start, data[start:end], threshold))
                start = None
                new_state = 'find_start'
        state = new_state
    if state == 'find_end':
        parts.append(DataPart(start, data[start:], threshold))
    return parts


def plot(power, threshold, parts=None):
    from itertools import cycle
    cycol = cycle('bgrcmk')

    time = [i/60.0 for i in range(len(power))]

    power = np.array(power)
    time = np.array(time)

    mask = power > threshold

    points = np.array([time, power]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    if threshold is not None:
        plt.axhline(y=threshold, color='r', linestyle=':')

    plt.plot(time,power)

    if parts:
        for part in parts:
            t = [x / 60.0 for x in range(part.start_time,
                part.start_time + len(part.data))]
            plt.plot(t, part.data, c=next(cycol))
    plt.show()

    diff_power = [power[i + 1] - power[i] for i in range(len(power) - 1)]
    plt.plot(time[:-1],diff_power)
    plt.show()

if __name__ == '__main__':
    import data_loader
    line = data_loader.load_file(lines='random')
    power = data_loader.load_all_power(3) #line.apparent.power_pos
    threshold = min(power) + 10

    parts = ed_split_where_less_than_threshold(power, threshold)
    for part in parts:
        print('[%f, %f)' % (part.start_time / 60.0, (part.start_time + len(part.data)) / 60.0))

    plot(power, threshold, parts=parts)

    # events = ed_diff(power)
    # for e in events:
    #     time, diff = e
    #     print('time=%d, diff=%d' % (e))
