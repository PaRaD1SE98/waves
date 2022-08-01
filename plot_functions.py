from settings import GRAPHIC_BACKEND, DATA_SOURCE, PLOTLY_OUTPUT

match GRAPHIC_BACKEND:
    case 'matplotlib':
        import waves_mpl as lib
    case 'plotly':
        import waves_plotly as lib

match DATA_SOURCE:
    case 'real':
        from process_real_data import fft, data, mask, abs_fft_masked, ifft_data
    case 'simulation':
        from process_simulation_data import fft, data, mask, abs_fft_masked, ifft_data

"""plot data in 2 ways"""


def o2d():
    """plot original data in 2d space"""
    lib.ani_2d.plot(data, data.sample_props.spt, 'Visualized Data', output=PLOTLY_OUTPUT)


def o3d():
    """plot original data in 3d space"""
    lib.ani_3d.plot(data, data.sample_props.spt, 'Visualized Data', output=PLOTLY_OUTPUT)


"""plot origin fft result in 3 directions with slider"""


def oxyf():
    """plot origin fft result ky/kx in 3 directions with frequency slider"""
    lib.kx_ky_freq_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(ky/kx)', c_scale_lim=True, output=PLOTLY_OUTPUT)


def oxfy():
    """plot origin fft result freq/kx in 3 directions with ky slider"""
    lib.kx_freq_ky_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(frequency/kx)', output=PLOTLY_OUTPUT)


def oyfx():
    """plot origin fft result freq/ky in 3 directions with frequency kx slider"""
    lib.ky_freq_kx_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(frequency/ky)', output=PLOTLY_OUTPUT)


def of3d():
    """plot origin fft result in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.fft_3d.plot(fft, fft.shifted_abs_fft, 'FFT Result 3d', surface_count=10, output=PLOTLY_OUTPUT)


"""plot fft mask shape in 3d space"""


def m3d():
    """plot fft mask shape in 3d space"""
    if data.sample_props.spt * data.sample_props.spx * data.sample_props.spy <= 128 ** 3:
        lib.mask_3d.plot(fft, mask, 'FFT Mask 3d', surface_count=10, output=PLOTLY_OUTPUT)


"""plot filtered fft result in 3 directions with slider"""


def fxyf():
    """plot filtered fft result ky/kx in 3 directions with frequency slider"""
    lib.kx_ky_freq_slider.plot(fft, abs_fft_masked, 'FFT Masked(ky/kx)', c_scale_lim=True, output=PLOTLY_OUTPUT)


def fxfy():
    """plot filtered fft result freq/kx in 3 directions with ky slider"""
    lib.kx_freq_ky_slider.plot(fft, abs_fft_masked, 'FFT Masked(frequency/kx)', output=PLOTLY_OUTPUT)


def fyfx():
    """plot filtered fft result freq/ky in 3 directions with kx slider"""
    lib.ky_freq_kx_slider.plot(fft, abs_fft_masked, 'FFT Masked(frequency/ky)', output=PLOTLY_OUTPUT)


"""plot filtered fft result in 3d space"""


def ff3d():
    """plot filtered fft result in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.fft_3d.plot(fft, abs_fft_masked, 'FFT Filtered 3d', surface_count=10, output=PLOTLY_OUTPUT)


"""plot filtered signal in 2 ways"""


def f2d():
    """plot filtered data in 2d space"""
    lib.ani_2d.plot(ifft_data, ifft_data.sample_props.spt, 'Filtered Data', output=PLOTLY_OUTPUT)


def f3d():
    """plot filtered data in 3d space"""
    lib.ani_3d.plot(ifft_data, ifft_data.sample_props.spt, 'Filtered Data', output=PLOTLY_OUTPUT)


o_plots = [o2d, o3d]
of_plots = [oxyf, oxfy, oyfx, of3d]
m_plots = [m3d]
ff_plots = [fxyf, fxfy, fyfx, ff3d]
f_plots = [f2d, f3d]
plots = o_plots + of_plots + m_plots + ff_plots + f_plots
d2_plots = [o2d, oxyf, oxfy, oyfx, fxyf, fxfy, fyfx, f2d]
d2_of_plots = [o2d, f2d]
d2_of_f_plots = [oxyf, oxfy, oyfx, fxyf, fxfy, fyfx]
d3_plots = [o3d, of3d, m3d, ff3d, f3d]
surface_plots = [o3d, f3d]
volume_plots = [of3d, m3d, ff3d]
