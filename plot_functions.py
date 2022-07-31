from settings import GRAPHIC_BACKEND, DATA_SOURCE

match GRAPHIC_BACKEND:
    case 'matplotlib':
        import waves_mpl as lib
    case 'plotly':
        import waves_plotly as lib

match DATA_SOURCE:
    case 'real':
        from process_real_data import fft, data, mask, abs_fft_masked
    case 'simulation':
        from process_simulation_data import fft, data, mask, abs_fft_masked

"""plot data in 2 ways"""


def o2d():
    """plot original data in 2d space"""
    lib.ani_2d.plot(data, data.sample_props.spt, 'Visualized Data')


def o3d():
    """plot original data in 3d space"""
    lib.ani_3d.plot(data, data.sample_props.spt, 'Visualized Data')


"""plot fft result in 3 directions with slider"""


def oxyf():
    """plot fft result ky/kx in 3 directions with frequency slider"""
    lib.kx_ky_freq_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(ky/kx)', c_scale_lim=True)


def oxfy():
    """plot fft result freq/kx in 3 directions with ky slider"""
    lib.kx_freq_ky_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(frequency/kx)')


def oyfx():
    """plot fft result freq/ky in 3 directions with frequency kx slider"""
    lib.ky_freq_kx_slider.plot(fft, fft.shifted_abs_fft, 'FFT Result(frequency/ky)')


def of3d():
    """plot fft result in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.fft_3d.plot(fft, fft.shifted_abs_fft)


"""plot fft mask shape in 3d space"""


def m3d():
    """plot fft mask shape in 3d space"""
    if data.sample_props.spt * data.sample_props.spx * data.sample_props.spy <= 128 ** 3:
        lib.mask_3d.plot(fft, mask)


"""plot filtered fft result in 3 directions with slider"""


def fxyf():
    """plot filtered fft result ky/kx in 3 directions with frequency slider"""
    lib.kx_ky_freq_slider.plot(fft, abs_fft_masked, 'FFT Masked(ky/kx)', c_scale_lim=True)


def fxfy():
    """plot filtered fft result freq/kx in 3 directions with ky slider"""
    lib.kx_freq_ky_slider.plot(fft, abs_fft_masked, 'FFT Masked(frequency/kx)')


def fyfx():
    """plot filtered fft result freq/ky in 3 directions with kx slider"""
    lib.ky_freq_kx_slider.plot(fft, abs_fft_masked, 'FFT Masked(frequency/ky)')


"""plot filtered fft result in 3d space"""


def ff3d():
    """plot filtered fft result in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.fft_3d.plot(fft, abs_fft_masked)


"""plot filtered signal in 2 ways"""


def f2d():
    """plot filtered data in 2d space"""
    lib.ani_2d.plot(data, data.sample_props.spt, 'Filtered Data')


def f3d():
    """plot filtered data in 3d space"""
    lib.ani_3d.plot(data, data.sample_props.spt, 'Filtered Data')


o_plots = [o2d, o3d]
of_plots = [oxyf, oxfy, oyfx, of3d]
m_plots = [m3d]
ff_plots = [fxyf, fxfy, fyfx, ff3d]
f_plots = [f2d, f3d]
plots = o_plots + of_plots + m_plots + ff_plots + f_plots
