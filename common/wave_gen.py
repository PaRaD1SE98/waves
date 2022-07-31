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
    class Data:
        T = np.arange(0, smpl_props.t_max, smpl_props.dt)
        X = np.arange(0, smpl_props.x_max, smpl_props.dx)
        Y = np.arange(0, smpl_props.y_max, smpl_props.dy)
        x, y = np.meshgrid(X, Y, indexing='ij')
        z = z_array
        sample_props = smpl_props

        print('constructed signal shape', z.shape)

    return Data
