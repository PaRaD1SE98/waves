import config


def match_fem():
    """
    return a tuple of (data_dir, degree, suffix, title)
    """
    data_dir = config.DATA_BASE_DIR
    # match string in data_dir
    data_type_map = {
        '0.0.90.90.s': ('[0-0-90-90]s/', '0', '_Lamb', '[0/0/90/90]s'),
        '90.90.0.0.s': ('[0-0-90-90]s/', '90', '_Lamb', '[90/90/0/0]s'),
        '0.90.0.90.s': ('[0-90-0-90]s/', '0', '_Lamb', '[0/90/0/90]s'),
        '90.0.90.0.s': ('[0-90-0-90]s/', '90', '_Lamb', '[90/0/90/0]s'),
    }
    # find if one of the data_types is in data_dir
    for data_type in data_type_map.keys():
        if data_type in data_dir:
            return data_type_map[data_type]


def match_exp():
    """
    return a tuple of (data_dir, degree, suffix, title)
    """
    data_dir = config.DATA_BASE_DIR
    # match string in data_dir
    data_type_map = {
        '0.0.90.90.s-0': ('[0-0-90-90]s/', '0', '_Lamb', '[0/0/90/90]s'),
        '0.0.90.90.s-90': ('[0-0-90-90]s/', '90', '_Lamb', '[90/90/0/0]s'),
        '0.90.0.90.s-0': ('[0-90-0-90]s/', '0', '_Lamb', '[0/90/0/90]s'),
        '0.90.0.90.s-90': ('[0-90-0-90]s/', '90', '_Lamb', '[90/0/90/0]s'),
    }
    # find if one of the data_types is in data_dir
    for data_type in data_type_map.keys():
        if data_type in data_dir:
            return data_type_map[data_type]