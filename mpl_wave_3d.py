import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation


def wave1(x, t):
    return np.cos(t - x) + np.cos(1.2 * t - 1.2 * x)


f1 = 20
f2 = 50
k1 = f1
k2 = f2


def wave2(x, y, t):
    return (np.cos(2 * np.pi * f1 * t - np.sqrt((2 * np.pi * k1 * (x - 50)) ** 2 + (2 * np.pi * k1 * (y - 50)) ** 2))
            + np.cos(2 * np.pi * f2 * t - np.sqrt(
                (2 * np.pi * k2 * (x - 50)) ** 2 + (2 * np.pi * k2 * (y - 50)) ** 2))) / 2 * np.exp(-t)


def wave3(x, y, t):
    return np.sin(2 * np.pi * t - np.sqrt((2 * np.pi * (x - 50)) ** 2 + (2 * np.pi * (y - 50)) ** 2)) / np.exp(-t)


fs = 100  # sampling frequency, (Hz)
dx = 1  # spatial sampling step along X in (mm)
dy = 1  # spatial sampling step along Y in (mm)
X = np.arange(0, 100, dx)
Y = np.arange(0, 100, dy)
T = np.arange(0, 5, 1 / fs)

x, y = np.meshgrid(X, Y)

z = np.zeros((100, 100, 500))
for t in range(len(T)):
    z[:, :, t] = wave2(x, y, T[t])


def change_plot(frame_number, z_array, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(x, y, z_array[:, :, frame_number], cmap="viridis")


def change_plot_img(frame_number, z_array, plot):
    plot[0].remove()
    plot[0] = ax.imshow(z_array[:, :, frame_number], cmap='viridis')


fps = 10

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
surface = [ax.plot_surface(x, y, z[:, :, 0], color='0.75', rstride=1, cstride=1)]
ax.set_zlim(-1, 1)
ani = animation.FuncAnimation(fig, change_plot, len(T), fargs=(z, surface), interval=1000 / fps)
plt.show()

fig2 = plt.figure()
ax = fig2.add_subplot()
image = [ax.imshow(z[:, :, 100], cmap='viridis')]
ani2 = animation.FuncAnimation(fig2, change_plot_img, len(T), fargs=(z, image), interval=1000 / fps)
plt.show()

x_max = z.shape[0]
y_max = z.shape[1]
t_max = z.shape[2]
x, y, t = np.meshgrid(X, Y, T)
z = wave2(x, y, t)
fft_wave2 = np.abs(np.fft.fftshift(np.fft.fftn(z), axes=(0, 1)))
print(fft_wave2.shape)

KX = np.linspace(-x_max / 2, x_max / 2, z.shape[0])
KY = np.linspace(-y_max / 2, y_max / 2, z.shape[1])
FREQ = np.linspace(0, fs, z.shape[2])
kx, ky, freq = np.meshgrid(KX, KY, FREQ)

fig3 = plt.figure()
ax = fig3.add_subplot()
image_fft = ax.imshow(fft_wave2[:, :, 0], cmap='viridis')
ax_freq = plt.axes([0.20, 0.01, 0.65, 0.03])
freq_slider = Slider(
    ax=ax_freq,
    label='Frequency [Hz]',
    valmin=0,
    valmax=fft_wave2.shape[2],
    valinit=0,
)


def update(val):
    ax.imshow(fft_wave2[:, :, int(val)], cmap='viridis')
    fig3.canvas.draw_idle()


freq_slider.on_changed(update)
plt.show()

fig4 = plt.figure()
ax = fig4.add_subplot()
image_fft_kx = ax.imshow(fft_wave2[0, :, :].T, cmap='viridis')
ax_kx = plt.axes([0.20, 0.01, 0.65, 0.03])
kx_slider = Slider(
    ax=ax_kx,
    label='kx',
    valmin=0,
    valmax=fft_wave2.shape[0],
    valinit=0,
)


def update_kx(val):
    ax.imshow(fft_wave2[int(val), :, :].T, cmap='viridis')
    fig4.canvas.draw_idle()


kx_slider.on_changed(update_kx)
plt.show()

fig5 = plt.figure()
ax = fig5.add_subplot()
image_fft_ky = ax.imshow(fft_wave2[:, 0, :].T, cmap='viridis')
ax_ky = plt.axes([0.20, 0.01, 0.65, 0.03])
kx_slider = Slider(
    ax=ax_ky,
    label='ky',
    valmin=0,
    valmax=fft_wave2.shape[1],
    valinit=0,
)


def update_ky(val):
    ax.imshow(fft_wave2[int(val), :, :].T, cmap='viridis')
    fig5.canvas.draw_idle()


kx_slider.on_changed(update_ky)
plt.show()
