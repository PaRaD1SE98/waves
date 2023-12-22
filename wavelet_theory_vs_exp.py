import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt

import config
from prepare.real import data
from theory_curve_matcher import match_exp

d_from_edge_to_point = 0.0  # m distance from scan edge to point
d_from_sensor_to_edge = 0.02  # m distance from sensor to the closest scan edge

sampling_freq = data.sample_props.sft
freq_start = 10000
freq_end = sampling_freq//2
freq_step = 10000
freqs = np.arange(freq_start, freq_end, freq_step)
normalized_freqs = freqs/sampling_freq
wavelet = 'cmor1.5-1.0'
scales = pywt.frequency2scale(wavelet, normalized_freqs)

total_distance = (data.z.shape[0]-1) * data.sample_props.dx  # m
print('total_distance', total_distance, 'm')


def get_index_by_distance(distance):
    """
    distance: m
    """
    assert distance <= total_distance
    # larger distance means smaller index
    return data.z.shape[0] - 1 - int(distance / data.sample_props.dx)


index = get_index_by_distance(d_from_edge_to_point)  # data index
print('index', index)
input_data = data.z[index, data.z.shape[1]//2, :]  # (x, y, t)
plt.plot(input_data)
plt.show()
sig_length = input_data.shape[0]
sampling_period = data.sample_props.dt
t = sampling_period * sig_length
time = np.linspace(0, t, sig_length)
time *= 1e6  # in us
cwtmatr, freqs = pywt.cwt(input_data, scales, wavelet, sampling_period)
freqs *= 1e-6  # in MHz
X, Y = np.meshgrid(freqs, time)
# plt.plot(input_data)
fig = plt.figure()
ax = fig.add_subplot()
img = ax.pcolormesh(X, Y, np.abs(cwtmatr).T, cmap='viridis')
fig.colorbar(img)

base_dir = 'data/li/disp_calc/'

data_dir, degree, suffix, title = match_exp()

df_0_S = pd.read_csv(base_dir+data_dir+degree+f'_S{suffix}.txt')
df_0_A = pd.read_csv(base_dir+data_dir+degree+f'_A{suffix}.txt')
distance_to_pzt = d_from_sensor_to_edge + d_from_edge_to_point  # m
title += f' EXP {distance_to_pzt*1e3:.1f}mm'
x_multiplyer = 1e-3  # MHz
y_multiplyer = 1e3  # us
ax.plot(df_0_S['S0 f (kHz)']*x_multiplyer, distance_to_pzt /
        df_0_S['S0 Energy velocity (m/ms)']*y_multiplyer, '--', label='S0', color='blue')
ax.plot(df_0_S['S1 f (kHz)']*x_multiplyer, distance_to_pzt /
        df_0_S['S1 Energy velocity (m/ms)']*y_multiplyer, '--', label='S1', color='orange')
ax.plot(df_0_S['S2 f (kHz)']*x_multiplyer, distance_to_pzt /
        df_0_S['S2 Energy velocity (m/ms)']*y_multiplyer, '--', label='S2', color='purple')
ax.plot(df_0_A['A0 f (kHz)']*x_multiplyer, distance_to_pzt /
        df_0_A['A0 Energy velocity (m/ms)']*y_multiplyer, label='A0', color='red')
ax.plot(df_0_A['A1 f (kHz)']*x_multiplyer, distance_to_pzt /
        df_0_A['A1 Energy velocity (m/ms)']*y_multiplyer, label='A1', color='green')
plt.legend(loc='upper right')
plt.xlabel('Freq(MHz)')
plt.ylabel('Arrival Time(us)')
plt.title(title)
plt.xlim(0, 1.75)
plt.ylim(0, 150)
plt.tight_layout()
plt.show()

# save figure
save_dir = os.path.join(config.DATA_BASE_DIR,
                        'results',
                        'wavelet_theory_vs_exp')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
fig.savefig(
    os.path.join(
        save_dir,
        f'{data_dir[:-1]}-{degree}-{distance_to_pzt*1e3:.1f}mm.png'
    )
)
