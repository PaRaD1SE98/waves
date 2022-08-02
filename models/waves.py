import numpy as np

from common.utils import WaveFactory


class Wave(WaveFactory):
    center = .5, .5  # x, y
    frequency = 15, 20, 25, 30  # Hz
    wave_number_x = 14, 23, 25, 31  # 1/m
    wave_number_y = 14, 23, 25, 31  # 1/m

    def __call__(self):
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

