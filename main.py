"""
1. Put data folder inside data/ directory if doing real data analysis.
    The data folder should contain the following files:
        wave.dat
        cmt-scan.txt
2. Set necessary parameters in config.py
3. Choose plots to be shown here
    Word Shortcuts:
        prefix:
            of: original fft
            ff: filtered fft
        followed by:
            3d: 3d plot
            xyf: kx-ky/freq slider
            xfy: kx-freq/ky slider
            yfx: ky-freq/kx slider
        prefix:
            m: mask
            mf: mask with FFT data
        followed by:
            3d: 3d plot
        prefix:
            od: original data
            fd: filtered data
        followed by:
            2d: 2d plot
"""
from plot_functions import *

if __name__ == '__main__':
    of3d()
