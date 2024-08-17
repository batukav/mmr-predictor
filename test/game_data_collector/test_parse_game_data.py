import sys
import os
import json
import pytest
from pytest_mock import mocker
from game_data_collector.parse_game_data import get_match_by_id, validate_clean_match_data
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import game_data_collector

# Mock OpenDota API response

def api_get_valid_match():
    with open(os.path.join("resources", "test", "parse_game_data", "valid_match.json"), "r") as fi:
        return json.load(fi)

def api_get_invalid_match():
    with open(os.path.join("resources", "test", "parse_game_data", "invalid_match.json"), "r") as fi:
        return json.load(fi)
    
# def api_get_incomplete_match(): # TODO implement
#     with open(os.path.join("resources", "test", "parse_game_data", "incomplete_match.json"), "r") as fi:
#         return json.load(fi)


# Tests

def test_validate_clean_match_data_invalid(mocker):
    # mock get_match_by_id response
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = api_get_invalid_match()
    type(mock_response).status_code = mocker.PropertyMock(return_value=200) # manually add status_code attribute

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response)
    
    # Test
    match_res = get_match_by_id(1) # TODO test method in _utils test class with status 429 etc
    
    assert type(match_res) is dict
    
    with pytest.raises(ValueError): # TODO test individual match validation criterias
        validate_clean_match_data(match_res)
