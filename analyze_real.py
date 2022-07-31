import numpy as np

from common.data_reader import fread
from common.fft import FFT, Mask
from common.sampling import SamplingProperties
from common.wave_gen import construct_data, down_sampling

if __name__ == '__main__':
    # choose 'matplotlib' or 'plotly' as backend
    # plotly is good when sampling points are not more than 128
    graphic_backend = 'plotly'

    if graphic_backend == 'plotly':
        import waves_plotly as lib
    elif graphic_backend == 'matplotlib':
        import waves_mpl as lib

    # construct data
    # set sampling properties
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
    smpl_props = SamplingProperties((spt, spx, spy), t_max, x_max, y_max)
    data = construct_data(smpl_props, raw_data)

    # down sampling to graph with plotly
    data = down_sampling(data, 64, 64, 32)
    smpl_props = data.sample_props

    # plot data in 2 ways
    lib.ani_3d.plot(data, smpl_props.spt, 'Visualized Data')
    lib.ani_2d.plot(data, smpl_props.spt, 'Visualized Data')

    # do fft
    fft = FFT(smpl_props)
    fft_result, abs_fft, shifted_fft, shifted_abs_fft = fft(data.z)

    # plot fft result in 3 directions with slider
    lib.kx_ky_freq_slider.plot(smpl_props, fft, shifted_abs_fft, 'FFT Result(ky/kx)', c_scale_lim=True, aspect_ratio='as_sample')
    lib.kx_freq_ky_slider.plot(smpl_props, fft, shifted_abs_fft, 'FFT Result(frequency/kx)')
    lib.ky_freq_kx_slider.plot(smpl_props, fft, shifted_abs_fft, 'FFT Result(frequency/ky)')

    # plot fft result in 3d space
    if graphic_backend == 'plotly':
        lib.fft_3d.plot(fft, shifted_abs_fft)

    # create filter
    # choose the needed range of f, kx, ky in the format (lower limit, higher limit)
    # todo: improve mask flexibility.
    # currently can only do rectangular filter, which has a high risk creating some glitches in the frequency domain
    mask = Mask(smpl_props,
                f_range=None,
                kx_range=(0, 0.1),
                ky_range=None)()

    # plot mask shape in 3d space
    if smpl_props.sp[0] * smpl_props.sp[1] * smpl_props.sp[2] <= 128 ** 3:
        lib.mask_3d.plot(fft, mask)

    # do filter
    fft_masked = shifted_fft * mask
    abs_fft_masked = np.abs(fft_masked)

    # plot filtered fft result in 3 directions with slider
    lib.kx_ky_freq_slider.plot(smpl_props, fft, abs_fft_masked, 'FFT Masked(ky/kx)', c_scale_lim=True, aspect_ratio='as_sample')
    lib.kx_freq_ky_slider.plot(smpl_props, fft, abs_fft_masked, 'FFT Masked(frequency/kx)')
    lib.ky_freq_kx_slider.plot(smpl_props, fft, abs_fft_masked, 'FFT Masked(frequency/ky)')

    # plot filtered fft result in 3d space
    if graphic_backend == 'plotly':
        lib.fft_3d.plot(fft, abs_fft_masked)

    # do ifft on the filtered result
    ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
    ifft_data = construct_data(smpl_props, ifft)

    # plot filtered signal in 2 ways
    lib.ani_3d.plot(ifft_data, smpl_props.spt, 'Reconstructed Data')
    lib.ani_2d.plot(ifft_data, smpl_props.spt, 'Reconstructed Data')
