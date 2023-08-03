import numpy as np
import matplotlib.pyplot as plt
from common.utils import to_idx
from prepare.real import data, fft

# 2d plot
d = data.z
print(d.shape)
extracted = d[:, 12, :]
# plt.imshow(extracted)
# plt.xlabel('t')
# plt.ylabel('x')
# plt.show()

# 2dfft
rs = np.fft.fft2(extracted)
# rs = np.fft.fftshift(rs)
# shift x and y axis
# rs = np.roll(rs, rs.shape[0] // 2, axis=0)
# rs = np.roll(rs, rs.shape[1] // 2, axis=1)
rs = np.abs(rs)
# use pcolormesh
plot_rs = rs[:100, :400].T
# plt.pcolormesh(plot_rs)

# plt.xlabel('f') # unit: 1/s
# plt.ylabel('k') # unit: 1/m
# plt.show()
c_scale_lim=True
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
fig.colorbar(image_fft_ky, label='Amplitude')
plt.show()