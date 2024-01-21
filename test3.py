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


sampling_freq = 1/dt  # Hz
data_path = os.path.join(config.DATA_BASE_DIR, config.FEM_DATA_FILENAME)
df = lsdyna_read_pd(data_path)
input_data = df[f'Sh-{shell_id}']
input_data_lower = df[f'Sh-{shell_lower_id}']
input_data_diff = input_data - input_data_lower
input_data_sum = input_data + input_data_lower

input_data = input_data_diff
print(input_data.shape)

base_dir = 'data/li/automeris/'
data_dir, degree, title = match_automeris()
title += f' FEM {distance_to_source:.1f}mm'

freq_start = 10000
freq_end = sampling_freq//2
freq_step = 10000
freqs = np.arange(freq_start, freq_end, freq_step)
normalized_freqs = freqs/sampling_freq
wavelet = 'cmor1.5-1.0'
scales = pywt.frequency2scale(wavelet, normalized_freqs)

sig_length = input_data.shape[0]
sampling_period = dt
t = sampling_period * sig_length
time = np.linspace(0, t, sig_length)
time *= 1e6  # in us

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

df_A0 = pd.read_csv(base_dir+data_dir+'A0.csv')
df_A1 = pd.read_csv(base_dir+data_dir+'A1.csv')
df_S0 = pd.read_csv(base_dir+data_dir+'S0.csv')
df_S2 = pd.read_csv(base_dir+data_dir+'S2.csv')
