from common.fft import MaskRange


"""General"""

# Options:
#   'plotly': Fast, interactive, has unique volume plot, but not support large datasets
#   'matplotlib': Supports large datasets, general option.
GRAPHIC_BACKEND = 'matplotlib'

# Set to False to disable output.
# Or a name for the output file common index.
PLOTLY_OUTPUT = False

# Options:
#   'simulation': Use wave generator.
#   'real': Use real data from data folder.
DATA_SOURCE = 'real'


"""Simulation"""

# 'pulse' or 'wave' if DATA_SOURCE == 'simulation'
# This is two default examples
# Create new models in models/ folder and process them in prepare_sim.py
SIMULATION_TYPE = 'pulse'


"""Real Data"""

# Path to data folder
DATA_BASE_DIR = 'data/chen'

# Downsampling ratio for plotly beckend
DOWN_SAMPLING_RATIO = 3

# Set fft mask shape
FFT_MASK: dict[str, MaskRange] = {
    'f_range': None,
    'kx_range': None,
    'ky_range': None,
}
