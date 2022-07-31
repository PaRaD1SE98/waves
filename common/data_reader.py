import numpy as np


def fread(f_name, spx, spy, spt):
    """
    Read data from file.

    :param f_name: filename
    :param spx: sampling size in x direction
    :param spy: sampling size in y direction
    :param spt: sampling size in t direction
    :return: numpy.array((spx, spy, spt))
    """
    with open(f_name, 'rb') as f:
        a = np.fromfile(f, dtype=np.int16)
        z = np.reshape(a, (spy, spt, spx))
        z = np.swapaxes(z, 0, 2)
        z = np.swapaxes(z, 1, 2)
    return z
