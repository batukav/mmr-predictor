import json
import parse_game_data_utils as pgdu
import os

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s [%(levelname)s]: %(message)s', datefmt='%H:%M')

class RequestCoundHandler:
    total_requests = 0

def get_latest_match_ids(limit: int = 2000) ->list[int]:
    url = "https://api.opendota.com/api/explorer?sql="
    sql = f"SELECT match_id FROM matches ORDER BY match_id DESC LIMIT {limit} ;"
    
    res = json.loads(pgdu.make_request_with_retries(url + sql).text)
    
    match_ids = [row["match_id"] for row in res["rows"]]
    
    logger.info(f"Successfully requested {len(match_ids)} latest match_ids")
    
    return match_ids

def parse_game_data(parsed_match_ids: list[int], output_dir: str) -> None:
    
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
            assert match_data_response.status_code == 200, f'Error getting match data: {match_data_response.status_code}'
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
                        with open(output_file, 'w', encoding='utf8') as file:
                            print(f'Saving match data to {output_file}')
                            json.dump(match_data, file, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
                    except Exception as e:
                        raise Exception(f'Some exception occurred while saving the match data: {e}')
        
        parsed_match_ids = match_ids
    
    return parsed_match_ids   

if __name__  == '__main__':
    get_latest_match_ids()     
        
    
                     
            
            
        
        