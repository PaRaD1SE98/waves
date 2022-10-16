from copy import copy
from typing import Optional

import numpy as np

from common.utils import to_idx


class FFT:
    """
    Construct the FFT results matrix with useful dimension parameters and sampling properties
    """

    def __init__(self, data):
        self.FREQ = np.linspace(
            0, data.sample_props.sft, data.sample_props.spt)
        self.KX = np.linspace(-data.sample_props.sfx / 2,
                              data.sample_props.sfx / 2, data.sample_props.spx)
        self.KY = np.linspace(-data.sample_props.sfy / 2,
                              data.sample_props.sfy / 2, data.sample_props.spy)
        self.smpl_props = data.sample_props
        self.fft_result = np.fft.fftn(data.z)
        self.abs_fft = np.abs(self.fft_result)
        self.shifted_fft = np.fft.fftshift(self.fft_result, axes=(0, 1))
        self.shifted_abs_fft = np.fft.fftshift(self.abs_fft, axes=(0, 1))


class Mask:
    """
    Construct a filter mask for the FFT results
    """

    def __init__(self,
                 fft,
                 f_range: Optional[tuple[int | float, int | float]] = None,
                 kx_range: Optional[tuple[int | float, int | float]] = None,
                 ky_range: Optional[tuple[int | float, int | float]] = None):
        self.fft = fft
        if f_range is None:
            self.f_range = (0, self.fft.smpl_props.sft / 2)
        else:
            assert f_range[0] < f_range[1], f'{f_range[0]},{f_range[1]}'
            assert f_range[1] < self.fft.smpl_props.sft / \
                2, f'{f_range[1]},{self.fft.smpl_props.sft / 2}'
            self.f_range = f_range
        if kx_range is None:
            self.kx_range = (-self.fft.smpl_props.sfx / 2,
                             self.fft.smpl_props.sfx / 2)
        else:
            assert kx_range[0] < kx_range[1], f'{kx_range[0]},{kx_range[1]}'
            assert kx_range[1] < self.fft.smpl_props.sfx / \
                2, f'{kx_range[1]},{self.fft.smpl_props.sfx / 2}'
            self.kx_range = kx_range

        if ky_range is None:
            self.ky_range = (-self.fft.smpl_props.sfy / 2,
                             self.fft.smpl_props.sfy / 2)
        else:
            assert ky_range[0] < ky_range[1], f'{ky_range[0]},{ky_range[1]}'
            assert ky_range[1] < self.fft.smpl_props.sfy / \
                2, f'{ky_range[1]},{self.fft.smpl_props.sfy / 2}'
            self.ky_range = ky_range

    def __call__(self):
        # data points inside the frequency range set to 1
        mask_f = np.zeros(
            (self.fft.smpl_props.spx, self.fft.smpl_props.spy, self.fft.smpl_props.spt))
        mask_k = copy(mask_f)
        mask_f[
            :,
            :,
            to_idx(self.fft.FREQ, self.f_range[0]):to_idx(self.fft.FREQ, self.f_range[1])
        ] = 1

        # for kx and ky, filter mirror part together
        # higher limit
        # lower than higher limit set to 1
        mask_k[
            to_idx(self.fft.KX, -self.kx_range[1]):to_idx(self.fft.KX, self.kx_range[1]),
            to_idx(self.fft.KY, -self.ky_range[1]):to_idx(self.fft.KY, self.ky_range[1]),
            :
        ] = 1
        # lower limit
        # lower than lower limit set to 0
        mask_k[
            to_idx(self.fft.KX, -self.kx_range[0]):to_idx(self.fft.KX, self.kx_range[0]),
            to_idx(self.fft.KY, -self.ky_range[0]):to_idx(self.fft.KY, self.ky_range[0]),
            :
        ] = 0
        # multipy the two mask to get the cross-section
        return mask_f * mask_k
