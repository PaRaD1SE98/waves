class SamplingProperties:
    def __init__(self,
                 sp,
                 t_max=None,
                 x_max=None,
                 y_max=None):
        """
        set sampling parameters

        :param sp: sampling points in 1d
        :param t_max: max time in s
        :param x_max: max x distance in m
        :param y_max: max y distance in m
        """
        self.sp = sp
        self.t_max = t_max
        self.x_max = x_max
        self.y_max = y_max
        self.dt = self.t_max / self.sp[0]  # sampling interval (s)
        self.dx = self.x_max / self.sp[1]  # sampling interval (m)
        self.dy = self.y_max / self.sp[2]  # sampling interval (m)
        self.sft = self.sp[0] / self.t_max  # sampling temporal frequency (sampling points in 1s) t
        self.sfx = self.sp[1] / self.x_max  # sampling spatial frequency (sampling points in 1m) x
        self.sfy = self.sp[2] / self.y_max  # sampling spatial frequency (sampling points in 1m) y
        print('sampling temporal frequency (sampling points in 1s) t', self.sft, 'Hz')
        print('sampling spatial frequency (sampling points in 1m) x', self.sfx, '1/m')
        print('sampling spatial frequency (sampling points in 1m) y', self.sfy, '1/m')
