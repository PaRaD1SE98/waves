import numpy as np
import plotly
import pandas as pd
import plotly.express as px


class Wave:
    center = [.5, .5]  # x, y
    frequency = [50, 70, 55, 100]  # Hz
    wave_number_x = [40, 80, 90, 100]  # 1/m
    wave_number_y = [40, 80, 70, 79]  # 1/m

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def __call__(self, *args, **kwargs):
        w = np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[0] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[0] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[0] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[1] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[1] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[1] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[2] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[2] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[2] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[3] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[3] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[3] * self.t)
        return w / 4


class Pulse:
    """
    y=exp(-(sqrt(x^2+y^2)-t)^2) * (sin(sqrt(x^2+y^2)-t)+cos(sqrt(x^2+y^2)-t))
    """
    center = [0, .5]  # x, y
    frequency = [30, 50, 80]  # Hz
    wave_number_x = [20, 40, 60]  # 1/m
    wave_number_y = [20, 40, 60]  # 1/m

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def __call__(self, *args, **kwargs):
        p = np.exp(
            - (np.sqrt(
                (2 * np.pi * self.wave_number_x[0] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[0] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[0] * self.t) ** 2
        )
        p *= np.sin(
            np.sqrt(
                (2 * np.pi * self.wave_number_x[1] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[1] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[1] * self.t
        ) + \
            np.cos(
                np.sqrt(
                    (2 * np.pi * self.wave_number_x[2] * (self.x - self.center[0])) ** 2 +
                    (2 * np.pi * self.wave_number_y[2] * (self.y - self.center[1])) ** 2
                ) - 2 * np.pi * self.frequency[2] * self.t
            )
        return p / 2


sp = 256  # sampling points in 1d
t_max = 1
x_max = 1
y_max = 1
dt = t_max / sp  # sampling interval (s)
dx = x_max / sp  # sampling interval (m)
dy = y_max / sp  # sampling interval (m
sft = sp / t_max  # sampling temporal frequency (sampling points in 1s) t
sfx = sp / x_max  # sampling spatial frequency (sampling points in 1m) x
sfy = sp / y_max  # sampling spatial frequency (sampling points in 1m) y

print('sampling temporal frequency (sampling points in 1s) t', sft, 'Hz')
print('sampling spatial frequency (sampling points in 1m) x', sfx, '1/m')
print('sampling spatial frequency (sampling points in 1m) y', sfy, '1/m')

T = np.arange(0, t_max, dt)
X = np.arange(0, x_max, dx)
Y = np.arange(0, y_max, dy)
x, y, t = np.meshgrid(X, Y, T)

Signal = Pulse  # choose the signal to be analyzed
z = Signal(x, y, t)()
assert sft > 2 * max(Signal.frequency), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the signal'
assert sfx > 2 * max(Signal.wave_number_x), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the signal'
assert sfy > 2 * max(Signal.wave_number_y), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the signal'
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
                          nbinsx=sp,
                          nbinsy=sp,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig2.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig2.show()

Kx_range = -sfx / 2, sfx / 2
Ky_range = -sfy / 2, sfy / 2
F_range = 0, sft / 2

KX = np.arange(-sfx / 2, sfx / 2, sfx / sp)
KY = np.arange(-sfy / 2, sfy / 2, sfy / sp)
FREQ = np.arange(0, sft, sft / sp)

fft_result = np.abs(np.fft.fftshift(np.fft.fftn(z), axes=(0, 1)))
kx, ky, freq = np.meshgrid(KX, KY, FREQ)
data_fft = {'kx': kx.flatten(), 'ky': ky.flatten(), 'freq': freq.flatten(), 'amplitude': fft_result.flatten()}
df_fft = pd.DataFrame(data_fft)
fig3 = px.density_heatmap(df_fft, 'kx', 'ky', 'amplitude',
                          animation_frame='freq',
                          nbinsx=sp,
                          nbinsy=sp,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig3.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig3.show()

kx, ky, freq = np.meshgrid(KX, KY, FREQ)
data_fft = {'kx': kx.flatten(), 'ky': ky.flatten(), 'freq': freq.flatten(), 'amplitude': fft_result.flatten()}
df_fft = pd.DataFrame(data_fft)
fig4 = px.density_heatmap(df_fft, 'kx', 'freq', 'amplitude',
                          animation_frame='ky',
                          nbinsx=sp,
                          nbinsy=sp,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig4.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig4.show()

fig5 = px.density_heatmap(df_fft, 'ky', 'freq', 'amplitude',
                          animation_frame='kx',
                          nbinsx=sp,
                          nbinsy=sp,
                          color_continuous_scale=plotly.colors.sequential.Viridis)
fig5.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
fig5.show()
