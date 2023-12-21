import numpy as np
import matplotlib.pyplot as plt
from common.utils import to_idx
from prepare.fem import fft
import pandas as pd

from theory_curve_matcher import match_fem

c_scale_lim = True
shifted_fft = fft.shifted_abs_fft
p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('Kx(1/m)')
ax.set_ylabel('Freq(Hz)')
kx, freq = np.meshgrid(fft.shifted_KX, fft.FREQ, indexing='ij')
image_fft_ky = ax.pcolormesh(
    kx, freq, shifted_fft[:, to_idx(fft.shifted_KY, 0), :], cmap='viridis',
    vmin=shifted_fft[p_min[0], p_min[1], p_min[2]] if c_scale_lim else None,
    vmax=shifted_fft[p_max[0], p_max[1], p_max[2]] if c_scale_lim else None
)
plt.ylim(0, fft.smpl_props.sft / 2)  # set valid frequency window
fig.colorbar(image_fft_ky)


def convert_rad_mm_to_1_m(x):
    """
    convert rad/mm to 1/m
    """
    return x * 1000 / (2 * np.pi)


def convert_khz_to_hz(x):
    """
    convert kHz to Hz
    """
    return x * 1000


base_dir = 'data/li/disp_calc/'

data_dir, degree, suffix, title = match_fem()

title += ' FEM'

df_0_S = pd.read_csv(base_dir+data_dir+degree+f'_S{suffix}.txt')
df_0_A = pd.read_csv(base_dir+data_dir+degree+f'_A{suffix}.txt')

df_0_S['S0 Wavenumber (rad/mm)'] = df_0_S['S0 Wavenumber (rad/mm)'].apply(
    convert_rad_mm_to_1_m)
df_0_S['S1 Wavenumber (rad/mm)'] = df_0_S['S1 Wavenumber (rad/mm)'].apply(
    convert_rad_mm_to_1_m)
df_0_S['S2 Wavenumber (rad/mm)'] = df_0_S['S2 Wavenumber (rad/mm)'].apply(
    convert_rad_mm_to_1_m)

df_0_A['A0 Wavenumber (rad/mm)'] = df_0_A['A0 Wavenumber (rad/mm)'].apply(
    convert_rad_mm_to_1_m)
df_0_A['A1 Wavenumber (rad/mm)'] = df_0_A['A1 Wavenumber (rad/mm)'].apply(
    convert_rad_mm_to_1_m)

df_0_S['S0 f (kHz)'] = df_0_S['S0 f (kHz)'].apply(convert_khz_to_hz)
df_0_S['S1 f (kHz)'] = df_0_S['S1 f (kHz)'].apply(convert_khz_to_hz)
df_0_S['S2 f (kHz)'] = df_0_S['S2 f (kHz)'].apply(convert_khz_to_hz)

df_0_A['A0 f (kHz)'] = df_0_A['A0 f (kHz)'].apply(convert_khz_to_hz)
df_0_A['A1 f (kHz)'] = df_0_A['A1 f (kHz)'].apply(convert_khz_to_hz)

ax.plot(df_0_S['S0 Wavenumber (rad/mm)'],
        df_0_S['S0 f (kHz)'], '--', label='S0', color='blue')
ax.plot(df_0_S['S1 Wavenumber (rad/mm)'],
        df_0_S['S1 f (kHz)'], '--', label='S1', color='orange')
ax.plot(df_0_S['S2 Wavenumber (rad/mm)'],
        df_0_S['S2 f (kHz)'], '--', label='S2', color='purple')

ax.plot(df_0_A['A0 Wavenumber (rad/mm)'], 
        df_0_A['A0 f (kHz)'], label='A0', color='red')
ax.plot(df_0_A['A1 Wavenumber (rad/mm)'], 
        df_0_A['A1 f (kHz)'], label='A1', color='green')
plt.legend(loc='upper right')
# plt.xlabel('Kx(1/m)')
# plt.ylabel('Freq(Hz)')
plt.title(title)
plt.xlim(0, 500)
plt.ylim(0, 2e6)
plt.tight_layout()
plt.show()
