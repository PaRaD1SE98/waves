import numpy as np


def to_idx(array, value):
    return np.argmin(np.abs(array - value))


class WaveMetaclass(type):
    def __nyquist_check__(cls, smpl_props):
        assert smpl_props.sft > 2 * max(
            cls.frequency), f'Nyquist: Make sure sampling frequency(current:{smpl_props.sft}) > 2 * highest frequency of the signal(current:{2 * max(cls.frequency)})'
        assert smpl_props.sfx > 2 * max(
            cls.wave_number_x), f'Nyquist: Make sure sampling frequency(current:{smpl_props.sfx}) > 2 * highest frequency of the signal(current:{2 * max(cls.frequency)})'
        assert smpl_props.sfy > 2 * max(
            cls.wave_number_y), f'Nyquist: Make sure sampling frequency(current:{smpl_props.sfy}) > 2 * highest frequency of the signal(current:{2 * max(cls.frequency)})'

    def __call__(cls, smpl_props, *args, **kwargs):
        cls.__nyquist_check__(smpl_props)
        return super().__call__(smpl_props, *args, **kwargs)


class WaveFactory(metaclass=WaveMetaclass):
    center = (None, None)  # center coordinate (x, y)
    frequency = []  # Hz
    wave_number_x = []  # 1/m
    wave_number_y = []  # 1/m

    def __init__(self, smpl_props, x, y, t):
        self.smpl_props = smpl_props
        self.x = x
        self.y = y
        self.t = t

    def __call__(self):
        return self.wave_func()

    def wave_func(self):
        raise NotImplementedError()
