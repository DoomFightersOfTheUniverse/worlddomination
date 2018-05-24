#!/usr/bin/env python3

import os
import csv
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
        return (headers, data)
