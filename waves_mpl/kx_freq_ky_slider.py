import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def ky_val_to_idx(smpl_props, v):
    return int(round((v + smpl_props.sfy / 2) * smpl_props.y_max))


def plot(smpl_props, fft, shifted_fft):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

    fig4 = plt.figure()
    ax4 = fig4.add_subplot()
    ax4.set_xlabel('Kx')
    ax4.set_ylabel('Freq')
    kx, freq = np.meshgrid(fft.KX, fft.FREQ, indexing='ij')
    image_fft_ky = ax4.pcolormesh(kx, freq, shifted_fft[:, ky_val_to_idx(smpl_props, 0), :], cmap='viridis',
                                  vmin=shifted_fft[p_min[0], p_min[1], p_min[2]],
                                  vmax=shifted_fft[p_max[0], p_max[1], p_max[2]])
    plt.ylim(0, smpl_props.sft / 2)  # set valid frequency window
    # ax4.set_aspect(x / y)
    fig4.colorbar(image_fft_ky, label='Amplitude')
    fig4.subplots_adjust(bottom=0.25)
    ax_ky = plt.axes([0.20, 0.05, 0.65, 0.06])
    ky_slider = Slider(
        ax=ax_ky,
        label='ky',
        valmin=-smpl_props.sfy / 2,
        valmax=smpl_props.sfy / 2,
        valinit=0,
        valstep=smpl_props.sfy / smpl_props.sp,
    )

    def update_ky(val):
        ax4.pcolormesh(kx, freq, shifted_fft[:, ky_val_to_idx(smpl_props, val), :], cmap='viridis',
                       vmin=shifted_fft[p_min[0], p_min[1], p_min[2]],
                       vmax=shifted_fft[p_max[0], p_max[1], p_max[2]])
        fig4.canvas.draw_idle()

    ky_slider.on_changed(update_ky)
    plt.show()
