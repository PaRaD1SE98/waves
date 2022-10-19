from copy import copy
from typing import Optional

import numpy as np
import scipy

from common.utils import to_idx


class FFT:
    """
    Construct the FFT results matrix with useful dimension parameters and sampling properties
    """

    def __init__(self, data):
        self.FREQ = np.linspace(0, data.sample_props.sft,
                                data.sample_props.spt)
        self.KX = np.linspace(0, data.sample_props.sfx,
                              data.sample_props.spx)
        self.KY = np.linspace(0, data.sample_props.sfy,
                              data.sample_props.spy)
        # bug: cannot use fftshift on class instance variable
        self.shifted_FREQ = scipy.fft.fftshift(
            scipy.fft.fftfreq(data.sample_props.spt, data.sample_props.dt))
        self.shifted_KX = scipy.fft.fftshift(scipy.fft.fftfreq(
            data.sample_props.spx, data.sample_props.dx))
        self.shifted_KY = scipy.fft.fftshift(scipy.fft.fftfreq(
            data.sample_props.spy, data.sample_props.dy))
        self.smpl_props = data.sample_props
        self.fft_result = scipy.fft.fftn(data.z)
        self.abs_fft = np.abs(self.fft_result)
        self.shifted_fft = scipy.fft.fftshift(self.fft_result, axes=(0, 1))
        self.shifted_abs_fft = scipy.fft.fftshift(self.abs_fft, axes=(0, 1))


MaskRange = Optional[tuple[float, float]]


class BaseBlackList:
    """
    Base class for blacklist filters
    """

    def __init__(self,
                 fft,
                 f_range: MaskRange = None,
                 kx_range: MaskRange = None,
                 ky_range: MaskRange = None):
        self.fft = fft
        if f_range is None:
            self.f_range = (self.fft.FREQ[0], self.fft.FREQ[-1] / 2)
        else:
            assert f_range[0] < f_range[1], f'{f_range[0]},{f_range[1]}'
            assert f_range[1] < self.fft.smpl_props.sft / \
                2, f'{f_range[1]},{self.fft.smpl_props.sft / 2}'
            self.f_range = f_range
        if kx_range is None:
            self.kx_range = (self.fft.shifted_KX[0],
                             self.fft.shifted_KX[-1])
        else:
            assert kx_range[0] < kx_range[1], f'{kx_range[0]},{kx_range[1]}'
            assert kx_range[1] < self.fft.smpl_props.sfx / \
                2, f'{kx_range[1]},{self.fft.smpl_props.sfx / 2}'
            self.kx_range = kx_range

        if ky_range is None:
            self.ky_range = (self.fft.shifted_KY[0],
                             self.fft.shifted_KY[-1])
        else:
            assert ky_range[0] < ky_range[1], f'{ky_range[0]},{ky_range[1]}'
            assert ky_range[1] < self.fft.smpl_props.sfy / \
                2, f'{ky_range[1]},{self.fft.smpl_props.sfy / 2}'
            self.ky_range = ky_range

    def __call__(self):
        raise NotImplementedError

class BaseWhiteList:
    """
    Base class for whitelist filters
    """

    def __init__(self,
                 fft,
                 f_range: MaskRange = None,
                 kx_range: MaskRange = None,
                 ky_range: MaskRange = None):
        self.fft = fft
        if f_range is None:
            self.f_range = None
        else:
            assert f_range[0] < f_range[1], f'{f_range[0]},{f_range[1]}'
            assert f_range[1] < self.fft.smpl_props.sft / \
                2, f'{f_range[1]},{self.fft.smpl_props.sft / 2}'
            self.f_range = f_range
        if kx_range is None:
            self.kx_range = None
        else:
            assert kx_range[0] < kx_range[1], f'{kx_range[0]},{kx_range[1]}'
            assert kx_range[1] < self.fft.smpl_props.sfx / \
                2, f'{kx_range[1]},{self.fft.smpl_props.sfx / 2}'
            self.kx_range = kx_range

        if ky_range is None:
            self.ky_range = None
        else:
            assert ky_range[0] < ky_range[1], f'{ky_range[0]},{ky_range[1]}'
            assert ky_range[1] < self.fft.smpl_props.sfy / \
                2, f'{ky_range[1]},{self.fft.smpl_props.sfy / 2}'
            self.ky_range = ky_range


class CubeWhiteList(BaseWhiteList):
    def __call__(self):
        # data points inside the frequency range set to 1
        mask_f = np.zeros(self.fft.shifted_abs_fft.shape)
        mask_kx = copy(mask_f)
        mask_ky = copy(mask_f)
        if self.f_range is not None:
            mask_f[
                :,
                :,
                to_idx(self.fft.FREQ, self.f_range[0]):to_idx(self.fft.FREQ, self.f_range[1])
            ] = 1
        else:
            mask_f[:, :, :] = 1
        if self.kx_range is not None:
            mask_kx[
                to_idx(self.fft.shifted_KX, self.kx_range[0]):to_idx(self.fft.shifted_KX, self.kx_range[1]),
                :,
                :
            ] = 1
        else:
            mask_kx[:, :, :] = 1
        if self.ky_range is not None:
            mask_ky[
                :,
                to_idx(self.fft.shifted_KY, self.ky_range[0]):to_idx(self.fft.shifted_KY, self.ky_range[1]),
                :
            ] = 1
        else:
            mask_ky[:, :, :] = 1
        return np.logical_and(mask_f, np.logical_and(mask_kx, mask_ky))


class CubeBlackList(BaseBlackList):
    def __call__(self):
        # data points inside the frequency range set to 1
        mask = np.ones(self.fft.shifted_abs_fft.shape)
        mask[
            to_idx(self.fft.shifted_KX, self.kx_range[0]):to_idx(self.fft.shifted_KX, self.kx_range[1]),
            to_idx(self.fft.shifted_KY, self.ky_range[0]):to_idx(self.fft.shifted_KY, self.ky_range[1]),
            to_idx(self.fft.FREQ, self.f_range[0]):to_idx(self.fft.FREQ, self.f_range[1])
        ] = 0
        return mask
