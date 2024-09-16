## This script averages the time dimension of the data and saves the middle slice of the data in a new file.
## The new file is saved in the 'compressed' directory.
## The script is used to reduce the size of the data for the purpose of testing the visualization.

import h5py
import os

def time_average(data, skip_steps):
    timesteps = list(data.keys())
    interesting_timesteps = timesteps[skip_steps:]
    data_av = data[timesteps[0]][()] * 0.0
    for t in interesting_timesteps:
        data_av += data[t][()]
    data_av /= len(interesting_timesteps)
    return data_av

def slice(data, axis, index):
    if axis == 0:
        return data[index:index+1, :, :]
    elif axis == 1:
        return data[:, index:index+1, :]
    elif axis == 2:
        return data[:, :, index:index+1]

def average_slice(file):
    with h5py.File(file, 'r') as f:
        label = list(f.keys())[0]
        data = f[label]
        data_av = time_average(data, 0)
        data_av = slice(data_av, 2, 0)
        return data_av, label

def save_slice(data, label, file):
    with h5py.File(file, 'w') as f:
        group = f.create_group(label)
        for i in range(60):
            group.create_dataset(f'{i:0>4}', data=data)

os.makedirs('./compressed')

ion, ion_label = average_slice('nd1p00_0000.h5')
save_slice(ion, ion_label, 'compressed/nd1p00_0000.h5')
ele, ele_label = average_slice('nd2p00_0000.h5')
save_slice(ele, ele_label, 'compressed/nd2p00_0000.h5')
phi, phi_label = average_slice('phisp00_0000.h5')
save_slice(phi, phi_label, 'compressed/phisp00_0000.h5')