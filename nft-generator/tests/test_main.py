""" Unit tests to assert appropriate behavior and results of top level functions """
from os import read

from src import read_yaml_config

import pytest


@pytest.fixture
def read_yaml_config_func():
    """ Set function as testing fixture to be reused below """
    return read_yaml_config

@pytest.fixture
def test_config_file():
    return 'nft-generator/tests/fixtures/config.yaml'

def test_read_yaml_config_func_requires_string(read_yaml_config_func):
    """ Assert function raises a TypeError upon not receiving a string as argument """
    not_strings = [1, [], {'hello': 'goodbye'}, 1.23]
    for bad_arg in not_strings:
        with pytest.raises(TypeError):
            read_yaml_config_func(bad_arg)

def test_read_yaml_config_func_returns_dict(read_yaml_config_func, test_config_file):
    """ Assert function returns a dictionary in successful conditions """
    return_data = read_yaml_config_func(test_config_file)
    assert isinstance(return_data, dict)
