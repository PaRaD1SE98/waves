import matplotlib.pyplot as plt
import numpy as np


def plot(smpl_props, data):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('kx')
    ax.set_ylabel('ky')
    ax.set_zlabel('f')
    x, y, z = np.indices(np.array((smpl_props.sp, smpl_props.sp, smpl_props.sp)) + 1)
    ax.voxels(x - smpl_props.sfx / 2, y - smpl_props.sfy / 2, z / 2, data)
    plt.show()
