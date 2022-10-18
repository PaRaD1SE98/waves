import matplotlib.pyplot as plt
import numpy as np


def plot(fft, data, title=None, **kwargs):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_title(title)
    ax.set_xlabel('kx')
    ax.set_ylabel('ky')
    ax.set_zlabel('f')
    x, y, z = np.indices(np.array(
        (fft.smpl_props.spx, fft.smpl_props.spy, fft.smpl_props.spt)) + 1)
    dfx = fft.smpl_props.sfx / fft.smpl_props.spx
    dfy = fft.smpl_props.sfy / fft.smpl_props.spy
    dft = fft.smpl_props.sft / fft.smpl_props.spt
    ax.voxels(((x-fft.smpl_props.spx/2)*dfx),
              ((y-fft.smpl_props.spy/2)*dfy),
              ((z[:fft.smpl_props.spt//2])*dft//2), data)
    plt.show()
