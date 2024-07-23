import json
import parse_game_data_utils as pgdu
import time
import argparse
import os

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
    assert data.status_code == 200, f'Error getting parsed match data: {data.status_code}'
    match_ids = [i['match_id'] for i in data.json()]
    
    intersecting_games = set(match_ids).intersection(set(parsed_match_ids)) 
    
    if len(intersecting_games) == 0:
        print('a new set of match_ids is found. Parsing them')
        for match_id in match_ids:
            url = f"https://api.opendota.com/api/matches/{match_id}"
            match_data_response = pgdu.make_request_with_retries(url)
            assert match_data_response.status_code == 200, f'Error getting match data: {match_data.status_code}'
            match_data = match_data_response.json()
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
    
                    match_id = match_data['match_id']
                    output_file = os.path.join(output_dir, f'{match_id}.json')
                    try:
                        with open(output_file, 'w') as file:
                            print(f'Saving match data to {output_file}')
                            json.dump(match_data, file)
                    except Exception as e:
                        raise Exception(f'Some exception occurred while saving the match data: {e}')
        
        parsed_match_ids = match_ids
    
    return parsed_match_ids        
                        
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
        
    
                     
            
            
        
        