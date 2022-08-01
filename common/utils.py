import numpy as np


def to_idx(array, value):
    return np.argmin(np.abs(array - value))
