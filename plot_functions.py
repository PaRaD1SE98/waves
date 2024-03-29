from config import GRAPHIC_BACKEND, DATA_SOURCE, PLOTLY_OUTPUT, DOWN_SAMPLING

# pre-check
if GRAPHIC_BACKEND == 'plotly' and not DOWN_SAMPLING:
    print('Warning: Plotly backend might not support large datasets. '
          'Set config.DOWN_SAMPLING to True to down sample data.')
    ans = input('Keep going? (Y/n)')
    if ans.capitalize() != 'Y':
        exit()

match GRAPHIC_BACKEND:
    case 'matplotlib':
        import lib.mpl as lib
    case 'plotly':
        import lib.plotly as lib

match DATA_SOURCE:
    case 'real':
        from prepare.real import fft, data, mask, abs_fft_masked, ifft_data
    case 'simulation':
        from prepare.sim import fft, data, mask, abs_fft_masked, ifft_data

"""plot data with 2 backends"""


def od2d():
    """plot original data in 2d space"""
    lib.ani_2d.plot(data, data.sample_props.spt,
                    'Visualized_Data_2d', output=PLOTLY_OUTPUT, origin=True)


def od3d():
    """plot original data in 3d space"""
    lib.ani_3d.plot(data, data.sample_props.spt,
                    'Visualized_Data_3d', output=PLOTLY_OUTPUT, origin=True)


"""plot origin fft result in 3 directions with slider"""


def ofxyf():
    """plot origin fft result ky/kx in 3 directions with frequency slider"""
    lib.kx_ky_freq_slider.plot(
        fft, fft.shifted_abs_fft, 'FFT_Result(ky_kx)', c_scale_lim=True, output=PLOTLY_OUTPUT)


def ofxfy():
    """plot origin fft result freq/kx in 3 directions with ky slider"""
    lib.kx_freq_ky_slider.plot(
        fft, fft.shifted_abs_fft, 'FFT_Result(freq_kx)', output=PLOTLY_OUTPUT)


def ofyfx():
    """plot origin fft result freq/ky in 3 directions with frequency kx slider"""
    lib.ky_freq_kx_slider.plot(
        fft, fft.shifted_abs_fft, 'FFT_Result(freq_ky)', output=PLOTLY_OUTPUT)


def of3d():
    """plot origin fft result in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.fft_3d.plot(fft, fft.shifted_abs_fft, 'FFT_Result_3d',
                        surface_count=10, output=PLOTLY_OUTPUT)
    else:
        print('of3d: plotly only, skipping...')


"""plot fft mask shape in 3d space"""


def m3d():
    """plot fft mask shape in 3d space"""
    if data.sample_props.spt * data.sample_props.spx * data.sample_props.spy <= 128 ** 3:
        lib.mask_3d.plot(fft, mask, 'FFT_Mask_3d',
                         surface_count=10, output=PLOTLY_OUTPUT)
    else:
        print('m3d: Dataset too large to plot with matplotlib voxels plot, skipping...')


def mf3d():
    """plot fft mask shape with fft data in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.mask_fft_3d.plot(fft, mask, 'Mask_with_FFT_3d',
                             surface_count=10, output=PLOTLY_OUTPUT)
    else:
        print('mf3d: plotly only, skipping...')


"""plot filtered fft result in 3 directions with slider"""


def ffxyf():
    """plot filtered fft result ky/kx in 3 directions with frequency slider"""
    lib.kx_ky_freq_slider.plot(
        fft, abs_fft_masked, 'FFT_Masked(ky_kx)', c_scale_lim=True, output=PLOTLY_OUTPUT)


def ffxfy():
    """plot filtered fft result freq/kx in 3 directions with ky slider"""
    lib.kx_freq_ky_slider.plot(
        fft, abs_fft_masked, 'FFT_Masked(freq_kx)', output=PLOTLY_OUTPUT)


def ffyfx():
    """plot filtered fft result freq/ky in 3 directions with kx slider"""
    lib.ky_freq_kx_slider.plot(
        fft, abs_fft_masked, 'FFT_Masked(freq_ky)', output=PLOTLY_OUTPUT)


"""plot filtered fft result in 3d space"""


def ff3d():
    """plot filtered fft result in 3d space"""
    if GRAPHIC_BACKEND == 'plotly':
        lib.fft_3d.plot(fft, abs_fft_masked, 'FFT_Filtered_3d',
                        surface_count=10, output=PLOTLY_OUTPUT)
    else:
        print('ff3d: plotly only, skipping...')


"""plot filtered signal in 2 ways"""


def fd2d():
    """plot filtered data in 2d space"""
    lib.ani_2d.plot(ifft_data, ifft_data.sample_props.spt,
                    'Filtered_Data_2d', output=PLOTLY_OUTPUT)


def fd3d():
    """plot filtered data in 3d space"""
    lib.ani_3d.plot(ifft_data, ifft_data.sample_props.spt,
                    'Filtered_Data_3d', output=PLOTLY_OUTPUT)


o = [od2d, od3d]
of = [ofxyf, ofxfy, ofyfx, of3d]
m = [m3d]
ff = [ffxyf, ffxfy, ffyfx, ff3d]
f = [fd2d, fd3d]
all = o + of + m + ff + f
d2 = [od2d, ofxyf, ofxfy, ofyfx, ffxyf, ffxfy, ffyfx, fd2d]
d2_of = [od2d, fd2d]
d2_of_f = [ofxyf, ofxfy, ofyfx, ffxyf, ffxfy, ffyfx]
d3 = [od3d, of3d, m3d, mf3d, ff3d, fd3d]
surface = [od3d, fd3d]
volume = [of3d, m3d, ff3d]


def original_data_plots():
    for plot in o:
        plot()


def original_fft_plots():
    for plot in of:
        plot()


def mask_plots():
    for plot in m:
        plot()


def filtered_fft_plots():
    for plot in ff:
        plot()


def filtered_data_plots():
    for plot in f:
        plot()


def all_plots():
    for plot in all:
        plot()


def d2_plots():
    for plot in d2:
        plot()


def d2_original_and_filtered_plots():
    for plot in d2_of:
        plot()


def d2_original_and_filtered_fft_plots():
    for plot in d2_of_f:
        plot()


def d3_plots():
    for plot in d3:
        plot()


def surface_plot():
    for plot in surface:
        plot()


def volume_plot():
    for plot in volume:
        plot()
