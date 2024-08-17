import json
import os
import logging
from tqdm import tqdm

import game_data_collector.parse_game_data_utils as pgdu

logger = logging.getLogger(__name__)

def get_parsed_match_ids() -> list[int]:
    """Get a list of matches fro mthe /parsedMatches endpoint for further processing

    Raises:
        ValueError: When HTTP Response is other than 200 OK

    Returns:
        list[int]:List of match ids
    """    
    url = "https://api.opendota.com/api/parsedMatches/"
    # without query value, parsedMatches seem to return the last parsed 100 games
    res = pgdu.make_request_with_retries(url)
    
    if res.status_code != 200:
        raise ValueError(f'Failed to retrieve data: {res.status_code}')
    
    match_ids = [i['match_id'] for i in res.json()]
    logger.info(f"Successfully requested {len(match_ids)} match ids")
    
    return match_ids
        
def get_match_ids_by_query(limit: int = 2000) ->list[int]:
    """Get custom match IDs from the /explorer endpoint

    Args:
        limit (int, optional): Amount of ids to query. Defaults to 2000.

    Raises:
        ValueError: When HTTP Response is other than 200 OK

    Returns:
        list[int]: Returns match IDs which match the Postgres query
    """    
    url = "https://api.opendota.com/api/explorer?sql="
    sql = f"SELECT match_id FROM matches ORDER BY match_id DESC LIMIT {limit} ;" # TODO WHERE ...
    
    res = pgdu.make_request_with_retries(url + sql)
    
    if res.status_code != 200:
        raise ValueError(f'Failed to retrieve data: {res.status_code}')
    
    json_body = json.loads(res.text)
    match_ids = [row["match_id"] for row in json_body["rows"]]
    logger.info(f"Successfully requested {len(match_ids)} latest match ids")
    
    return match_ids

def get_match_by_id(match_id: int) -> dict:
    url = f"https://api.opendota.com/api/matches/{match_id}"
    match_data_response = pgdu.make_request_with_retries(url)
    if not match_data_response.status_code == 200:
        raise ConnectionError(f'Error getting match data: {match_data_response.status_code}')
    return match_data_response

# TODO das fetchen und parsen von match data splitten, damit man das testen kann
def validate_clean_match_data(match_data_json: dict) -> dict:
    """validate and clean match data from the OpenDota API /parsedMatches endpoint.

    Args:
        match_id (int): Match id

    Raises:
        ValueError: match does not meet the following criteria:
                    - game_mode = 22 all_pick
                    - lobby_type = 7 ranked
                    - region = 3 EUROPE
                    - player leaver_status = 1 -> don't parse the game
                    - duration < 60 * 25 -> don't parse, possibly a stomp
                    - if any player data['players']{}['randomed'] -> don't parse

    Returns:
        dict: parsed match data as dict
    """    

    # TODO check if required keys are present (cause of occasional exception?)
    
    if match_data_json['game_mode'] == 22 and match_data_json['lobby_type'] == 7 and match_data_json['region'] == 3 and match_data_json['duration'] > 60 * 25:
        match_data = pgdu.clean_match_data(match_data_json)
        if any([(player['leaver_status'] == 1 or player['randomed'] == 1) for player in match_data['players']]):
            raise ValueError("player left or randomed")

        for id, player in enumerate(match_data['players']):
            match_data['players'][id] = pgdu.clean_player_data(player)
        return match_data
    else: 
        raise ValueError("game mode, lobby_type, region or duration not meeting requirements")

def parse_and_dump_match_data(match_ids: list[int], output_dir: str, parsed_match_ids: list[int] = None) -> None:
    """GET, parse and save all matches from lsit of IDs to a given output directory.

    Args:
        match_ids (list[int]): Pre-queried match ids
        output_dir (str): Directory to save the JSONs to
        parsed_match_ids (list[int], optional): List of already existing match IDs which will be skipped when parsing. Defaults to None.
    """        
    # skip existing match ids
    if parsed_match_ids:
        new_matches = [m for m in match_ids if m not in parsed_match_ids]
    else:
        new_matches = match_ids
        
    logger.info(f"Now parsing match data for {len(new_matches)} matches (skipping {len(match_ids) - len(new_matches)} existing matches)")
    
    for m_id in tqdm(new_matches):
        try:
            # clean match response data
            match_data_res = get_match_by_id(m_id)
            match_data = validate_clean_match_data(match_data_res.json())
            
            # dump match_data to json file
            match_id = match_data['match_id']
            output_file = os.path.join(output_dir, f'{match_id}.json')    
                
            with open(output_file, 'w', encoding='utf8') as file:
                logger.debug(f'Saving match data to {output_file}')
                json.dump(match_data, file, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
                
        except ValueError as e:
            logger.debug(f"Parsing error in match id {m_id}: {e}")
            continue
        except Exception as e:
            logger.error(f"Exception while parsing match id {m_id}: {e}")
            continue