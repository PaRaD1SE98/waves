import string

template = string.Template("""Nx=$Nx , Ny=$Ny , N=$N
dx= ${dx}mm , dy= ${dy}mm 
X-intvl=58 Y-intvl=268
X0=-8122 Y0=-8292
R to Target  = 0.335m
LaserFREQ=50Hz  
Start=21:52:05 End=21:52:45 2023/06/28
Photo-Nx=59089 Photo-Ny=44500
JpgX0=1290JpgY0=1162
Pixcel-X=2592 Pixcel-Y=1944
AVE=2 CONT=1 Ymirror=+
ScanPattern=2
A/D device=5122 store bit=16 LaserName=ULTRA
A/D Data length =$data_length, Sample Rate = $sr, Vertical Range (Volt)p-p = 20.000""")


def gen_cfg(dx, dy, dt, num_points_t):
    """
    generate c_scan config file
    
    Parameters
    ----------
    dx : float
        x interval between two points in mm
    dy : float
        y interval between two points in mm
    dt : float
        time interval between two points in s
    num_points_t : int
        number of points in time direction
    """
    sample_rate = 1/dt
    return template.substitute(Nx=1,
                               Ny=1,
                               N=1,
                               dx=dx,
                               dy=dy,
                               data_length=num_points_t,
                               sr=sample_rate)


if __name__ == '__main__':
    data = gen_cfg(0.1, 0.1, 1e-6, 1000)
    print(data)
