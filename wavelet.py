import matplotlib.pyplot as plt
import numpy as np
import pywt

from prepare.real import data

print(data.z.shape)
sampling_freq = data.sample_props.sft
freqs = np.arange(0, sampling_freq)
print(len(freqs))
freqs = freqs[100:1750000:100]
print(len(freqs))

normed_freqs = freqs/sampling_freq

scales = pywt.frequency2scale('cmor1.5-1.0', normed_freqs)
input_data = data.z[205, data.z.shape[1]//2, :]
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
# plt.xlim(0, 1750)
# plt.ylim(0, 14e-3)

plt.show()
