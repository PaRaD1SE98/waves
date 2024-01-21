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
"""
LOADING NODES ID

middle upper 4     layer:  99050, 99049
middle upper 3.5   layer: 105053, 105052
middle upper 3     layer:  85043, 85042
middle upper 2.5   layer:  91046, 91045
middle upper 2     layer:  71036, 71035
middle upper 1.5   layer:  77039, 77038
middle upper 1     layer:  57029, 57028
middle upper 0.5   layer:  63032, 63031
middle center      layer:  43022, 43021
middle lower 0.5   layer:  49025, 49024
middle lower 1     layer:  29015, 29014
middle lower 1.5   layer:  35018, 35017
middle lower 2     layer:  15008, 15007
middle lower 2.5   layer:  21011, 21010
middle lower 3     layer:   1004, 1003
middle lower 3.5   layer:   7004, 7003
middle lower 4     layer:  13007, 13006

left upper 4   layer: 100050
left upper 3.5 layer: 106053
left upper 3   layer: 86043
left upper 2.5 layer: 92046
left upper 2   layer: 72036
left upper 1.5 layer: 78039
left upper 1   layer: 58029
left upper 0.5 layer: 64032
left center    layer: 44022
left lower 0.5 layer: 50025
left lower 1   layer: 30015
left lower 1.5 layer: 36018
left lower 2   layer: 16008
left lower 2.5 layer: 22011
left lower 3   layer:  2001
left lower 3.5 layer:  8004
left lower 4   layer: 14007

in [0/0/90/90]s
load posision should be -2 ~ 2
in [90/90/0/0]s
load posision should be -4 ~ -2 and 2 ~ 4
"""

# Path to data folder
# disp_verify
# DATA_BASE_DIR = 'data/li/disp_verify/90.90.0.0.s'
# DATA_BASE_DIR = 'data/li/disp_verify/0.0.90.90.s'
# DATA_BASE_DIR = 'data/li/disp_verify/90.0.90.0.s'
# DATA_BASE_DIR = 'data/li/disp_verify/0.90.0.90.s'
# exp
DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.0.90.90.s-90'
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.0.90.90.s-0'
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.90.0.90.s-90'
# DATA_BASE_DIR = 'data/li/2023-06-28-AE504S/0.90.0.90.s-0'
# fem
# DATA_BASE_DIR = 'data/li/2023-12-10-FEM/90.90.0.0.s'
# DATA_BASE_DIR = 'data/li/2023-12-10-FEM/90.0.90.0.s'
# DATA_BASE_DIR = 'data/li/2023-12-10-FEM/0.0.90.90.s'
# DATA_BASE_DIR = 'data/li/2023-12-10-FEM/0.90.0.90.s'

# FEM output file name
# FEM_DATA_FILENAME = 'data-left-upper-1.5.csv' # for [0-0-90-90]s or [90-0-90-0]s
# FEM_DATA_FILENAME = 'data-left-lower-2.5.csv' # for [0-90-0-90]s

# FEM_DATA_FILENAME = 'data-left-lower-3.csv' # for [90-90-0-0]s
# FEM_DATA_FILENAME = 'data-left-lower-1.csv' # for [0-0-90-90]s
FEM_DATA_FILENAME = 'data-middle-lower-1.csv' # for [0-0-90-90]s
# FEM_DATA_FILENAME = 'data-middle-lower-1-selected-only.csv'  # for [0-0-90-90]s
# FEM_DATA_FILENAME = 'data-middle-lower-3.csv'  # for [90-90-0-0]s
# FEM_DATA_FILENAME = 'data-middle-lower-3-selected-only.csv'  # for [90-90-0-0]s


# Down sampling
# Matplotlib 3d mask plot might need this
DOWN_SAMPLING = False

# Downsampling ratio (0 ~ 1)
DOWN_SAMPLING_RATIO = 0.45
