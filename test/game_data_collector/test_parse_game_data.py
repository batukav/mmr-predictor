import sys
import os
import pytest

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from game_data_collector.parse_game_data import get_match_by_id, validate_clean_match_data

# Tests

def test_validate_clean_match_data_valid(mocker):
    # mock get_match_by_id response object
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
    "version": 123,
    "game_mode": 22,
    "lobby_type": 7,
    "region": 3,
    "duration": 2000,
    "players": [
        {
            "leaver_status": False,
            "randomed": False,
            "firstblood_claimed": True
        }
    ]
}
    type(mock_response).status_code = mocker.PropertyMock(return_value=200) # manually add status_code attribute

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response)
    
    match_res = get_match_by_id(1234) # TODO test method in _utils test class with status 429 etc
    match = validate_clean_match_data(match_res)
    
    assert type(match) is dict
    assert "level" not in match.keys()  # test clean_match_data
    assert all(["firstblood_claimed" not in player.keys() for player in match["players"]])  # test clean_player_data

def test_validate_clean_match_data_invalid(mocker):
    # mock get_match_by_id response object
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
    "game_mode": 22,
    "lobby_type": 7,
    "region": 2, # wrong region
    "duration": 2000,
    "players": [
        {
            "leaver_status": False,
            "randomed": False
        }
    ]
}
    type(mock_response).status_code = mocker.PropertyMock(return_value=200) # manually add status_code attribute

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response)
    
    match_res = get_match_by_id(1) 
    
    assert type(match_res) is dict
    
    with pytest.raises(ValueError): 
        validate_clean_match_data(match_res)
        
def test_validate_clean_match_data_missing_attr(mocker):
    # mock get_match_by_id response object
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = { # 'region' attr is missing
    "game_mode": 22,
    "lobby_type": 7,
    "duration": 2000,
    "players": [
        {
            "leaver_status": False,
            "randomed": False
        }
    ]
}
    type(mock_response).status_code = mocker.PropertyMock(return_value=200) # manually add status_code attribute

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response)
    
    match_res = get_match_by_id(1) 
    
    assert type(match_res) is dict
    
    with pytest.raises(ValueError):
        validate_clean_match_data(match_res)

