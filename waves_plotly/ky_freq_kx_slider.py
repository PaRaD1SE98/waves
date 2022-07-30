import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def kx_val_to_idx(smpl_props, v):
    return int(round((v + smpl_props.sfx / 2) * smpl_props.x_max))


def plot(smpl_props, fft, shifted_fft):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Kx')
    ax.set_ylabel('Freq')
    ky, freq = np.meshgrid(fft.KY, fft.FREQ, indexing='ij')
    image_fft_kx = ax.pcolormesh(ky, freq, shifted_fft[kx_val_to_idx(smpl_props, 0), :, :], cmap='viridis',
                                 vmin=shifted_fft[p_min[0], p_min[1], p_min[2]],
                                 vmax=shifted_fft[p_max[0], p_max[1], p_max[2]])
    plt.ylim(0, smpl_props.sft / 2)  # set valid frequency window
    # ax.set_aspect(x / y)
    fig.colorbar(image_fft_kx, label='Amplitude')
    fig.subplots_adjust(bottom=0.25)
    ax_kx = plt.axes([0.20, 0.05, 0.65, 0.06])
    kx_slider = Slider(
        ax=ax_kx,
        label='kx',
        valmin=-smpl_props.sfx / 2,
        valmax=smpl_props.sfx / 2,
        valinit=0,
        valstep=smpl_props.sfx / smpl_props.sp,
    )

    def update_kx(val):
        ax.pcolormesh(ky, freq, shifted_fft[kx_val_to_idx(smpl_props, val), :, :], cmap='viridis',
                      vmin=shifted_fft[p_min[0], p_min[1], p_min[2]],
                      vmax=shifted_fft[p_max[0], p_max[1], p_max[2]])
        fig.canvas.draw_idle()

    kx_slider.on_changed(update_kx)
    plt.show()
