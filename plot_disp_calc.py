import matplotlib.pyplot as plt
import pandas as pd


def convert_rad_mm_to_1_m(x):
    """
    convert rad/mm to 1/m
    """
    return x * 1000 / (2 * 3.141592653589793)


def convert_khz_to_hz(x):
    """
    convert kHz to Hz
    """
    return x * 1000


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

plt.plot(df_0_S['S0 Wavenumber (rad/mm)'], df_0_S['S0 f (kHz)'], '--', label='S0')
plt.plot(df_0_S['S1 Wavenumber (rad/mm)'], df_0_S['S1 f (kHz)'], '--', label='S1')
plt.plot(df_0_S['S2 Wavenumber (rad/mm)'], df_0_S['S2 f (kHz)'], '--', label='S2')
plt.plot(df_0_A['A0 Wavenumber (rad/mm)'], df_0_A['A0 f (kHz)'], label='A0')
plt.plot(df_0_A['A1 Wavenumber (rad/mm)'], df_0_A['A1 f (kHz)'], label='A1')

# plt.plot(df_0_S['S0 f (kHz)'], 1/df_0_S['S0 Energy velocity (m/ms)'], '--', label='S0')
# plt.plot(df_0_S['S1 f (kHz)'], 1/df_0_S['S1 Energy velocity (m/ms)'], '--', label='S1')
# plt.plot(df_0_S['S2 f (kHz)'], 1/df_0_S['S2 Energy velocity (m/ms)'], '--', label='S2')
# plt.plot(df_0_A['A0 f (kHz)'], 1/df_0_A['A0 Energy velocity (m/ms)'], label='A0')
# plt.plot(df_0_A['A1 f (kHz)'], 1/df_0_A['A1 Energy velocity (m/ms)'], label='A1')
plt.legend()
plt.xlabel('Kx(1/m)')
# plt.ylabel('Time')
plt.ylabel('Freq(Hz)')
plt.title(title)
# plt.xlim(0, 500)
# plt.ylim(0, 1.2e6)
plt.show()
