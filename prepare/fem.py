"""
prepare data for plotting
"""
import os
import numpy as np
import scipy

from common.data_reader import lsdyna_read as fread
from common.fft import CubeBlackList, BaseBlackList, FFT, CubeWhiteList
from common.sampling import SamplingProperties
from common.constructor import construct_data, down_sampling
from common.utils import CScanConfig
import config

data_path = os.path.join(config.DATA_BASE_DIR, config.FEM_DATA_FILENAME)
raw_data = fread(data_path)

# Put C_Scan data in this directory
# including wave.dat and cmt-scan.txt

# construct data
c_scan_path = os.path.join(config.DATA_BASE_DIR, 'cmt-scan.txt')
c_scan = CScanConfig(c_scan_path)
c_scan.Nx = raw_data.shape[0]
c_scan.Ny = raw_data.shape[1]
c_scan.data_length = raw_data.shape[2]
# set sampling properties from cmt-scan.txt
sr: int = c_scan.sample_rate     # sampling rate Hz | Sample Rate
spx: int = c_scan.Nx             # sampling size x  | Nx
spy: int = c_scan.Ny             # sampling size y  | Ny
spt: int = c_scan.data_length    # sampling size t  | A/D Data length
dx: float = c_scan.dx / 1000     # m                | dx mm
dy: float = c_scan.dy / 1000     # m                | dy mm

t_max = spt / sr
x_max = spx * dx
y_max = spy * dy


props = SamplingProperties((spt, spx, spy), t_max, x_max, y_max)
data = construct_data(props, raw_data)

# down sampling to make it possible to graph with plotly
# down sampling will result in a less plotting range because.
if config.DOWN_SAMPLING:
    new_samp_size = [
        round(i * config.DOWN_SAMPLING_RATIO) for i in [spt, spx, spy]]
    data = down_sampling(data, *new_samp_size)

# do fft
fft = FFT(data)

# create filter
# choose the needed range of f, kx, ky in the format (lower limit, higher limit)
# todo: improve mask flexibility.
# currently can only do cube filter
white_list = CubeWhiteList(fft, **config.FILTER_WHITELIST)
# black_list = CubeBlackList(fft, **config.FILTER_BLACKLIST)
# mask = np.logical_and(white_list(), black_list())
mask = white_list()
# do filter
fft_masked = fft.shifted_fft * mask
abs_fft_masked = np.abs(fft_masked)

# do ifft on the filtered result
ifft = scipy.fft.ifftn(scipy.fft.ifftshift(fft_masked)).real
ifft_data = construct_data(data.sample_props, ifft)
