#TODO signatures of devices
from event_detection import *

def sle_split(part):
    data = part.data
    diffs = ed_diff(data)
    pos_diffs = []
    neg_diffs = []
    for pos, diff in diffs:
        if diff >= 0:
            pos_diffs.append((diff, pos))
        else:
            neg_diffs.append((-diff, pos))

    sort(pos_diffs)
    sort(neg_diffs)


if __name__ == '__main__':
    parts = None#TODO
