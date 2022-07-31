import numpy as np


class FFT:
    """
    Construct the FFT results matrix with useful dimension parameters and sampling properties
    """

    def __init__(self, data):
        self.FREQ = np.arange(0, data.sample_props.sft, data.sample_props.sft / data.sample_props.sp[0])
        self.KX = np.arange(-data.sample_props.sfx / 2, data.sample_props.sfx / 2, data.sample_props.sfx / data.sample_props.sp[1])
        self.KY = np.arange(-data.sample_props.sfy / 2, data.sample_props.sfy / 2, data.sample_props.sfy / data.sample_props.sp[2])
        self.smpl_props = data.sample_props
        self.fft_result = np.fft.fftn(data.z)
        self.abs_fft = np.abs(self.fft_result)
        self.shifted_fft = np.fft.fftshift(self.fft_result, axes=(0, 1))
        self.shifted_abs_fft = np.fft.fftshift(self.abs_fft, axes=(0, 1))


class Mask:
    """
    Construct a filter mask for the FFT results
    """

    def __init__(self, smpl_props, f_range=None, kx_range=None, ky_range=None):
        self.smpl_props = smpl_props
        if f_range is None:
            self.f_range = (0, self.smpl_props.sft / 2)
        else:
            assert f_range[0] < f_range[1], f'{f_range[0]},{f_range[1]}'
            assert f_range[1] < smpl_props.sft / 2, f'{f_range[1]},{smpl_props.sft / 2}'
            self.f_range = f_range
        if kx_range is None:
            self.kx_range = (-self.smpl_props.sfx / 2, self.smpl_props.sfx / 2)
        else:
            assert kx_range[0] < kx_range[1], f'{kx_range[0]},{kx_range[1]}'
            assert kx_range[1] < smpl_props.sfx / 2, f'{kx_range[1]},{smpl_props.sfx / 2}'
            self.kx_range = kx_range

        if ky_range is None:
            self.ky_range = (-self.smpl_props.sfy / 2, self.smpl_props.sfy / 2)
        else:
            assert ky_range[0] < ky_range[1], f'{ky_range[0]},{ky_range[1]}'
            assert ky_range[1] < smpl_props.sfy / 2, f'{ky_range[1]},{smpl_props.sfy / 2}'
            self.ky_range = ky_range

    def f_val_to_idx(self, v):
        return int(round(v * self.smpl_props.t_max))

    def kx_val_to_idx(self, v):
        return int(round((v + self.smpl_props.sfx / 2) * self.smpl_props.x_max))

    def ky_val_to_idx(self, v):
        return int(round((v + self.smpl_props.sfy / 2) * self.smpl_props.y_max))

    def __call__(self):
        # data points inside the frequency range set to 1
        mask_f = np.zeros((self.smpl_props.sp[1], self.smpl_props.sp[2], self.smpl_props.sp[0]))
        mask_f[
            :,
            :,
            self.f_val_to_idx(self.f_range[0]):self.f_val_to_idx(self.f_range[1])
        ] = 1

        # for kx and ky, filter mirror part together
        mask_k = np.zeros((self.smpl_props.sp[1], self.smpl_props.sp[2], self.smpl_props.sp[0]))
        # higher limit
        # lower than higher limit set to 1
        mask_k[
            self.kx_val_to_idx(-self.kx_range[1]):self.kx_val_to_idx(self.kx_range[1]),
            self.ky_val_to_idx(-self.ky_range[1]):self.ky_val_to_idx(self.ky_range[1]),
            :
        ] = 1
        # lower limit
        # lower than lower limit set to 0
        mask_k[
            self.kx_val_to_idx(-self.kx_range[0]):self.kx_val_to_idx(self.kx_range[0]),
            self.ky_val_to_idx(-self.ky_range[0]):self.ky_val_to_idx(self.ky_range[0]),
            :
        ] = 0
        # multipy the two mask to get the cross-section
        return mask_f * mask_k
