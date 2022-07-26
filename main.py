import numpy as np
import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def wave1(x, t):
    return np.cos(t - x) + np.cos(1.2 * t - 1.2 * x)


f1 = 20
f2 = 50
k1 = f1
k2 = f2


def wave2(x, y, t):
    return (np.cos(2 * np.pi * f1 * t - np.sqrt((2 * np.pi * k1 * (x - 50)) ** 2 + (2 * np.pi * k1 * (y - 50)) ** 2))
            + np.cos(2 * np.pi * f2 * t - np.sqrt(
                (2 * np.pi * k2 * (x - 50)) ** 2 + (2 * np.pi * k2 * (y - 50)) ** 2))) \
           / 2 * np.exp(-t)


def wave3(x, y, t):
    return np.sin(2 * np.pi * t - np.sqrt((2 * np.pi * (x - 50)) ** 2 + (2 * np.pi * (y - 50)) ** 2)) / np.exp(-t)


fs = 100  # sampling frequency, (Hz)
dx = 1  # spatial sampling step along X in (mm)
dy = 1  # spatial sampling step along Y in (mm)
X = np.arange(0, 100, dx)
Y = np.arange(0, 100, dy)
T = np.arange(0, 1, 1 / fs)
x, y, t = np.meshgrid(X, Y, T)
z = wave2(x, y, t)
x_max = z.shape[0]
y_max = z.shape[1]
t_max = z.shape[2]
data = {'x': x.flatten(), 'y': y.flatten(), 't': t.flatten(), 'z': z.flatten()}
df = pd.DataFrame(data)
fig = px.scatter_3d(df, 'x', 'y', 'z', animation_frame='t', range_z=(-2, 2))
fig.update_traces(marker_size=1)
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)

fig.show()
fig2 = px.scatter(df, 'x', 'y', color='z', animation_frame='t', symbol_sequence=['square'],
                  color_continuous_scale=plotly.colors.sequential.Viridis)
fig2.update_traces(marker_size=6)
fig2.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig2.show()
fft_wave2 = np.abs(np.fft.fftshift(np.fft.fftn(z), axes=(0, 1)))
print(fft_wave2.shape)

KX = np.linspace(-x_max / 2, x_max / 2, z.shape[0])
KY = np.linspace(-y_max / 2, y_max / 2, z.shape[1])
FREQ = np.linspace(0, fs, z.shape[2])
kx, ky, freq = np.meshgrid(KX, KY, FREQ)
data_fft = {'kx': kx.flatten(), 'ky': ky.flatten(), 'freq': freq.flatten(), 'amplitude': fft_wave2.flatten()}
df_fft = pd.DataFrame(data_fft)
fig3 = px.scatter(df_fft, 'kx', 'ky', color='amplitude', animation_frame='freq', symbol_sequence=['square'],
                  color_continuous_scale=plotly.colors.sequential.Viridis)
fig3.update_traces(marker_size=10)
fig3.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig3.show()
fig4 = px.scatter(df_fft, 'kx', 'freq', color='amplitude', animation_frame='ky', symbol_sequence=['square'],
                  color_continuous_scale=plotly.colors.sequential.Viridis)
fig4.update_traces(marker_size=10)
fig4.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig4.show()
fig5 = px.scatter(df_fft, 'ky', 'freq', color='amplitude', animation_frame='kx', symbol_sequence=['square'],
                  color_continuous_scale=plotly.colors.sequential.Viridis)
fig5.update_traces(marker_size=10)
fig5.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig5.show()
