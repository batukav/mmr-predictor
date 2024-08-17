import sys
import os
import json
import pytest

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
    
# def api_get_incomplete_match():
#     with open(os.path.join("resources", "test", "parse_game_data", "incomplete_match.json"), "r") as fi:
#         return json.load(fi)


# Tests

def test_foo():
    assert True