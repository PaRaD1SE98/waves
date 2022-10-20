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

# Matplotlib animation output speed (0 ~ 1)
MPL_ANI_OUTPUT_SPEED = 0.1

# Options:
#   'simulation': Use wave generator.
#   'real': Use real data from data folder.
DATA_SOURCE = 'real'

# Set fft filter shape
FILTER_WHITELIST: dict[str, MaskRange] = {
    'f_range': (230000, 250000),
    'kx_range': (-150, 150),
    'ky_range': (-230, -150),
}
FILTER_BLACKLIST: dict[str, MaskRange] = {
    'f_range': None,
    'kx_range': (-50, 50),
    'ky_range': (-190, -150),
}


"""Simulation"""

# 'pulse' or 'wave' if DATA_SOURCE == 'simulation'
# There is two default examples
# Create new models in 'models/' folder and process them in prepare_sim.py
SIMULATION_TYPE = 'wave'


"""Real Data"""

# Path to data folder
DATA_BASE_DIR = 'data/chen'

# Down sampling
# Matplotlib 3d mask plot might need this
DOWN_SAMPLING = False

# Downsampling ratio (0 ~ 1)
DOWN_SAMPLING_RATIO = 0.45
