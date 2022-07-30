import numpy as np

from waves_mpl import ani_3d, ani_2d, kx_ky_freq_slider, kx_freq_ky_slider, ky_freq_kx_slider
from waves_mpl.fft import FFT, Mask
from waves_mpl.sampling import SamplingProperties
from waves_mpl.wave_gen import generate_data, Pulse, property_check, construct_data, Wave

if __name__ == '__main__':
    signal = Wave
    # set sampling properties
    smpl_props = SamplingProperties(256, 1, 1, 1)
    property_check(smpl_props.sft, smpl_props.sfx, smpl_props.sfy, signal)
    data = generate_data(smpl_props, signal)
    # plot data in 2 ways
    ani_3d.plot(data, smpl_props.sp)
    ani_2d.plot(data, smpl_props.sp)
    # do fft
    fft = FFT(smpl_props)
    fft_result, abs_fft, shifted_fft, shifted_abs_fft = fft(data.z)
    # plot fft result in 3 directions with slider
    kx_ky_freq_slider.plot(smpl_props, fft, shifted_abs_fft)
    kx_freq_ky_slider.plot(smpl_props, fft, shifted_abs_fft)
    ky_freq_kx_slider.plot(smpl_props, fft, shifted_abs_fft)
    # create filter
    # choose the needed range of f, kx, ky in the format (lower limit, higher limit)
    mask = Mask(smpl_props, (90, 110), (30, 50), (30, 50))()
    # do filter
    fft_masked = shifted_fft * mask
    abs_fft_masked = np.abs(fft_masked)
    # plot filtered fft result in 3 directions with slider
    kx_ky_freq_slider.plot(smpl_props, fft, abs_fft_masked)
    kx_freq_ky_slider.plot(smpl_props, fft, abs_fft_masked)
    ky_freq_kx_slider.plot(smpl_props, fft, abs_fft_masked)
    # do ifft on the filtered result
    ifft = np.fft.ifftn(np.fft.ifftshift(fft_masked)).real
    ifft_data = construct_data(smpl_props, ifft)
    # plot filtered signal in 2 ways
    ani_3d.plot(ifft_data, smpl_props.sp)
    ani_2d.plot(ifft_data, smpl_props.sp)
