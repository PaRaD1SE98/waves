import numpy as np


def fread(f_name, spx, spy, spt):
    """
    Read data from file.

    Reads binary data as signed 16-bit integers in big-endian order

    :param f_name: filename
    :param spx: sampling size in x direction
    :param spy: sampling size in y direction
    :param spt: sampling size in t direction
    :return: numpy.array((spx, spy, spt))
    """
    with open(f_name, 'rb') as f:
        # big-endian: '>', signed: 'i', 16bit: '2'
        raw_data = np.fromfile(f, dtype='>i2').reshape((spx, spy, spt))
        # convert to regular array with best compatibility
        raw_data = np.array(raw_data, dtype=np.float32)
        return raw_data
