from copy import deepcopy

import numpy as np


class Wave:
    center = .5, .5  # x, y
    frequency = 15, 20, 25, 30  # Hz
    wave_number_x = 14, 23, 25, 31  # 1/m
    wave_number_y = 14, 23, 25, 31  # 1/m

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def __call__(self, *args, **kwargs):
        w = np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[0] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[0] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[0] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[1] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[1] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[1] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[2] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[2] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[2] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[3] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[3] * (self.y - self.center[1])) ** 2) + 2 * np.pi *
            self.frequency[3] * self.t)
        return w / 4


class Pulse:
    """
    y=exp(-(sqrt(x^2+y^2)-t)^2) * (sin(sqrt(x^2+y^2)-t)+cos(sqrt(x^2+y^2)-t))
    """
    center = 0, .5  # center coordinate (x, y)
    frequency = 10, 20, 30  # Hz
    wave_number_x = 10, 20, 30  # 1/m
    wave_number_y = 10, 20, 30  # 1/m

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def __call__(self, *args, **kwargs):
        p = np.exp(
            - (np.sqrt(
                (2 * np.pi * self.wave_number_x[0] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[0] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[0] * self.t) ** 2
        )
        p *= np.sin(
            np.sqrt(
                (2 * np.pi * self.wave_number_x[1] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[1] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[1] * self.t
        ) + \
             np.cos(
                 np.sqrt(
                     (2 * np.pi * self.wave_number_x[2] * (self.x - self.center[0])) ** 2 +
                     (2 * np.pi * self.wave_number_y[2] * (self.y - self.center[1])) ** 2
                 ) - 2 * np.pi * self.frequency[2] * self.t
             )
        return p / 2


def property_check(sft, sfx, sfy, signal_cls):
    """
    Nyquist check

    :param sft: sample temporal frequency
    :param sfx: sample spacial frequency x
    :param sfy: sample spacial frequency y
    :param signal_cls: the signal class
    """
    assert sft > 2 * max(
        signal_cls.frequency), f'Nyquist: Make sure sampling frequency(current:{sft}) > 2 * highest frequency of the signal(current:{2 * max(signal_cls.frequency)})'
    assert sfx > 2 * max(
        signal_cls.wave_number_x), f'Nyquist: Make sure sampling frequency(current:{sfx}) > 2 * highest frequency of the signal(current:{2 * max(signal_cls.frequency)})'
    assert sfy > 2 * max(
        signal_cls.wave_number_y), f'Nyquist: Make sure sampling frequency(current:{sfy}) > 2 * highest frequency of the signal(current:{2 * max(signal_cls.frequency)})'


def generate_data(smpl_props, signal_cls):
    class Data:
        T = np.arange(0, smpl_props.t_max, smpl_props.dt)
        X = np.arange(0, smpl_props.x_max, smpl_props.dx)
        Y = np.arange(0, smpl_props.y_max, smpl_props.dy)
        x, y = np.meshgrid(X, Y, indexing='ij')
        z = np.zeros((len(X), len(Y), len(T)))
        sample_props = smpl_props

        for i, t in enumerate(T):
            z[:, :, i] = signal_cls(x, y, t)()

        print('generated signal shape', z.shape)

    return Data


def construct_data(smpl_props, z_array):
    """
    Construct a data class with all formatted properties.

    :param smpl_props:
    :param z_array:
    :return:
    """

    class Data:
        T = np.arange(0, smpl_props.t_max, smpl_props.dt)
        X = np.arange(0, smpl_props.x_max, smpl_props.dx)
        Y = np.arange(0, smpl_props.y_max, smpl_props.dy)
        x, y = np.meshgrid(X, Y, indexing='ij')
        z = z_array
        sample_props = smpl_props

        print('constructed signal shape', z.shape)

    return Data


def down_sampling(data_cls,
                  new_expect_spt=None,
                  new_expect_spx=None,
                  new_expect_spy=None,
                  sample_interval_t=None,
                  sample_interval_x=None,
                  sample_interval_y=None):
    """
    Down sampling the data.
    This down sampling method is base on finding intervals between the original data.
    The original sampling size may not be completely divisible, so the actual sampling
    size could be different from the expected sampling size.

    :param data_cls: data class generated by generate_data or construct_data
    :param new_expect_spt: new expected sample points in t
    :param new_expect_spx: new expected sample points in x
    :param new_expect_spy: new expected sample points in y
    :param sample_interval_t: points between each new sample in t
    :param sample_interval_x: points between each new sample in x
    :param sample_interval_y: points between each new sample in y
    :return:
    """

    class Data:
        if sample_interval_t is None:
            assert new_expect_spt is not None, 'either sample_interval_t or new_expect_spt must be specified'
            rate_spt = round(data_cls.sample_props.spt / new_expect_spt)
        else:
            rate_spt = sample_interval_t
        if sample_interval_x is None:
            assert new_expect_spx is not None, 'either sample_interval_x or new_expect_spx must be specified'
            rate_spx = round(data_cls.sample_props.spx / new_expect_spx)
        else:
            rate_spx = sample_interval_x
        if sample_interval_y is None:
            assert new_expect_spy is not None, 'either sample_interval_y or new_expect_spy must be specified'
            rate_spy = round(data_cls.sample_props.spy / new_expect_spy)
        else:
            rate_spy = sample_interval_y
        z = data_cls.z[::rate_spx, ::rate_spy, ::rate_spt]
        T = np.linspace(0, data_cls.sample_props.t_max, z.shape[2])
        X = np.linspace(0, data_cls.sample_props.x_max, z.shape[0])
        Y = np.linspace(0, data_cls.sample_props.y_max, z.shape[1])
        x, y = np.meshgrid(X, Y, indexing='ij')
        sample_props = deepcopy(data_cls.sample_props)
        sample_props.sp = (z.shape[2], z.shape[0], z.shape[1])
        sample_props.spt = z.shape[2]
        sample_props.spx = z.shape[0]
        sample_props.spy = z.shape[1]
        sample_props.dt = sample_props.t_max / sample_props.spt
        sample_props.dx = sample_props.x_max / sample_props.spx
        sample_props.dy = sample_props.y_max / sample_props.spy
        sample_props.sft = sample_props.spt / sample_props.t_max
        sample_props.sfx = sample_props.spx / sample_props.x_max
        sample_props.sfy = sample_props.spy / sample_props.y_max
        print('down sampling temporal frequency (sampling points in 1s) t', sample_props.sft, 'Hz')
        print('down sampling spatial frequency (sampling points in 1m) x', sample_props.sfx, '1/m')
        print('down sampling spatial frequency (sampling points in 1m) y', sample_props.sfy, '1/m')

        print('down sampled signal shape', z.shape)

    return Data
