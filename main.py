"""
1. Put data in a folder in the same directory as this file if doing real data analysis.
    The data folder should contain the following files:
        wave.dat
        cmt-scan.txt
2. Set necessary parameters in config.py
3. Choose plots to be shown here
    Word Shortcuts:
        prefix:
            od: original data
            fd: filtered data
            of: original fft
            ff: filtered fft
            m: mask
        followed by:
            2d: 2d plot
            3d: 3d plot
            xyf: kx-ky/freq slider
            xfy: kx-freq/ky slider
            yfx: ky-freq/kx slider
"""
from plot_functions import *

if __name__ == '__main__':
    volume_plot()
