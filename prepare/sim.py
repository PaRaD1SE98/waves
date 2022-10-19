import numpy as np

from common.constructor import construct_data, generate_data
from common.fft import FFT, CubeBlackList, CubeWhiteList
from common.sampling import SamplingProperties
from models.pulses import Pulse
from models.waves import Wave
from config import SIMULATION_TYPE

match SIMULATION_TYPE:
    case 'pulse':
        signal = Pulse
    case 'wave':
        signal = Wave
    case _:
        raise ValueError('Unknown SIMULATION_TYPE: {}'.format(SIMULATION_TYPE))

# set sampling properties
props = SamplingProperties((64, 64, 64), 1, 1, 1)
data = generate_data(props, signal)

# do fft
fft = FFT(data)

# create filter
# choose the needed range of f, kx, ky in the format (lower limit, higher limit)
# todo: improve mask flexibility.
# currently can only do rectangular filter, which has a high risk creating some glitches in the frequency domain
mask = CubeWhiteList(fft, (17, 25), (10, 30), (10, 30))()

# do filter
fft_masked = fft.shifted_fft * mask
abs_fft_masked = np.abs(fft_masked)

# do ifft on the filtered result
ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
ifft_data = construct_data(data.sample_props, ifft)
