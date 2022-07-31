import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def f_val_to_idx(smpl_props, v):
    return int(round(v * smpl_props.t_max))


def plot(fft, shifted_fft, title=None, c_scale_lim=False, aspect_ratio=None):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(title)
    ax.set_xlabel('Kx')
    ax.set_ylabel('Ky')
    if aspect_ratio is not None:
        if aspect_ratio == 'as_sample':
            ax.set_aspect(fft.smpl_props.spy / fft.smpl_props.spx)
        elif aspect_ratio == 'as_value':
            ax.set_aspect(fft.smpl_props.sfy / fft.smpl_props.sfx)
        elif type(aspect_ratio) == float:
            ax.set_aspect(aspect_ratio)
    kx, ky = np.meshgrid(fft.KX, fft.KY, indexing='ij')
    image_fft = ax.pcolormesh(
        kx, ky, shifted_fft[:, :, 0], cmap='viridis',
        vmin=shifted_fft[p_min[0], p_min[1], p_min[2]] if c_scale_lim else None,
        vmax=shifted_fft[p_max[0], p_max[1], p_max[2]] if c_scale_lim else None
    )
    fig.colorbar(image_fft, label='Amplitude')
    fig.subplots_adjust(bottom=0.25)
    ax_freq = plt.axes([0.20, 0.05, 0.65, 0.06])
    freq_slider = Slider(
        ax=ax_freq,
        label='Freq',
        valmin=0,
        valmax=fft.smpl_props.sft / 2,
        valinit=0,
        valstep=fft.smpl_props.sft / fft.smpl_props.sp[0],
    )

    def update(val):
        ax.pcolormesh(
            kx, ky, shifted_fft[:, :, f_val_to_idx(fft.smpl_props, val)], cmap='viridis',
            vmin=shifted_fft[p_min[0], p_min[1], p_min[2]] if c_scale_lim else None,
            vmax=shifted_fft[p_max[0], p_max[1], p_max[2]] if c_scale_lim else None
        )
        fig.canvas.draw_idle()

    freq_slider.on_changed(update)
    plt.show()
