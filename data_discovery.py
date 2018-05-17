#!/usr/bin/env python3
import csv
import os
import random
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
        return (headers, data) # test


def print_row(row):
    print('<' + '>, <'.join(row) + '>')


def column(rows, index, function=str):
    return [function(r[index]) for r in rows]


def aritmeticalMedium(power):
    for i in power:
        sum += power
    average = power/len(power)


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
    plt.plot(time,power)
    plt.ylabel('%s.power' % file_name)
    plt.show()

    diff_power = [power[i + 1] - power[i] for i in range(len(power) - 1)]
    plt.plot(time[:-1],diff_power)
    plt.ylabel('%s.diff_power' % file_name)
    plt.show()
