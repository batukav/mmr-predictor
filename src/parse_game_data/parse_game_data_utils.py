import requests
import json
import time

def clean_player_data(player_dict: dict) -> dict:
    
    """
    Cleans a player data dictionary by removing specified keys that are deemed unnecessary.

    Args:
        player_dict (dict): The original player data dictionary containing various keys and values.

    Returns:
        dict: The cleaned player data dictionary with specified keys removed.

    Notes:
        - This function removes a predefined list of keys from the player data dictionary.
        - The removed keys include various logs, actions, reasons, item data, cosmetic data, and other metadata.
        - If a key is removed, a message is printed indicating which key was removed.

    Removed Keys:
        'firstblood_claimed', 'towers_killed', 'roshans_killed', 'max_hero_hit', 'times',
        'gold_t', 'lh_t', 'dn_t', 'xp_t', 'purchase_log', 'kills_log', 'buyback_log', 
        'runes_log', 'connection_log', 'actions', 'gold_reasons', 'xp_reasons', 'killed',
        'ability_targets', 'damage', 'healing', 'lane_pos', 'damage_targets', 'damage_taken',
        'damage_inflictor', 'killed_by', 'randomed', 'pred_vict', 'hero_hits', 'party_id',
        'permanent_buffs', 'party_size', 'team_number', 'team_slot', 'item_0', 'item_1', 
        'item_2', 'item_3', 'item_4', 'item_5', 'backpack_0', 'backpack_1', 'backpack_2', 
        'item_neutral', 'aghanims_scepter', 'aghanims_shard', 'moonshard', 'ability_upgrades_arr',
        'personaname', 'name', 'last_login', 'radiant_win', 'start_time', 'duration', 'cluster',
        'lobby_type', 'game_mode', 'is_contributor', 'patch', 'region', 'isRadiant', 'purchase_time',
        'first_purchase_time', 'item_win', 'item_usage', 'is_subscriber', 'cosmetics', 'ability_uses',
        'damage_inflictor_received'
    """
    keys_to_be_removed = [
    'firstblood_claimed',
    'towers_killed',
    'roshans_killed',
    'max_hero_hit',
    'times',
    'gold_t',
    'lh_t', 'dn_t', 'xp_t',
    'purchase_log',
    'kills_log', 'buyback_log', 'runes_log',
    'connection_log',
    'actions',
    'gold_reasons',
    'xp_reasons',
    'killed',
    'ability_targets',
    'damage',
    'healing',
    'lane_pos',
    'damage_targets',
    'damage_taken',
    'damage_inflictor',
    'killed_by',
    'randomed',
    'pred_vict', 'hero_hits',
    'party_id', 'permanent_buffs', 'party_size',
    'team_number', 'team_slot',
    'item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'backpack_0', 'backpack_1', 'backpack_2', 'item_neutral',
    'aghanims_scepter', 'aghanims_shard', 'moonshard',
    'ability_upgrades_arr', 'personaname', 'name', 'last_login',
    'radiant_win', 'start_time', 'duration', 'cluster',
    'lobby_type', 'game_mode', 'is_contributor', 'patch', 'region', 'isRadiant',
    'purchase_time', 'first_purchase_time', 'item_win', 'item_usage',
    'is_subscriber', 'cosmetics', 'ability_uses','damage_inflictor_received',
    ]
    
    # player_dict = {key: value for key, value in player_dict.items() if key not in keys_to_be_removed}
    new_player_dict = {}
    for key, value in player_dict.items():
        if key in keys_to_be_removed:
            print(f"Removed key: {key}")
        else:
            new_player_dict[key] = value

    # Update the original dictionary with the new one
    player_dict = new_player_dict
    
    return player_dict

def clean_match_data(match_dict: dict) -> dict:
    
    """
    Cleans a match data dictionary by removing specified keys that are deemed unnecessary.

    Args:
        match_dict (dict): The original match data dictionary containing various keys and values.

    Returns:
        dict: The cleaned match data dictionary with specified keys removed.

    Notes:
        - This function removes a predefined list of keys from the match data dictionary.
        - The removed keys include version information, draft timings, teamfights data, objectives,
          chat logs, gold and XP advantages, cosmetic data, league and series information, and other metadata.
        - If a key is removed, a message is printed indicating which key was removed.

    Removed Keys:
        'version', 'draft_timings', 'teamfights', 'objectives', 'chat', 'radiant_gold_adv', 
        'radiant_xp_adv', 'cosmetics', 'leagueid', 'start_time', 'series_id', 'series_type', 
        'cluster', 'replay_salt', 'pre_game_duration', 'match_seq_num', 'tower_status_radiant', 
        'tower_status_dire', 'barracks_status_radiant', 'barracks_status_dire', 'first_blood_time', 
        'human_players', 'game_mode', 'region', 'throw', 'loss', 'all_word_counts', 'my_word_counts', 
        'flags', 'patch', 'engine', 'picks_bans', 'od_data'
    """
    keys_to_be_removed = [
        'version', 'draft_timings','teamfights',
        'objectives', 'chat',  'radiant_gold_adv', 'radiant_xp_adv', 
        'cosmetics', 'leagueid', 'start_time', 'series_id', 
        'series_type', 'cluster', 'replay_salt',
        'pre_game_duration', 'match_seq_num', 
        'tower_status_radiant', 'tower_status_dire', 
        'barracks_status_radiant', 'barracks_status_dire', 
        'first_blood_time', 'human_players', 'game_mode', 
        'region', 'throw', 'loss',
        'all_word_counts','my_word_counts',
        'flags','patch', 'engine',
        'picks_bans','od_data'
    ]
    
    # match_dict = {key: value for key, value in match_dict.items() if key not in keys_to_be_removed}
    new_match_dict = {}
    for key, value in match_dict.items():
        if key in keys_to_be_removed:
            print(f"Removed key: {key}")
        else:
            new_match_dict[key] = value

    # Update the original dictionary with the new one
    match_dict = new_match_dict
    
    return match_dict

def get_url(url: str) -> dict:
    
    response = requests.get(url)
    assert response.status_code == 200, f'Failed to retrive data: {response.status_code}'
    data = response.json()
  
    return data

def make_request_with_retries(url: str, max_retries: int=5) -> requests.Response:
    
    """
    Makes an HTTP GET request to the specified URL, handling 429 Too Many Requests errors
    with retry logic and exponential backoff, and optionally handling other server errors.

    Args:
        url (str): The URL to send the HTTP GET request to.
        max_retries (int): The maximum number of retries before giving up. Default is 5.

    Returns:
        requests.Response: The response object from the successful HTTP GET request.

    Raises:
        Exception: If the maximum number of retries is reached without a successful response.

    Retries:
        - If a 429 status code is received, retries the request after the duration specified in 
          the 'Retry-After' header if present, otherwise uses exponential backoff.
        - If a server error (status codes 500, 502, 503, 504, 408, 409) is received, retries the request 
          using exponential backoff.

    Note:
        - The retry wait time doubles with each retry, i.e., exponential backoff, to reduce the load on the server.
        - If the 'Retry-After' header is present in a 429 response, its value is used as the wait time for retries.
    """
    
    retries = 0
    
    force_errors = [500, 502, 503, 504, 408, 409]

    while retries < max_retries:
        response = requests.get(url)
        
        if response.status_code == 429:
            if 'Retry-After' in response.headers:
                wait_time = int(response.headers['Retry-After'])
                print(f"Received 429 Too Many Requests. Retrying after {wait_time} seconds...")
            else:
                wait_time = 2 ** retries  # Fallback to exponential backoff
                print(f"Received 429 Too Many Requests. Retrying after a fallback wait time of {wait_time} seconds...")            
            retries += 1
            time.sleep(wait_time)
        elif response.status_code in force_errors:
            wait_time = 2 ** retries
            time.sleep(wait_time)
            retries += 1
        else:
            return response

        # If max retries reached
        raise Exception(f"Max retries reached. Could not complete the request. Last status code: {response.status_code}")
