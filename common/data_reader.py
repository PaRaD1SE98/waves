import numpy as np


def fread(f_name, nx=365 + 1, ny=32 + 1, l_wave=1000):
    with open(f_name, 'rb') as f:
        a = np.fromfile(f, dtype=np.int16)
        z = np.reshape(a, (nx, ny, l_wave))
    return z
