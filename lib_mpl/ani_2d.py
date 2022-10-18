import os
from matplotlib.widgets import Slider
import numpy as np
from matplotlib import animation, pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import config
from common.utils import PauseAnimation, to_idx


def plot(data, fps=10, title=None, aspect_ratio=1, **kwargs):
    p_min = np.unravel_index(np.argmin(data.z), data.z.shape)
    p_max = np.unravel_index(np.argmax(data.z), data.z.shape)

    def change_plot_img(frame_number, z_array, plot, ignore_slider=False):
        if not ignore_slider:
            # set slider text value but not trigger slider event
            val = data.T[frame_number]
            xy = step_slider.poly.xy
            xy[2] = val, .75
            xy[3] = val, .25
            step_slider._handle.set_xdata([val])
            step_slider.poly.xy = xy
            step_slider.valtext.set_text(
                step_slider._format(val))
        # update plot
        plot[0].remove()
        plot[0] = ax.pcolormesh(data.x, data.y, z_array[:, :, frame_number], cmap='viridis',
                                vmin=z_array[p_min[0], p_min[1], p_min[2]],
                                vmax=z_array[p_max[0], p_max[1], p_max[2]])

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(title)
    ax.set_aspect(aspect_ratio)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    # slider
    fig.subplots_adjust(bottom=0.2)
    ax_slider = fig.add_axes([0.2, 0.025, 0.6, 0.05])
    step_slider = Slider(
        ax=ax_slider,
        label='t[s]',
        valmin=data.T[0],
        valmax=data.T[-1],
        valinit=data.T[0],
        valstep=data.T,
    )

    def update_slider(val):
        change_plot_img(to_idx(data.T, val), data.z, image, ignore_slider=True)
    step_slider.on_changed(update_slider)

    image = [
        ax.pcolormesh(data.x, data.y, data.z[:, :, 0], cmap='viridis', vmin=data.z[p_min[0], p_min[1], p_min[2]],
                      vmax=data.z[p_max[0], p_max[1], p_max[2]])]
    div = make_axes_locatable(ax)
    cax = div.append_axes('right', '5%', '5%')
    fig.colorbar(image[0], label='Amplitude', cax=cax)
    ani = PauseAnimation(fig, change_plot_img, len(
        data.T), fargs=(data.z, image), interval=1000 / fps)
    plt.show()

    if config.MPL_ANI_OUTPUT:
        if not os.path.exists('output'):
            os.mkdir('output')
        if not os.path.exists('output/videos'):
            os.mkdir('output/videos')
        writer = animation.FFMpegWriter(
            codec="h264", fps=round(fps * config.MPL_ANI_OUTPUT_SPEED))
        output_name = f'{"origin" if kwargs.get("origin",False) else "filterd"}' \
            f'-{__name__.split(".")[-1]}' \
            f'-{config.DATA_BASE_DIR.split("/")[1] if config.DATA_SOURCE == "real" else "simulation"}' \
            f'-speed-{config.MPL_ANI_OUTPUT_SPEED}'
        ani.animation.save(f'output/videos/{output_name}.mp4', writer=writer,
                           progress_callback=lambda i, n: print(f'Saving frame {i} of {n}', end='\r'))
