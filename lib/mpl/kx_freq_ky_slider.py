import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

from common.utils import to_idx


def plot(fft, shifted_fft, title=None, c_scale_lim=False, aspect_ratio=None, **kwargs):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(title)
    ax.set_xlabel('Kx')
    ax.set_ylabel('Freq')
    if aspect_ratio is not None:
        if aspect_ratio == 'as_sample':
            ax.set_aspect(fft.smpl_props.spt / fft.smpl_props.spx)
        elif aspect_ratio == 'as_value':
            ax.set_aspect(fft.smpl_props.sft / fft.smpl_props.sfx)
        elif type(aspect_ratio) == float:
            ax.set_aspect(aspect_ratio)
    kx, freq = np.meshgrid(fft.shifted_KX, fft.FREQ, indexing='ij')
    image_fft_ky = ax.pcolormesh(
        kx, freq, shifted_fft[:, to_idx(fft.shifted_KY, 0), :], cmap='viridis',
        vmin=shifted_fft[p_min[0], p_min[1], p_min[2]] if c_scale_lim else None,
        vmax=shifted_fft[p_max[0], p_max[1], p_max[2]] if c_scale_lim else None
    )
    plt.ylim(0, fft.smpl_props.sft / 2)  # set valid frequency window
    fig.colorbar(image_fft_ky, label='Amplitude')
    fig.subplots_adjust(bottom=0.25)
    ax_ky = plt.axes([0.13, 0.05, 0.65, 0.06])
    ky_slider = Slider(
        ax=ax_ky,
        label='ky',
        valmin=-fft.smpl_props.sfy / 2,
        valmax=fft.smpl_props.sfy / 2,
        valinit=0,
        valstep=fft.shifted_KY,
    )

    def update_ky(val):
        ax.pcolormesh(
            kx, freq, shifted_fft[:, to_idx(
                fft.shifted_KY, val), :], cmap='viridis',
            vmin=shifted_fft[p_min[0], p_min[1], p_min[2]] if c_scale_lim else None,
            vmax=shifted_fft[p_max[0], p_max[1], p_max[2]] if c_scale_lim else None
        )
        fig.canvas.draw_idle()

    ky_slider.on_changed(update_ky)
    plt.show()
