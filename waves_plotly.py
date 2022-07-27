import numpy as np
import plotly
import pandas as pd
import plotly.express as px


def wave1(x, t):
    return np.cos(t - x) + np.cos(1.2 * t - 1.2 * x)


def wave2(x, y, t):
    f1 = 20
    f2 = 50
    k1 = f1
    k2 = f2

    return (np.cos(2 * np.pi * f1 * t - np.sqrt((2 * np.pi * k1 * (x - 50)) ** 2 + (2 * np.pi * k1 * (y - 50)) ** 2))
            + np.cos(2 * np.pi * f2 * t - np.sqrt(
                (2 * np.pi * k2 * (x - 50)) ** 2 + (2 * np.pi * k2 * (y - 50)) ** 2))) / 2 * np.exp(-t)


def wave3(x, y, t):
    return np.sin(2 * np.pi * t - np.sqrt((2 * np.pi * (x - 50)) ** 2 + (2 * np.pi * (y - 50)) ** 2)) / np.exp(-t)


def pulse1(x, y, t):
    return 4 * np.sqrt((x - 50) ** 2 + (y - 50) ** 2) + 5 * t + 4


def pulse2(x, y, t):
    """
    y=exp(-(sqrt(x^2+y^2)-t)^2)*(sin(sqrt(x^2+y^2)-t)+cos(sqrt(x^2+y^2)-t))
    """
    center_x = 0
    center_y = 50
    omega_0 = 2 * np.pi * 10  # 2 * pi * f
    omega_1 = 2 * np.pi * 20  # 2 * pi * f
    omega_2 = 2 * np.pi * 30  # 2 * pi * f
    k_0 = 1
    k_1 = 2
    k_2 = 3

    return np.exp(-1 / 50 * (np.sqrt(k_0 * (x - center_x) ** 2 + k_0 * (y - center_y) ** 2) - omega_0 * t) ** 2) * 0.5 \
           * (np.sin(np.sqrt(k_1 * (x - center_x) ** 2 + k_1 * (y - center_y) ** 2) - omega_1 / 2 * t) +
              np.cos(np.sqrt(k_2 * (x - center_x) ** 2 + k_2 * (y - center_y) ** 2) - omega_2 / 5 * t))


resolution_x = 100  # steps_x
resolution_y = 100  # steps_y
resolution_t = 100  # steps_t

x_max = 100  # m
y_max = 100  # m
t_max = 2  # s

Fs = resolution_t / t_max  # sampling frequency, (Hz)
Kxs = resolution_x / x_max  # spatial sampling frequency along X in (1/m)
Kys = resolution_y / y_max  # spatial sampling frequency along Y in (1/m)
print('Fs', Fs)
print('Kxs', Kxs)
print('Kys', Kys)
X = np.arange(0, x_max, 1 / Kxs)
Y = np.arange(0, y_max, 1 / Kys)
T = np.arange(0, t_max, 1 / Fs)
x, y, t = np.meshgrid(X, Y, T)
z = pulse2(x, y, t)
print('z.shape', z.shape)
data = {'x': x.flatten(), 'y': y.flatten(), 't': t.flatten(), 'z': z.flatten()}
df = pd.DataFrame(data)
fig = px.scatter_3d(df, 'x', 'y', 'z', animation_frame='t', range_z=(-2, 2))
fig.update_traces(marker_size=1)
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig.show()

fig2 = px.density_heatmap(df, 'x', 'y', 'z',
                          animation_frame='t',
                          nbinsx=resolution_x,
                          nbinsy=resolution_y,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig2.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig2.show()

Kx_range = -Kxs / 4, Kxs / 4
Ky_range = -Kys / 4, Kys / 4
F_range = 0, Fs / 2
# Nyquist check
assert Kx_range[1] - Kx_range[0] <= Kxs / 2
assert Ky_range[1] - Ky_range[0] <= Kys / 2
assert F_range[1] - F_range[0] <= Fs / 2

KX = np.linspace(*Kx_range, resolution_x)
KY = np.linspace(*Ky_range, resolution_y)
FREQ = np.linspace(*F_range, resolution_t)

fft_result = np.abs(np.fft.fftshift(np.fft.fftn(z), axes=(0, 1)))
kx, ky, freq = np.meshgrid(KX, KY, FREQ)
data_fft = {'kx': kx.flatten(), 'ky': ky.flatten(), 'freq': freq.flatten(), 'amplitude': fft_result.flatten()}
df_fft = pd.DataFrame(data_fft)
fig3 = px.density_heatmap(df_fft, 'kx', 'ky', 'amplitude',
                          animation_frame='freq',
                          nbinsx=resolution_x,
                          nbinsy=resolution_y,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig3.update_yaxes(
    scaleanchor="x",
    scaleratio=Kxs / Kys,
)
fig3.show()

KX = np.linspace(-Kxs / 4, Kxs / 4, resolution_x)
KY = np.linspace(-Kys / 4, Kys / 4, resolution_y)
FREQ = np.linspace(0, Fs / 2, resolution_t)
kx, ky, freq = np.meshgrid(KX, KY, FREQ)
data_fft = {'kx': kx.flatten(), 'ky': ky.flatten(), 'freq': freq.flatten(), 'amplitude': fft_result.flatten()}
df_fft = pd.DataFrame(data_fft)
fig4 = px.density_heatmap(df_fft, 'kx', 'freq', 'amplitude',
                          animation_frame='ky',
                          nbinsx=resolution_x,
                          nbinsy=resolution_t,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig4.update_yaxes(
    scaleanchor="x",
    scaleratio=Kxs / Fs,
)
fig4.show()

fig5 = px.density_heatmap(df_fft, 'ky', 'freq', 'amplitude',
                          animation_frame='kx',
                          nbinsx=resolution_y,
                          nbinsy=resolution_t,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig5.update_yaxes(
    scaleanchor="x",
    scaleratio=Kys / Fs,
)
fig5.show()
