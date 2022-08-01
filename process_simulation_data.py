import numpy as np

from common.constructor import construct_data, generate_data, property_check
from common.fft import Mask, FFT
from common.sampling import SamplingProperties
from models.pulses import Pulse
from models.waves import Wave

# choose signal or construct data
signal = Wave

# set sampling properties
props = SamplingProperties((64, 64, 64), 1, 1, 1)
property_check(props.sft, props.sfx, props.sfy, signal)
data = generate_data(props, signal)

# do fft
fft = FFT(data)

# create filter
# choose the needed range of f, kx, ky in the format (lower limit, higher limit)
# todo: improve mask flexibility.
# currently can only do rectangular filter, which has a high risk creating some glitches in the frequency domain
mask = Mask(fft, (17, 25), (10, 30), (10, 30))()

# do filter
fft_masked = fft.shifted_fft * mask
abs_fft_masked = np.abs(fft_masked)

# do ifft on the filtered result
ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
ifft_data = construct_data(data.sample_props, ifft)
