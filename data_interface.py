

class LineData:
    def __init__(self):
        self.active = None#PowerData
        self.reactive = None#PowerData
        self.apparent = None#PowerData
        self.current = None#float
        self.voltage = None#float
        self.power_factor = None#float
        self.shared_data = None#SharedData

def check_power(power):
    for p in power:
        if p < 0 or p > 7000:#TODO just guesses
            raise Exception('Unexpected power: %s' % power)
    return power

def check_energy(energy):
    #TODO check code here
    return energy

class PowerData:
    def __init__(self, p_pos, p_neg, e_pos, e_neg):
        self.power_pos = check_power(p_pos)#float
        self.power_neg = check_power(p_neg) #float
        self.energy_pos = check_energy(e_pos)#float
        self.energy_neg = check_energy(e_neg)#float

class SharedData:
    def __init__(self):
        self.time = None
        self.supply_frequency = None


if __name__ == '__main__':
    p = PowerData(0, 1, 0, 0)
