#%%
import requests
import json
import parse_game_data.parse_game_data_utils as pgdu
import time
import argparse

OUTPUT_FILE_PATH = '/Users/peptid/Local_Documents/mmr_predictor/parsed_games.json'
WAIT_TIME = 120

def parse_game_data(parsed_match_ids):
    
    """
    Following are used to limit the games:
    game_mode = 22 all_pick
    lobby_type = 7 ranked
    region = 3 EUROPE
    player leaver_status = 1 -> don't parse the game
    duration < 60 * 25 -> don't parse, possibly a stomp
    if any player data['players']{}['randomed'] -> don't parse
    """
    
    url = "https://api.opendota.com/api/parsedMatches/"
    # without query value, parsedMatches seem to return the last parsed 100 games
    data = pgdu.make_request_with_retries(url)
    assert data.response == 200, f'Error getting parsed match data: {data.response}'
    match_ids = [i['match_id'] for i in data]
    
    intersecting_games = set(match_ids).intersection(set(parsed_match_ids)) 
    
    if len(intersecting_games) == 0:
        print('a new set of match_ids is found. Parsing them')
        for match_id in match_ids:
            url = f"https://api.opendota.com/api/matches/{match_id}"
            match_data = pgdu.make_request_with_retries(url)
            assert match_data.response == 200, f'Error getting match data: {match_data.response}'
            break_loop = False
            if match_data['game_mode'] == 22 and match_data['lobby_type'] == 7 and match_data['region'] == 3 and match_data['duration'] > 60 * 25:
                match_data = pgdu.clean_match_data(match_data)
                for player in match_data['players']:
                    if player['leaver_status'] == 1 or player['randomed'] == 1:
                        break_loop = True
                if break_loop == True:
                    continue
                else:
                    for id, player in enumerate(match_data['players']):
                        match_data['players'][id] = pgdu.clean_player_data(player)
    
                    # Read the existing data from the JSON file
                    try:
                        with open(OUTPUT_FILE_PATH, 'r') as file:
                            data = json.load(file)
                    except FileNotFoundError:
                        data = []

                    # Append the new dictionary to the existing data
                    if isinstance(data, list):
                        data.append(match_data)
                    elif isinstance(data, dict):
                        data.update(match_data)

                    # Write the updated data back to the JSON file
                    with open(OUTPUT_FILE_PATH, 'w') as file:
                        json.dump(data, file, indent=4)

                    print("Data appended successfully.")
        
        parsed_match_ids = match_ids
    
    return parsed_match_ids        
                        
if __name__  == '__main__':
    
    parsed_match_ids = []
    try:
        with open(OUTPUT_FILE_PATH, 'r') as file:
            processed_match_data = json.load(file)
            for i in processed_match_data:
                parsed_match_ids.append(i['match_id'])         
    except FileNotFoundError:
        print('Seems like a fresh run, setting the parsed_match_ids to empty')
        pass
    
    print(f'Total number of parsed games is {len(parsed_match_ids)}')
    while True:
        new_parsed_match_ids = parse_game_data(parsed_match_ids)
        if new_parsed_match_ids == parsed_match_ids:
            print('Some game ids are overlapping. Waiting for new games to be parsed')
            time.sleep(WAIT_TIME)
        
    
                     
            
            
        
        