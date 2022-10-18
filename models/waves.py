import numpy as np

from common.utils import WaveFactory


class Wave(WaveFactory):
    """
    Periodic waves superposed on each other.
    """
    center = .5, .5  # x, y
    frequency = 5, 10, 15, 20  # Hz
    wave_number_x = 2, 3, 4, 5  # 1/m
    wave_number_y = 1, 3, 5, 7  # 1/m

    def wave_func(self):
        w = np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[0] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[0] * (self.y - self.center[1])) ** 2) - 2 * np.pi *
            self.frequency[0] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[1] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[1] * (self.y - self.center[1])) ** 2) - 2 * np.pi *
            self.frequency[1] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[2] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[2] * (self.y - self.center[1])) ** 2) - 2 * np.pi *
            self.frequency[2] * self.t)
        w += np.sin(
            np.sqrt((2 * np.pi * self.wave_number_x[3] * (self.x - self.center[0])) ** 2 + (
                    2 * np.pi * self.wave_number_y[3] * (self.y - self.center[1])) ** 2) - 2 * np.pi *
            self.frequency[3] * self.t)
        return w / 4

