import numpy as np

from common.utils import WaveFactory


class Pulse(WaveFactory):
    """
    y=exp(-(sqrt(x^2+y^2)-t)^2) * (sin(sqrt(x^2+y^2)-t)+cos(sqrt(x^2+y^2)-t))
    """
    center = .5, .5  # center coordinate (x, y)
    frequency = 10, 20, 30  # Hz
    wave_number_x = 10, 20, 30  # 1/m
    wave_number_y = 10, 20, 30  # 1/m

    def wave_func(self):
        p = np.exp(
            - (np.sqrt(
                (2 * np.pi * self.wave_number_x[0] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[0] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[0] * self.t) ** 2
        )
        w = np.sin(
            np.sqrt(
                (2 * np.pi * self.wave_number_x[1] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[1] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[1] * self.t
        )
        w += np.cos(
            np.sqrt(
                (2 * np.pi * self.wave_number_x[2] * (self.x - self.center[0])) ** 2 +
                (2 * np.pi * self.wave_number_y[2] * (self.y - self.center[1])) ** 2
            ) - 2 * np.pi * self.frequency[2] * self.t
        )
        return p * w / 2
