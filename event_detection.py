import data_analysis as ld
import random, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from itertools import cycle

#gives the power of the Base Consumption Zone, the background power that is
#always used
#ideas: Otsu's method
# - minimum
OFFSET = 10.0
DIFF_THRESHOLD = 50.0
REC_MIN_DISTANCE = 50
REC_MIN_TIME = 5
MIN_SLOPE = 30

def BCZ(data):
    return min(data) + OFFSET

class Event:
    def __init__(self, start, data):
        self.start = start
        self.data = data
        self.sub_events = []

    def gen_time(self):
        return range(self.start, self.start + len(self.data))

    def gen_h_time(self):#human readable time: hours
        return [i/60.0 for i in self.gen_time()]

def ed_diff(data, threshold=DIFF_THRESHOLD):
    events = []
    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        if abs(diff) > threshold:
            events.append((i,diff))
    return events


#"climbs" up and gives the start of the not that bad area
def find_no_climb_start_and_end(data):
    start = len(data)
    end = 0

    for i in range(1, len(data)):
        if data[i] - data[i - 1] < MIN_SLOPE:
            start = i
            break

    for i in range(len(data) - 1, 0, -1):
        if data[i] - data[i - 1] > -MIN_SLOPE:
            end = i - 1
            break

    if start < end:
        return (start, end)
    else:
        return (0,0)

def rec_split_by_baseline(event, max_split=5):
    if max_split <= 0:
        return

    data = event.data

    # make sure there are at least some values
    if len(data) > REC_MIN_TIME:
        start, end = find_no_climb_start_and_end(data)
        if start >= end:
            return

        #remove the first and last value
        min_val = min(data[start:end])
        threshold = min_val + OFFSET #guess#TODO make dynamic

        # Now make sure that there are big differences in the data
        if max(data) - threshold > REC_MIN_DISTANCE:
            event.sub_events = ed_split_where_less_than_threshold(data, threshold)

            for e in event.sub_events:
                e.start += event.start
                rec_split_by_baseline(e, max_split=max_split-1) # recurisve magic happens here

def ed_split_by_baseline(event):
    #remove the first and last value
    threshold = min(event.data[1:-1] + 10)#guess#TODO make dynamic
    parts = ed_split_where_less_than_threshold(event.data, threshold)
    for e in parts:
        e.start += event.start
    return parts

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
                parts.append(Event(start, data[start:end]))
                start = None
                new_state = 'find_start'
        state = new_state
    if state == 'find_end':
        parts.append(Event(start, data[start:]))
    return parts

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

PLOT_COLORS = ['rm', 'gb', 'ck']
def rec_plot(event, depth=0):
    cols = PLOT_COLORS[depth % len(PLOT_COLORS)]
    cycol = cycle(cols)

    if depth == 0:
        time = event.gen_h_time()
        power = event.data
        plt.plot(time, power, c='black')

    for e in event.sub_events:
        plt.plot(e.gen_h_time(), e.data, c=next(cycol))
        rec_plot(e, depth=depth+1)

    if depth == 0:
        plt.show()

if __name__ == '__main__':
    import data_loader
    power = data_loader.load_all_power(1) #line.apparent.power_pos
    power = power[10*60:50*60] #look just at the beginning of the data
    power = smooth(power, 4)

    main_event = Event(0, power)

    rec_split_by_baseline(main_event, max_split=2)

    rec_plot(main_event)
