import time
import argparse

from parse_game_data import parse_game_data

WAIT_TIME = 120

if __name__  == '__main__':
    
    parser = argparse.ArgumentParser(description="Parsing arguments to fetch, process, and save game data")
    parser.add_argument('--output_dir', type = str, required=True, help= "Path to the output root directory. Each game data will be saved to this directory separately as {match_id}.json")
    args = parser.parse_args()
    output_dir = args.output_dir
    
    parsed_match_ids = []

    while True:
        new_parsed_match_ids = parse_game_data(parsed_match_ids)
        if new_parsed_match_ids == parsed_match_ids:
            print('Some game ids are overlapping. Waiting for new games to be parsed')
            time.sleep(WAIT_TIME)