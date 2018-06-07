import data_analysis as ld
import random, os

def load_random_file():
    file_name = random.choice(ld.file_names)
    path = os.path.join(ld.data_dir,file_name)
    return [ld.build_LineData(path, line_id) for line_id in [0, 1, 2, 3]]

def load_file(file=None, lines=[0, 1, 2, 3]):
    if lines == 'random':
        lines = [random.choice([1, 2, 3])]

    if file is None:
        file_name = random.choice(ld.file_names)
        file = os.path.join(ld.data_dir, file_name)

    list = [ld.build_LineData(file, x) for x in lines]
    data = list[0] if len(list) == 1 else list
    return data

def load_all_power(line):
    power = []
    for file_name in ld.file_names:
        file = os.path.join(ld.data_dir, file_name)
        data = ld.build_LineData(file, line)
        power += data.apparent.power_pos
