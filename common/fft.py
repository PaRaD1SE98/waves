import numpy as np


class FFT:
    def __init__(self, smpl_props):
        self.FREQ = np.arange(0, smpl_props.sft, smpl_props.sft / smpl_props.sp)
        self.KX = np.arange(-smpl_props.sfx / 2, smpl_props.sfx / 2, smpl_props.sfx / smpl_props.sp)
        self.KY = np.arange(-smpl_props.sfy / 2, smpl_props.sfy / 2, smpl_props.sfy / smpl_props.sp)

    def __call__(self, z):
        fft_result = np.fft.fftn(z)
        abs_fft = np.abs(fft_result)
        shifted_fft = np.fft.fftshift(fft_result, axes=(0, 1))
        shifted_abs_fft = np.fft.fftshift(abs_fft, axes=(0, 1))
        return fft_result, abs_fft, shifted_fft, shifted_abs_fft


class Mask:
    def __init__(self, smpl_props, f_range=None, kx_range=None, ky_range=None):
        self.smpl_props = smpl_props
        self.f_range = f_range if f_range is not None else (0, self.smpl_props.sft / 2)
        self.kx_range = kx_range if kx_range is not None else (-self.smpl_props.sfx / 2, self.smpl_props.sfx / 2)
        self.ky_range = ky_range if kx_range is not None else (-self.smpl_props.sfy / 2, self.smpl_props.sfy / 2)
        assert f_range[0] < f_range[1]
        assert kx_range[0] < kx_range[1]
        assert ky_range[0] < ky_range[1]

    def f_val_to_idx(self, v):
        return int(round(v * self.smpl_props.t_max))

    def kx_val_to_idx(self, v):
        return int(round((v + self.smpl_props.sfx / 2) * self.smpl_props.x_max))

    def ky_val_to_idx(self, v):
        return int(round((v + self.smpl_props.sfy / 2) * self.smpl_props.y_max))

    def __call__(self):
        mask = np.zeros((self.smpl_props.sp, self.smpl_props.sp, self.smpl_props.sp))
        # higher limit
        # lower than higher limit set to 1
        mask[
        self.kx_val_to_idx(-self.kx_range[1]):self.kx_val_to_idx(self.kx_range[1]),
        self.ky_val_to_idx(-self.ky_range[1]):self.ky_val_to_idx(self.ky_range[1]),
        self.f_val_to_idx(self.f_range[0]):self.f_val_to_idx(self.f_range[1])
        ] = 1
        # lower limit
        # lower than lower limit set to 0
        mask[
        self.kx_val_to_idx(-self.kx_range[0]):self.kx_val_to_idx(self.kx_range[0]),
        self.ky_val_to_idx(-self.ky_range[0]):self.ky_val_to_idx(self.ky_range[0]),
        self.f_val_to_idx(0):self.f_val_to_idx(self.f_range[0])
        ] = 0
        return mask
