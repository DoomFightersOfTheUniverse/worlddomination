#!/usr/bin/env python3

import os
import csv
import random
from data_interface import *
script_dir = str(os.path.dirname(os.path.abspath(__file__)))

data_dir = os.path.join(script_dir, os.pardir, 'data')
file_names = ['SN70807705-B-control-EM-2017-05-%02d.csv' % (i,) for i in range(1, 32)]

def read_file(file_path, header_lines=3):
    with open(file_path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        lines = list(spamreader)
        headers = lines[:header_lines]
        data = lines[header_lines:]
        return (headers, data)

def column(rows, index, function=str):
    return [function(r[index]) for r in rows]

def build_PowerData(data, index):
    pow_pos = column(data, index, function=float)
    pow_neg = column(data, index+2, function=float)
    eny_pos = column(data, index+1, function=float)
    eny_neg = column(data, index+3, function=float)
    power_energy = PowerData(pow_pos, pow_neg, eny_pos, eny_neg)
    return power_energy

def build_LineData(file_path, phase):
    switcher = {
        0: 2,
        1: 16,
        2: 31,
        3: 46,
    }

    index = switcher.get(phase)
    # chose random file
    headers,data = read_file(file_path)
    # build data for LineData object
    act_pe = build_PowerData(data,index)
    react_pe = build_PowerData(data,index+4)
    apparent_pe = build_PowerData(data,index+8)
    shared_data = SharedData()
    shared_data.time = column(data,1)
    shared_data.supply_frequency = column(data,15)

    line_data = LineData()
    line_data.active = act_pe
    line_data.reactive = react_pe
    line_data.apparent = apparent_pe
    if index==0:
        current_L1 = column(data,28)
        current_L2 = column(data,43)
        current_L3 = column(data,58)
        line_data.current = list([current_L1[i]+current_L2[i]+current_L3[i]
            for i in range(len(current_L1))])
        line_data.voltage = None
        line_data.power_factor = column(data,14)
    else:
        line_data.current = column(data,index+12)
        line_data.voltage = column(data,index+13)
        line_data.power_factor = column(data,index+14)
    line_data.shared_data = shared_data
    return line_data

if __name__ == '__main__':
    file_name = random.choice(file_names)
    total = build_LineData(os.path.join(data_dir,file_name),0)
    print(total.current)
