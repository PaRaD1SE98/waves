from common.fft import MaskRange


"""General"""

# Options:
#   'plotly': Fast, interactive, has unique volume plot, but not support large datasets
#   'matplotlib': Supports large datasets, general option.
GRAPHIC_BACKEND = 'matplotlib'

# Set to False to disable output.
# Or a name for the output file common index.
PLOTLY_OUTPUT = False

# Set Matplotlib animation output
MPL_ANI_OUTPUT = False

# animation output speed (0 ~ 1)
MPL_ANI_OUTPUT_SPEED = 0.1

# Options:
#   'simulation': Use wave generator.
#   'real': Use real data from data folder.
DATA_SOURCE = 'real'

# Set fft mask shape
FFT_MASK: dict[str, MaskRange] = {
    'f_range': (230000, 250000),
    'kx_range': (-50, 150),
    'ky_range': None,
}


"""Simulation"""

# 'pulse' or 'wave' if DATA_SOURCE == 'simulation'
# This is two default examples
# Create new models in models/ folder and process them in prepare_sim.py
SIMULATION_TYPE = 'pulse'


"""Real Data"""

# Path to data folder
DATA_BASE_DIR = 'data/chen'

# Down sampling
# matplotlib 3d mask plot might need this
DOWN_SAMPLING = False

# Downsampling ratio (0 ~ 1)
DOWN_SAMPLING_RATIO = 0.33
