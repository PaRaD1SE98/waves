import matplotlib.pyplot as plt
import numpy as np


def plot(fft, data):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('kx')
    ax.set_ylabel('ky')
    ax.set_zlabel('f')
    x, y, z = np.indices(np.array((fft.smpl_props.sp[1], fft.smpl_props.sp[2], fft.smpl_props.sp[0])) + 1)
    ax.voxels(x - fft.smpl_props.sfx / 2, y - fft.smpl_props.sfy / 2, z / 2, data)
    plt.show()
