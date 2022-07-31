class SamplingProperties:
    """
    Construct useful sampling parameters from sampling points and max distance
    """

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
        self.spt = sp[0]
        self.spx = sp[1]
        self.spy = sp[2]
        self.t_max = t_max
        self.x_max = x_max
        self.y_max = y_max
        self.dt = self.t_max / self.spt  # sampling interval (s)
        self.dx = self.x_max / self.spx  # sampling interval (m)
        self.dy = self.y_max / self.spy  # sampling interval (m)
        self.sft = self.spt / self.t_max  # sampling temporal frequency (sampling points in 1s) t
        self.sfx = self.spx / self.x_max  # sampling spatial frequency (sampling points in 1m) x
        self.sfy = self.spy / self.y_max  # sampling spatial frequency (sampling points in 1m) y
        print('sampling temporal frequency (sampling points in 1s) t', self.sft, 'Hz')
        print('sampling spatial frequency (sampling points in 1m) x', self.sfx, '1/m')
        print('sampling spatial frequency (sampling points in 1m) y', self.sfy, '1/m')
