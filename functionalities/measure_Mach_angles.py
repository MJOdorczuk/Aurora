import h5py
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import lstsq
import os
import shutil
import sys

path = sys.argv[1]

data_ion = h5py.File(path + '/nd1p00_0000.h5', 'r')
data_ion = data_ion[list(data_ion.keys())[0]]
data_ele = h5py.File(path + '/nd2p00_0000.h5', 'r')
data_ele = data_ele[list(data_ele.keys())[0]]
data_phi = h5py.File(path + '/phisp00_0000.h5', 'r')
data_phi = data_phi[list(data_phi.keys())[0]]

timesteps = list(data_ion.keys())

def trailEdgePoint(slice, vs, x, threshold, upper, edge):
    try:
        if upper:
            ys = np.array([np.where(slice < v)[0][0] for v in vs])
        else:
            slice = slice[::-1]
            ys = slice.shape[0] - np.array([np.where(slice < v)[0][0] for v in vs]) - 1

        M = ys[:, np.newaxis] ** [0, 1]
        c, m = lstsq(M, vs, rcond=None)[0]

        edge.append([x, (threshold - c) / m])
    except:
        pass

def getEdges(data, n_smooth, vs, threshold, x0, x1):
    edge1 = []
    edge2 = []
    midz = data.shape[0] // 2
    z0 = midz - n_smooth // 2
    z1 = midz + n_smooth // 2

    data = data[z0:z1, :, :]
    data = np.average(data, axis=0)
    for x in range(x0, x1, 1):
        slice = data[:,x]
        vs = np.arange(0.9, 0.99, 0.01)
        trailEdgePoint(slice, vs, x, threshold, True, edge1)
        trailEdgePoint(slice, vs, x, threshold, False, edge2)

    edge1 = np.array(edge1)
    edge2 = np.array(edge2)
    return edge1, edge2, data

def getMach(edge):
    M = edge[:,0][:, np.newaxis] ** [0, 1]
    c, m = lstsq(M, edge[:,1], rcond=None)[0]
    return np.abs(1 / np.sin(np.arctan(m))), c, m


def plotCones(data, edge1, edge2, c1, m1, c2, m2, Ma1, Ma2, timestep, type):
    plt.imshow(data)
    plt.scatter(edge1[:,0], edge1[:,1])
    plt.scatter(edge2[:,0], edge2[:,1])
    plt.plot(edge1[:,0], edge1[:,0] * m1 + c1, color='k', label=f'Upper edge Ma={Ma1:.3f}')


    plt.plot(edge2[:,0], edge2[:,0] * m2 + c2, color='brown', label=f'Lower edge Ma={Ma2:.3f}')
    plt.title("Frame " + timestep + " - " + type)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(f'plots/{type}/{timestep}')
    plt.clf()

def plotMach(Ma1, Ma2, type):
    plt.plot(Ma1)
    plt.plot(Ma2)

    print(f"Ma = {Ma1[5:].mean():.3f} ± {Ma1[5:].std():.3f} for {type}")
    print(f"Ma = {Ma2[5:].mean():.3f} ± {Ma2[5:].std():.3f} for {type}")

    plt.xlabel('Timestep')
    plt.ylabel('Mach number')
    plt.title("Mach number over time - " + type)
    plt.ylim(0, 10)
    plt.savefig(f'plots/{type}/mach')
    plt.clf()

Ma_ion1 = []
Ma_ion2 = []
Ma_ele1 = []
Ma_ele2 = []

if os.path.exists('./plots'):
    shutil.rmtree('./plots')
os.makedirs('./plots')
os.makedirs('./plots/ion density')
os.makedirs('./plots/electron density')

for timestep in timesteps:
    ion = data_ion[timestep][()]
    ele = data_ele[timestep][()]
    phi = data_phi[timestep][()]

    edge1, edge2, data = getEdges(ion, 20, np.arange(0.9, 0.97, 0.01), 1, 60, 140)
    Ma1, c1, m1 = getMach(edge1)
    Ma_ion1.append(Ma1)
    Ma2, c2, m2 = getMach(edge2)
    Ma_ion2.append(Ma2)

    plotCones(data, edge1, edge2, c1, m1, c2, m2, Ma1, Ma2, timestep, 'ion density')
    plotMach(Ma1, Ma2, 'ion density')

    edge1, edge2, data = getEdges(ele, 20, np.arange(0.9, 0.99, 0.01), 1, 60, 140)
    Ma1, c1, m1 = getMach(edge1)
    Ma_ele1.append(Ma1)
    Ma2, c2, m2 = getMach(edge2)
    Ma_ele2.append(Ma2)


    plotCones(data, edge1, edge2, c1, m1, c2, m2, Ma1, Ma2, timestep, 'electron density')
    plotMach(Ma1, Ma2, 'electron density')