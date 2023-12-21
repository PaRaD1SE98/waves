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
shell_id = 85676  # "sensor" position upper right half
# distance_to_source = 51.0992  # mm
distance_to_source = 30  # mm lower left verify source location
data_filename = 'data-left-upper-1.5'

"""
LOADING NODES ID

middle upper 4     layer:  99072, 99071
middle upper 3.5   layer: 105075, 105074
middle upper 3     layer:  85065, 85064
middle upper 2.5   layer:  91068, 91067
middle upper 2     layer:  71058, 71057
middle upper 1.5   layer:  77061, 77060
middle upper 1     layer:  57051, 57050
middle upper 0.5   layer:  63054, 63053
middle center      layer:  43044, 43043
middle lower 0.5   layer:  49047, 49046
middle lower 1     layer:  29037, 29036
middle lower 1.5   layer:  35040, 35039
middle lower 2     layer:  15030, 15029
middle lower 2.5   layer:  21033, 21032
middle lower 3     layer:   1023, 1022
middle lower 3.5   layer:   7026, 7025
middle lower 4     layer:  13029, 13028

left upper 4   layer: 100050
left upper 3.5 layer: 106053
left upper 3   layer: 86043
left upper 2.5 layer: 92046
left upper 2   layer: 72036
left upper 1.5 layer: 78039
left upper 1   layer: 58029
left upper 0.5 layer: 64032
left center    layer: 44022
left lower 0.5 layer: 50025
left lower 1   layer: 30015
left lower 1.5 layer: 36018
left lower 2   layer: 16008
left lower 2.5 layer: 22011
left lower 3   layer:  2001
left lower 3.5 layer:  8004
left lower 4   layer: 14007

in [0/0/90/90]s
load posision should be -2 ~ 2
in [90/90/0/0]s
load posision should be -4 ~ -2 and 2 ~ 4
"""

sampling_freq = 1/dt  # Hz
data_path = os.path.join(config.DATA_BASE_DIR, f'{data_filename}.csv')
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

title += ' FEM'

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
save_dir = os.path.join(config.DATA_BASE_DIR, 'results',
                        'wavelet_theory_vs_fem')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
fig.savefig(os.path.join(save_dir, f'{data_filename}.png'))
