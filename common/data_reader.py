import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
        raw_data = np.array(raw_data, dtype=np.int16)
        # plot first 50 data sets
        # plt.plot(raw_data[-1, 0, :])
        # plt.show()
        print(raw_data.shape)
        return raw_data


def lsdyna_read(f_name):
    """
    Read data from ls-dyna plot save.
    single x csv file
    """
    df = pd.read_csv(f_name, skiprows=1)
    # delete 'time' column
    df = df.drop(df.columns[0], axis=1)
    # delete last column
    df = df.iloc[:, :-1]
    raw_data = np.array(df)
    # add one dimension in axis 1
    raw_data = np.expand_dims(raw_data, axis=1)
    # reshape to (2,1,0)
    raw_data = np.swapaxes(raw_data, 0, 2)

    # plot first 50 data sets
    # plt.plot(raw_data[1500, 0, :600])
    # plt.show()
    return raw_data


def lsdyna_read_pd(f_name, format_col_name=lambda x: x):
    """
    Read data from ls-dyna plot save.
    single x csv file
    """
    df = pd.read_csv(f_name, skiprows=1)
    # delete 'time' column
    df = df.drop(df.columns[0], axis=1)
    # delete last column
    df = df.iloc[:, :-1]
    # format column name
    # apply function to each column name
    df.columns = df.columns.map(format_col_name)
    return df
