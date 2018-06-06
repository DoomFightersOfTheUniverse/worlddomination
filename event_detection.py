
#gives the power of the Base Consumption Zone, the background power that is
#always used
#ideas: Otsu's method
# - minimum
OFFSET = 15.0
DIFF_THRESHOLD = 50.0

def BCZ(data):
    return min(data) + OFFSET

def ed_diff(data):
    events = []
    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        if abs(diff) > DIFF_THRESHOLD:
            events.append((i,diff))
    return events

if __name__ == '__main__':
    data = None
    events = ed_diff(data)
    for e in events:
        time, diff = e
        print('time=%d, diff=%d' % (e))
