import numpy as np

from common.data_reader import fread
from common.fft import Mask, FFT
from common.sampling import SamplingProperties
from common.constructor import construct_data, down_sampling

# construct data
# set sampling properties from data description
sr = 5000000  # sampling rate Hz
spx = 365 + 1  # sampling size x
spy = 32 + 1  # sampling size y
spt = 1000  # sampling size t
dx = 0.415  # m
dy = 0.417  # m
dt = 1 / spt  # s
t_max = spt / sr
x_max = spx * dx
y_max = spy * dy
raw_data = fread('data/wave.dat', spx, spy, spt)
props = SamplingProperties((spt, spx, spy), t_max, x_max, y_max)
data = construct_data(props, raw_data)

# down sampling to graph with plotly
data = down_sampling(data, 64, 64, 32)

# do fft
fft = FFT(data)

# create filter
# choose the needed range of f, kx, ky in the format (lower limit, higher limit)
# todo: improve mask flexibility.
# currently can only do rectangular filter, which has a high risk creating some glitches in the frequency domain
mask = Mask(fft,
            f_range=None,
            kx_range=(0, 0.1),
            ky_range=None)()

# do filter
fft_masked = fft.shifted_fft * mask
abs_fft_masked = np.abs(fft_masked)

# do ifft on the filtered result
ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
ifft_data = construct_data(data.sample_props, ifft)
