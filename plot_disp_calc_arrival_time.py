import matplotlib.pyplot as plt
import pandas as pd


base_dir = 'data/li/disp_calc/'

data_dir = '[0-0-90-90]s/'

degree = '0'

if degree == '0':
    title = '[0-0-90-90]s'
elif degree == '90':
    title = '[90-90-0-0]s'

if degree not in ['0', '90']:
    suffix = ''
else:
    suffix = '_Lamb'

df_0_S = pd.read_csv(base_dir+data_dir+degree+f'_S{suffix}.txt')
df_0_A = pd.read_csv(base_dir+data_dir+degree+f'_A{suffix}.txt')

distance_to_pzt = 0.15 # m
kHz_to_MHz = 1e-3
m_ms_to_m_us = 1e3
x_multiplyer = 1
y_multiplyer = 1
plt.plot(df_0_S['S0 f (kHz)']*x_multiplyer, distance_to_pzt/df_0_S['S0 Energy velocity (m/ms)']*y_multiplyer, '--', label='S0')
# plt.plot(df_0_S['S1 f (kHz)']*multiplier, distance_to_pzt/df_0_S['S1 Energy velocity (m/ms)']*y_multiplyer, '--', label='S1')
# plt.plot(df_0_S['S2 f (kHz)']*multiplier, distance_to_pzt/df_0_S['S2 Energy velocity (m/ms)']*y_multiplyer, '--', label='S2')
plt.plot(df_0_A['A0 f (kHz)']*x_multiplyer, distance_to_pzt/df_0_A['A0 Energy velocity (m/ms)']*y_multiplyer, label='A0')
plt.plot(df_0_A['A1 f (kHz)']*x_multiplyer, distance_to_pzt/df_0_A['A1 Energy velocity (m/ms)']*y_multiplyer, label='A1')
plt.legend()
plt.ylabel('Arrival Time(ms)')
plt.xlabel('Freq(kHz)')
plt.title(title)
plt.xlim(0, 1500)
plt.ylim(0, 0.15)
plt.show()
