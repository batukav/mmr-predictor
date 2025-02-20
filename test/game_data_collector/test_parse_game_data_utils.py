import sys
import os
import pytest
import random
import requests

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from game_data_collector import make_request_with_retries


def test_make_request_with_retries_ok(mocker):
    # mock get_match_by_id response object
    mock_response = mocker.MagicMock(spec=requests.Response)
    type(mock_response).status_code = mocker.PropertyMock(return_value=200)

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response, max_retries=1)
    
    res = make_request_with_retries("http://foo.com")
    assert isinstance(mock_response, requests.Response)
    
def test_make_request_with_retries_force_errors(mocker):
    # mock get_match_by_id response object
    mock_response = mocker.MagicMock()
    type(mock_response).status_code = mocker.PropertyMock(return_value=random.choice([500, 502, 503, 504, 408, 409]))

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response)
    
    with pytest.raises(ConnectionError): 
        res = make_request_with_retries("http://foo.com", max_retries=1)

def test_make_request_with_retries_timeout(mocker):
    # mock get_match_by_id response object
    mock_response = mocker.MagicMock()
    type(mock_response).status_code = mocker.PropertyMock(return_value=429)

    # Override 'requests.get' to return the mock response
    mocker.patch("requests.get", return_value=mock_response)
    
    with pytest.raises(ConnectionError): 
        res = make_request_with_retries("http://foo.com", max_retries=1)
    
    
    