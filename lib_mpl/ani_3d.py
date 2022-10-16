import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def plot(data, fps=10, title=None, **kwargs):
    p_min = np.unravel_index(np.argmin(data.z), data.z.shape)
    p_max = np.unravel_index(np.argmax(data.z), data.z.shape)

    def change_plot(frame_number, z_array, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(data.x, data.y, z_array[:, :, frame_number], cmap="viridis",
                                  vmin=z_array[p_min[0], p_min[1], p_min[2]],
                                  vmax=z_array[p_max[0], p_max[1], p_max[2]])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    surface = [ax.plot_surface(data.x, data.y, data.z[:, :, 0], cmap="viridis",
                               vmin=data.z[p_min[0], p_min[1], p_min[2]],
                               vmax=data.z[p_max[0], p_max[1], p_max[2]]
                               )]
    ax.set_zlim(data.z[p_min[0], p_min[1], p_min[2]], data.z[p_max[0], p_max[1], p_max[2]])
    ani = animation.FuncAnimation(fig, change_plot, len(data.T), fargs=(data.z, surface), interval=1000 / fps)
    plt.show()
