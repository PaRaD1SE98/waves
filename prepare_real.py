"""
prepare data for plotting
"""
import numpy as np

from common.data_reader import fread
from common.fft import Mask, FFT
from common.sampling import SamplingProperties
from common.constructor import construct_data, down_sampling
from common.utils import CScanConfig
import config

# Put C_Scan data in this directory
# including wave.dat and cmt-scan.txt

# construct data
c_scan = CScanConfig(f'{config.DATA_BASE_DIR}/cmt-scan.txt')
# set sampling properties from cmt-scan.txt
sr: int = c_scan.sample_rate     # sampling rate Hz | Sample Rate
spx: int = c_scan.Nx + 1         # sampling size x  | Nx
spy: int = c_scan.Ny + 1         # sampling size y  | Ny
spt: int = c_scan.data_length    # sampling size t  | A/D Data length
dx: float = c_scan.dx / 1000     # m                | dx mm
dy: float = c_scan.dy / 1000     # m                | dy mm

t_max = spt / sr
x_max = spx * dx
y_max = spy * dy
raw_data = fread(f'{config.DATA_BASE_DIR}/wave.dat', spx, spy, spt)

props = SamplingProperties((spt, spx, spy), t_max, x_max, y_max)
data = construct_data(props, raw_data)

# down sampling to make it possible to graph with plotly
# down sampling will result in a less plotting range because.
if config.GRAPHIC_BACKEND == 'plotly':
    new_samp_size = [
        i // config.DOWN_SAMPLING_RATIO for i in [spt, spx, spy]]
    data = down_sampling(data, *new_samp_size)

# do fft
fft = FFT(data)

# create filter
# choose the needed range of f, kx, ky in the format (lower limit, higher limit)
# todo: improve mask flexibility.
# currently can only do rectangular filter, which has a high risk creating some glitches in the frequency domain
mask = Mask(fft, **config.FFT_MASK)()

# do filter
fft_masked = fft.shifted_fft * mask
abs_fft_masked = np.abs(fft_masked)

# do ifft on the filtered result
ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
ifft_data = construct_data(data.sample_props, ifft)
