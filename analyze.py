import numpy as np

from common.fft import FFT, Mask
from common.sampling import SamplingProperties
from common.wave_gen import generate_data, property_check, construct_data, Wave, Pulse

if __name__ == '__main__':
    # choose 'matplotlib' or 'plotly' as backend
    # plotly is good when sampling points are not more than 128
    graphic_backend = 'matplotlib'

    if graphic_backend == 'plotly':
        import waves_plotly as lib
    elif graphic_backend == 'matplotlib':
        import waves_mpl as lib

    # choose signal
    signal = Pulse

    # set sampling properties
    smpl_props = SamplingProperties(256, 1, 1, 1)
    property_check(smpl_props.sft, smpl_props.sfx, smpl_props.sfy, signal)
    data = generate_data(smpl_props, signal)

    # plot data in 2 ways
    lib.ani_3d.plot(data, smpl_props.sp)
    lib.ani_2d.plot(data, smpl_props.sp)

    # do fft
    fft = FFT(smpl_props)
    fft_result, abs_fft, shifted_fft, shifted_abs_fft = fft(data.z)

    # plot fft result in 3 directions with slider
    lib.kx_ky_freq_slider.plot(smpl_props, fft, shifted_abs_fft)
    lib.kx_freq_ky_slider.plot(smpl_props, fft, shifted_abs_fft)
    lib.ky_freq_kx_slider.plot(smpl_props, fft, shifted_abs_fft)

    # create filter
    # choose the needed range of f, kx, ky in the format (lower limit, higher limit)
    # todo: improve mask flexibility.
    # currently can only do rectangular filter, which has a high risk creating some glitches in the frequency domain
    mask = Mask(smpl_props, (90, 120), (30, 50), (30, 50))()

    # do filter
    fft_masked = shifted_fft * mask
    abs_fft_masked = np.abs(fft_masked)

    # plot filtered fft result in 3 directions with slider
    lib.kx_ky_freq_slider.plot(smpl_props, fft, abs_fft_masked)
    lib.kx_freq_ky_slider.plot(smpl_props, fft, abs_fft_masked)
    lib.ky_freq_kx_slider.plot(smpl_props, fft, abs_fft_masked)

    # do ifft on the filtered result
    ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
    ifft_data = construct_data(smpl_props, ifft)

    # plot filtered signal in 2 ways
    lib.ani_3d.plot(ifft_data, smpl_props.sp)
    lib.ani_2d.plot(ifft_data, smpl_props.sp)
