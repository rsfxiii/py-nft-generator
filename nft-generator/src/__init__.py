import yaml


def read_yaml_config(filepath: str) -> dict:
    """
    :param filepath str - Filename of .yaml or .yml config file
    :returns config dict - Dictionary data from the config
    """
    if not isinstance(filepath, str):
        raise TypeError('String argument is required: filepath')

    config_data = None
    with open (filepath, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data