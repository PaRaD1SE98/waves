import re
from matplotlib.animation import FuncAnimation
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


class CScanConfig:
    """
    Read scan configuration from cmt-scan.txt file.
    """

    def __init__(self, filename):
        self.filename = filename
        self.__dict__ = self.read()

    def read(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            Nx = int(re.search(r'(?<=Nx=)\d+', lines[0]).group())
            Ny = int(re.search(r'(?<=Ny=)\d+', lines[0]).group())
            # match int or float after 'dx=\s' and 'dy=\s' in the second line
            dx = float(re.search(r'(?<=dx=\s)\d+\.?\d*', lines[1]).group())
            dy = float(re.search(r'(?<=dy=\s)\d+\.?\d*', lines[1]).group())
            # match int after 'LaserFREQ=' in the 5th line
            laser_freq = int(
                re.search(r'(?<=LaserFREQ=)\d+', lines[5]).group())
            # match int after 'A/D Data length\s=' in the 8th line
            data_length = int(
                re.search(r'(?<=A/D Data length =)\d+', lines[7]).group())
            # match int after 'Sample Rate =\s' in the 8th line
            sample_rate = int(
                re.search(r'(?<=Sample Rate =\s)\d+', lines[7]).group())
            return {'Nx': Nx,
                    'Ny': Ny,
                    'dx': dx,
                    'dy': dy,
                    'laser_freq': laser_freq,
                    'data_length': data_length,
                    'sample_rate': sample_rate}


class PauseAnimation:
    """
    Matplotlib animation with pause feature
    Press 'space' or 'enter' to pause or resume the animation
    """

    def __init__(self, fig, *args, **kwargs):
        self.animation = FuncAnimation(fig, *args, **kwargs)
        self.paused = False

        fig.canvas.mpl_connect('key_press_event', self.toggle_pause)

    def toggle_pause(self, event):
        if event.key in ('enter', ' '):
            if self.paused:
                self.animation.resume()
            else:
                self.animation.pause()
            self.paused = not self.paused
