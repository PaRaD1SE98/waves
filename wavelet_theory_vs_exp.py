import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt

from prepare.real import data

print(data.z.shape)
sampling_freq = data.sample_props.sft
freqs = np.arange(0, sampling_freq)
# print(freqs)
print(len(freqs))
freqs = freqs[100:1750000:100]
# print(freqs)
print(len(freqs))

normed_freqs = freqs/sampling_freq
# print(normed_freqs)
index = 205
scales = pywt.frequency2scale('cmor1.5-1.0', normed_freqs)
input_data = data.z[index, data.z.shape[1]//2, :]
sig_length = input_data.shape[0]
sampling_period = data.sample_props.dt
t = sampling_period * sig_length
time = np.linspace(0, t, sig_length) * 1e3 # in ms
cwtmatr, freqs = pywt.cwt(input_data, scales, 'cmor1.5-1.0', sampling_period)
freqs = freqs * 1e-3 # in kHz
X, Y = np.meshgrid(freqs, time)
# plt.plot(input_data)
plt.contourf(X, Y, np.abs(cwtmatr).T, cmap='viridis', levels=20)
plt.xlabel('Frequency (kHz)')
plt.ylabel('Time (ms)')
plt.tight_layout()

base_dir = 'data/li/disp_calc/'

data_dir = '[0-0-90-90]s/'

degree = '90'

title = data_dir+degree

if degree not in ['0', '90']:
    suffix = ''
else:
    suffix = '_Lamb'

df_0_S = pd.read_csv(base_dir+data_dir+degree+f'_S{suffix}.txt')
df_0_A = pd.read_csv(base_dir+data_dir+degree+f'_A{suffix}.txt')

distance_to_pzt = 0.015 + index*data.sample_props.dx
x_multiplyer = 1
y_multiplyer = 1
plt.plot(df_0_S['S0 f (kHz)']*x_multiplyer, distance_to_pzt/df_0_S['S0 Energy velocity (m/ms)']*y_multiplyer, '--', label='S0')
# plt.plot(df_0_S['S1 f (kHz)']*multiplier, distance_to_pzt/df_0_S['S1 Energy velocity (m/ms)']*y_multiplyer, '--', label='S1')
# plt.plot(df_0_S['S2 f (kHz)']*multiplier, distance_to_pzt/df_0_S['S2 Energy velocity (m/ms)']*y_multiplyer, '--', label='S2')
plt.plot(df_0_A['A0 f (kHz)']*x_multiplyer, distance_to_pzt/df_0_A['A0 Energy velocity (m/ms)']*y_multiplyer, label='A0')
plt.plot(df_0_A['A1 f (kHz)']*x_multiplyer, distance_to_pzt/df_0_A['A1 Energy velocity (m/ms)']*y_multiplyer, label='A1')
plt.legend()
plt.xlabel('Freq(kHz)')
plt.ylabel('Arrival Time(ms)')
plt.title(title)
plt.xlim(0, 1750)
# plt.ylim(0, 14e-3)
plt.show()
