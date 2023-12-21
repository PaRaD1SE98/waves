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
MPL_ANI_OUTPUT = True

# Matplotlib animation output speed (0 ~ 1)
MPL_ANI_OUTPUT_SPEED = 0.1

# Options:
#   'simulation': Use wave generator.
#   'real': Use real data from data folder.
#   'fem': Use fem data from data folder.
DATA_SOURCE = 'fem'

# Set fft filter shape
# modify detail filter logic in prepare/(real.py or sim.py)
FILTER_WHITELIST: dict[str, MaskRange] = {
    'f_range': (0, 4999999),
    'kx_range': (0, 1269),
    'ky_range': (-20, 20),
}
FILTER_BLACKLIST: dict[str, MaskRange] = {
    'f_range': None,
    'kx_range': (500, 1300),
    'ky_range': (-200, 200),
}


"""Simulation"""

# 'pulse' or 'wave' if DATA_SOURCE == 'simulation'
# There is two default examples
# Create new models in 'models/' folder and process them in prepare_sim.py
SIMULATION_TYPE = 'wave'


"""Real/FEM Data"""

# Path to data folder
# disp_verify
# DATA_BASE_DIR = 'data/li/disp_verify/90.90.0.0.s'
# DATA_BASE_DIR = 'data/li/disp_verify/0.0.90.90.s'
# DATA_BASE_DIR = 'data/li/disp_verify/90.0.90.0.s'
# DATA_BASE_DIR = 'data/li/disp_verify/0.90.0.90.s'
# exp
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.0.90.90.s-90'
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.0.90.90.s-0'
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.90.0.90.s-90'
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.90.0.90.s-0'
# fem
# DATA_BASE_DIR = 'data/li/2023-12-10/90.90.0.0.s'
DATA_BASE_DIR = 'data/li/2023-12-10/90.0.90.0.s'
# DATA_BASE_DIR = 'data/li/2023-12-10/0.0.90.90.s'
# DATA_BASE_DIR = 'data/li/2023-12-10/0.90.0.90.s'

# FEM output file name
# FEM_DATA_FILENAME = 'data.csv'
FEM_DATA_FILENAME = 'data-left-upper-1.5.csv' # for [0-0-90-90]s or [90-0-90-0]s
# FEM_DATA_FILENAME = 'data-left-lower-2.5.csv' # for [0-90-0-90]s
# FEM_DATA_FILENAME = 'data-left-lower-3.csv' # for [90-90-0-0]s


# Down sampling
# Matplotlib 3d mask plot might need this
DOWN_SAMPLING = False

# Downsampling ratio (0 ~ 1)
DOWN_SAMPLING_RATIO = 0.45
