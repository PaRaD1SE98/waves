from process_data_real import fft, data, mask, abs_fft_masked, ifft_data

# choose 'matplotlib' or 'plotly' as backend
# plotly is good when sampling points are not more than 128
graphic_backend = 'matplotlib'

if graphic_backend == 'plotly':
    import waves_plotly as lib
elif graphic_backend == 'matplotlib':
    import waves_mpl as lib

if __name__ == '__main__':

    # plot data in 2 ways
    lib.ani_3d.plot(data, data.sample_props.spt, 'Visualized Data')
    lib.ani_2d.plot(data, data.sample_props.spt, 'Visualized Data')

    # plot fft result in 3 directions with slider
    lib.kx_ky_freq_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(ky/kx)', c_scale_lim=True)
    lib.kx_freq_ky_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(frequency/kx)')
    lib.ky_freq_kx_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(frequency/ky)')

    # plot fft result in 3d space
    if graphic_backend == 'plotly':
        lib.fft_3d.plot(fft, fft.shifted_abs_fft)

    # plot mask shape in 3d space
    if data.sample_props.spt * data.sample_props.spx * data.sample_props.spy <= 128 ** 3:
        lib.mask_3d.plot(fft, mask)

    # plot filtered fft result in 3 directions with slider
    lib.kx_ky_freq_slider.plot(fft, abs_fft_masked, 'FFT Masked(ky/kx)', c_scale_lim=True)
    lib.kx_freq_ky_slider.plot(fft, abs_fft_masked, 'FFT Masked(frequency/kx)')
    lib.ky_freq_kx_slider.plot(fft, abs_fft_masked, 'FFT Masked(frequency/ky)')

    # plot filtered fft result in 3d space
    if graphic_backend == 'plotly':
        lib.fft_3d.plot(fft, abs_fft_masked)

    # plot filtered signal in 2 ways
    lib.ani_3d.plot(ifft_data, data.sample_props.spt, 'Reconstructed Data')
    lib.ani_2d.plot(ifft_data, data.sample_props.spt, 'Reconstructed Data')
