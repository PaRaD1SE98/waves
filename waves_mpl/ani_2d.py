import numpy as np
from matplotlib import pyplot as plt, animation
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot(data, fps=10, title=None, aspect_ratio=1):
    p_min = np.unravel_index(np.argmin(data.z), data.z.shape)
    p_max = np.unravel_index(np.argmax(data.z), data.z.shape)

    def change_plot_img(frame_number, z_array, plot):
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
    image = [
        ax.pcolormesh(data.x, data.y, data.z[:, :, 0], cmap='viridis', vmin=data.z[p_min[0], p_min[1], p_min[2]],
                      vmax=data.z[p_max[0], p_max[1], p_max[2]])]
    div = make_axes_locatable(ax)
    cax = div.append_axes('right', '5%', '5%')
    fig.colorbar(image[0], label='Amplitude', cax=cax)
    ani = animation.FuncAnimation(fig, change_plot_img, len(data.T), fargs=(data.z, image), interval=1000 / fps)
    plt.show()
