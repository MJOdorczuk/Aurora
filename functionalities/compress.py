import h5py
import os
import pandas as pd
import sys
import shutil

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

def slice_and_smooth(data, axis, index, n):
    begin = index - n // 2
    indices = list(range(begin, begin + n))
    slices = [slice(data, axis, i) for i in indices]
    return sum(slices) / n

def average_slice(file):
    with h5py.File(file, 'r') as f:
        label = list(f.keys())[0]
        data = f[label]
        data_av = time_average(data, 20)
        data_av = slice_and_smooth(data_av, 0, data_av.shape[0] // 2, 11)
        return data_av, label

def save_slice(data, label, file):
    with h5py.File(file, 'w') as f:
        group = f.create_group(label)
        group.create_dataset(f'0000', data=data)

def save_to_csv(data, file):
    columns = ["Point ID", "Structured Coordinates:0", "Structured Coordinates:1", "Structured Coordinates:2"] + list(data.keys())
    shape = data[list(data.keys())[0]].shape
    rows = []
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                rows.append([i * shape[1] * shape[2] + j * shape[2] + k, k, j, i] + [data[label][i, j, k] for label in data])
    pd.DataFrame(rows, columns=columns).to_csv(file, index=False)

if os.path.exists('./compressed'):
    shutil.rmtree('./compressed')
os.makedirs('./compressed')

ax = sys.argv[1]
Ma = sys.argv[2]
B = sys.argv[3]

data = {}
ion, ion_label = average_slice('nd1p00_0000.h5')
data[ion_label] = ion
save_slice(ion, ion_label, 'compressed/nd1p00_0000.h5')
ele, ele_label = average_slice('nd2p00_0000.h5')
data[ele_label] = ele
save_slice(ele, ele_label, 'compressed/nd2p00_0000.h5')
phi, phi_label = average_slice('phisp00_0000.h5')
data[phi_label] = phi
save_slice(phi, phi_label, 'compressed/phisp00_0000.h5')

save_to_csv(data, f'compressed/data_B{ax}_Ma{Ma}_{B}uT.csv')