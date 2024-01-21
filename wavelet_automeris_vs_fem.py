import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt

import config
from common.data_reader import lsdyna_read_pd
from theory_curve_matcher import match_automeris

"""FEM Parameters"""
dx = 0.1  # mm
dy = 0.025  # mm
dt = 1e-7  # s

# for source position in the left edge
# shell_id = 85676  # "sensor" position upper left
# shell_lower_id = 11676
# distance_to_source = 32.399  # mm lower left verify source location
# for source position in the middle
shell_id = 84750  # "sensor" position upper right 1/4
shell_lower_id = 10750
distance_to_source = 25  # mm
# shell_id = 84620  # "sensor" position upper right 3/8
# shell_lower_id = 10620
# distance_to_source = 37.5  # mm
# shell_id = 84500  # "sensor" position upper right half
# shell_lower_id = 10500
# distance_to_source = 50  # mm
# shell_id = 84250  # "sensor" position upper right 3/4
# shell_lower_id = 10250
# distance_to_source = 75  # mm
# shell_id = 84125  # "sensor" position upper right 7/8
# shell_lower_id = 10125
# distance_to_source = 87.5  # mm
# shell_id = 84001  # "sensor" position upper right edge
# shell_lower_id = 10001
# distance_to_source = 100  # mm


# sampling_freq = 1/dt  # Hz
# data_path = os.path.join(config.DATA_BASE_DIR, config.FEM_DATA_FILENAME)
# df = lsdyna_read_pd(data_path)
# input_data = df[f'Sh-{shell_id}']
# input_data_lower = df[f'Sh-{shell_lower_id}']
# input_data_diff = input_data - input_data_lower
# input_data_sum = input_data + input_data_lower

# input_data = input_data_diff
# print(input_data.shape)

base_dir = 'data/li/automeris/'
data_dir, degree, title = match_automeris()
title += f' FEM {distance_to_source:.1f}mm'

# freq_start = 10000
# freq_end = sampling_freq//2
# freq_step = 10000
# freqs = np.arange(freq_start, freq_end, freq_step)
# normalized_freqs = freqs/sampling_freq
# wavelet = 'cmor1.5-1.0'
# scales = pywt.frequency2scale(wavelet, normalized_freqs)

# sig_length = input_data.shape[0]
# sampling_period = dt
# t = sampling_period * sig_length
# time = np.linspace(0, t, sig_length)
# time *= 1e6  # in us

# plt.plot(time, input_data)
# plt.xlabel('Time (us)')
# plt.ylabel('Amplitude')
# plt.title(title)
# plt.show()

# cwtmatr, freqs = pywt.cwt(input_data, scales, wavelet, sampling_period)
# freqs *= 1e-6  # in MHz
# X, Y = np.meshgrid(freqs, time)
# # plt.plot(input_data)
# fig = plt.figure()
# ax = fig.add_subplot()
# img = ax.pcolormesh(X, Y, np.abs(cwtmatr).T, cmap='viridis')
# fig.colorbar(img)


# df_0_S = pd.read_csv(base_dir+data_dir+degree+f'_S{suffix}.txt')
# df_0_A = pd.read_csv(base_dir+data_dir+degree+f'_A{suffix}.txt')
# df_ first row is x, second row is y, no index， set first row name to Kx(1/m), second row name to Freq(Hz)
df_A0 = pd.read_csv(base_dir+data_dir+'A0.csv', header=None)
df_A1 = pd.read_csv(base_dir+data_dir+'A1.csv', header=None)
df_S0 = pd.read_csv(base_dir+data_dir+'S0.csv', header=None)
# df_S1 = pd.read_csv(base_dir+data_dir+'S1.csv', header=None)
df_S2 = pd.read_csv(base_dir+data_dir+'S2.csv', header=None)
df_A0 = df_A0.rename(columns={0: 'Kx(1/m)', 1: 'Freq(Hz)'})
df_A1 = df_A1.rename(columns={0: 'Kx(1/m)', 1: 'Freq(Hz)'})
df_S0 = df_S0.rename(columns={0: 'Kx(1/m)', 1: 'Freq(Hz)'})
# df_S1 = df_S1.rename(columns={0: 'Kx(1/m)', 1: 'Freq(Hz)'})
df_S2 = df_S2.rename(columns={0: 'Kx(1/m)', 1: 'Freq(Hz)'})
# sort by kx
df_A0 = df_A0.sort_values(by='Kx(1/m)')
df_A1 = df_A1.sort_values(by='Kx(1/m)')
df_S0 = df_S0.sort_values(by='Kx(1/m)')
# df_S1 = df_S1.sort_values(by='Kx(1/m)')
df_S2 = df_S2.sort_values(by='Kx(1/m)')
print(df_A0)

distance_to_pzt = distance_to_source * 1e-3  # m
# x_multiplyer = 1e-3  # MHz
# y_multiplyer = 1e3  # us
# ax.plot(df_0_S['S0 f (kHz)']*x_multiplyer, distance_to_pzt /
#         df_0_S['S0 Energy velocity (m/ms)']*y_multiplyer, '--', label='S0', color='blue')
# ax.plot(df_0_S['S1 f (kHz)']*x_multiplyer, distance_to_pzt /
#         df_0_S['S1 Energy velocity (m/ms)']*y_multiplyer, '--', label='S1', color='orange')
# ax.plot(df_0_S['S2 f (kHz)']*x_multiplyer, distance_to_pzt /
#         df_0_S['S2 Energy velocity (m/ms)']*y_multiplyer, '--', label='S2', color='purple')
# ax.plot(df_0_A['A0 f (kHz)']*x_multiplyer, distance_to_pzt /
#         df_0_A['A0 Energy velocity (m/ms)']*y_multiplyer, label='A0', color='red')
# ax.plot(df_0_A['A1 f (kHz)']*x_multiplyer, distance_to_pzt /
#         df_0_A['A1 Energy velocity (m/ms)']*y_multiplyer, label='A1', color='green')

fig = plt.figure()
ax = fig.add_subplot()
# df_ second row is x, first row is y
ax.plot(df_A0['Freq(Hz)'], df_A0['Kx(1/m)'], label='A0', color='red')
ax.plot(df_A1['Freq(Hz)'], df_A1['Kx(1/m)'], label='A1', color='green')
ax.plot(df_S0['Freq(Hz)'], df_S0['Kx(1/m)'], '--', label='S0', color='blue')
# ax.plot(df_S1['Freq(Hz)'], df_S1['Kx(1/m)'], '--', label='S1', color='orange')
ax.plot(df_S2['Freq(Hz)'], df_S2['Kx(1/m)'], '--', label='S2', color='purple')
plt.legend(loc='upper right')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Arrival Time (us)')
plt.title(title)
# plt.xlim(0, 1.75)
# plt.ylim(0, 150)
plt.tight_layout()
plt.show()

# save figure
save_dir = os.path.join(config.DATA_BASE_DIR,
                        'results',
                        'wavelet_theory_vs_fem')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
fig.savefig(
    os.path.join(
        save_dir,
        config.FEM_DATA_FILENAME.replace(
            '.csv', '')+f'-{distance_to_source}mm'+'.png'
    )
)
