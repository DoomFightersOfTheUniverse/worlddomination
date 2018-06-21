import os
import scipy.io as sio
import matplotlib.pyplot as plt
script_dir = str(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(script_dir, os.pardir, 'Geraete_Plots')


def import_device_matlabdata():
    return [
        (sio.loadmat(os.path.join(data_dir,filename)),filename)
        for filename in os.listdir(data_dir)
        if str(filename).endswith(".mat")
    ]


def plot_device_data(): pass

if __name__ == '__main__':

    mats = import_device_matlabdata()
    for mat in mats:
        data,name = mat
        plt.plot(data['yAP'])
        plt.title(name)
        plt.show()
