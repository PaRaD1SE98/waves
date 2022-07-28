import numpy as np
import plotly
import pandas as pd
import plotly.express as px


def wave(x, y, t):
    center_x = .5
    center_y = .5
    kx1 = 40  # 1/m
    kx2 = 80  # 1/m
    kx3 = 90  # 1/m
    kx4 = 100  # 1/m
    ky1 = 40  # 1/m
    ky2 = 80  # 1/m
    ky3 = 70  # 1/m
    ky4 = 79  # 1/m
    f1 = 50  # Hz
    f2 = 70  # Hz
    f3 = 55  # Hz
    f4 = 100  # Hz
    assert sft > 2 * max(f1, f2, f3, f4), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the wave'
    assert sfx > 2 * max(kx1, kx2, kx3, kx4), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the wave'
    assert sfy > 2 * max(ky1, ky2, ky3, ky4), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the wave'
    w = np.sin(np.sqrt((2 * np.pi * kx1 * (x-center_x))**2 + (2 * np.pi * ky1 * (y-center_y))**2) + 2 * np.pi * f1 * t)
    w += np.sin(np.sqrt((2 * np.pi * kx2 * (x-center_x))**2 + (2 * np.pi * ky2 * (y-center_y))**2) + 2 * np.pi * f2 * t)
    w += np.sin(np.sqrt((2 * np.pi * kx3 * (x-center_x))**2 + (2 * np.pi * ky3 * (y-center_y))**2) + 2 * np.pi * f3 * t)
    w += np.sin(np.sqrt((2 * np.pi * kx4 * (x-center_x))**2 + (2 * np.pi * ky4 * (y-center_y))**2) + 2 * np.pi * f4 * t)
    return w / 4

def pulse(x, y, t):
    """
    y=exp(-(sqrt(x^2+y^2)-t)^2)*(sin(sqrt(x^2+y^2)-t)+cos(sqrt(x^2+y^2)-t))
    """
    center_x = 0
    center_y = .5
    f1 = 30  # Hz
    f2 = 50  # Hz
    f3 = 10  # Hz
    kx1 = 20  # 1/m
    kx2 = 40  # 1/m
    kx3 = 60  # 1/m
    ky1 = 20  # 1/m
    ky2 = 40  # 1/m
    ky3 = 60  # 1/m
    assert sft > 2 * max(f1, f2, f3), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the wave'
    assert sfx > 2 * max(kx1, kx2, kx3), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the wave'
    assert sfy > 2 * max(ky1, ky2, ky3), 'Nyquist: Make sure sampling frequency > 2 * highest frequency of the wave'
    p = np.exp(
        - (np.sqrt((2*np.pi* kx1 *(x - center_x)) ** 2 + (2*np.pi* ky1 *(y - center_y))** 2)
           - 2 * np.pi * f1 * t) ** 2)
    p *= (np.sin(np.sqrt((2*np.pi* kx2 *(x - center_x)) ** 2 + (2*np.pi* ky2 *(y - center_y))**2) - 2 * np.pi * f2 * t) + np.cos(np.sqrt((2*np.pi* kx3 *(x - center_x)) ** 2 + (2*np.pi* ky3 *(y - center_y))**2) - 2 * np.pi * f3 * t)) / 2
    return p

sp = 128  # sampling points in 1d
t_max = 1  # s
x_max = 1  # m
y_max = 1  # m
dt = t_max / sp  # sampling interval
dx = x_max / sp  # sampling interval
dy = y_max / sp  # sampling interval
sft = sp / t_max  # sampling frequency t
sfx = sp / x_max  # sampling spatial frequency x
sfy = sp / y_max  # sampling spatial frequency y

print('sampling frequency t', sft)
print('sampling frequency x', sfx)
print('sampling frequency y', sfy)
X = np.arange(0, x_max, dx)
Y = np.arange(0, y_max, dy)
T = np.arange(0, t_max, dt)
x, y, t = np.meshgrid(X, Y, T)
z = pulse(x, y, t)
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
