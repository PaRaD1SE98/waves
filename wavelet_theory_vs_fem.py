import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt

import config
from common.data_reader import lsdyna_read_pd
from theory_curve_matcher import match_fem

"""FEM Parameters"""
dx = 0.1  # mm
dy = 0.025  # mm
dt = 1e-7  # s

# for source position in the left edge
# shell_id = 85676  # "sensor" position upper left
# distance_to_source = 32.399  # mm lower left verify source location
# for source position in the middle
shell_id = 84750  # "sensor" position upper right 1/4
distance_to_source = 25  # mm
# shell_id = 84620  # "sensor" position upper right 3/8
# distance_to_source = 37.5  # mm
shell_id = 84500  # "sensor" position upper right half
distance_to_source = 50  # mm
# shell_id = 84250  # "sensor" position upper right 3/4
# distance_to_source = 75  # mm
# shell_id = 84125  # "sensor" position upper right 7/8
# distance_to_source = 87.5  # mm
# shell_id = 84001  # "sensor" position upper right edge
# distance_to_source = 100  # mm


sampling_freq = 1/dt  # Hz
data_path = os.path.join(config.DATA_BASE_DIR, config.FEM_DATA_FILENAME)
df = lsdyna_read_pd(data_path)
input_data = df[f'Sh-{shell_id}']
print(input_data.shape)
plt.plot(input_data)
plt.show()

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
cwtmatr, freqs = pywt.cwt(input_data, scales, wavelet, sampling_period)
freqs *= 1e-6  # in MHz
X, Y = np.meshgrid(freqs, time)
# plt.plot(input_data)
fig = plt.figure()
ax = fig.add_subplot()
img = ax.pcolormesh(X, Y, np.abs(cwtmatr).T, cmap='viridis')
fig.colorbar(img)

base_dir = 'data/li/disp_calc/'

data_dir, degree, suffix, title = match_fem()

title += f' FEM {distance_to_source:.1f}mm'

df_0_S = pd.read_csv(base_dir+data_dir+degree+f'_S{suffix}.txt')
df_0_A = pd.read_csv(base_dir+data_dir+degree+f'_A{suffix}.txt')

distance_to_pzt = distance_to_source * 1e-3  # m
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
plt.xlabel('Frequency (MHz)')
plt.ylabel('Arrival Time (us)')
plt.title(title)
plt.xlim(0, 1.75)
plt.ylim(0, 150)
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
