from enum import Enum
import pymongo.collection
import requests
import json
import logging
import pandas as pd

import game_data_collector.parse_game_data_utils as pgdu

logger = logging.getLogger(__name__)

class Role(Enum):
    ANY = 0
    CARRY = 1 # name = value
    DISABLER = 2
    DURABLE = 3
    ESCAPE = 4
    INITIATOR = 5
    NUKER = 6
    PUSHER = 7
    SUPPORT = 8
    
# Experimental getter function combines several preprocessing steps

def get_kpis_by_role(col: pymongo.collection, role: Role, rank_nin: list = [None, 80]) -> pd.DataFrame:

    # Aggregation pipeline
    pipeline = [
        {"$unwind": "$players"},
        {"$group": {
            "_id": None, 
            "rank_tier": {"$push": {"$ifNull": ["$players.rank_tier", 0]}}, 
            "hero_id": {"$push": "$players.hero_id"},
            "kda": {"$push": "$players.kda"},
            "last_hits": {"$push": "$players.last_hits"},
            "actions_per_min": {"$push": "$players.actions_per_min"},
            "gold_per_min": {"$push": "$players.benchmarks.gold_per_min.raw"},
            "xp_per_min": {"$push": "$players.benchmarks.xp_per_min.raw"}}},
        {"$project": {"_id": 0, "rank_tier": 1, "hero_id": 1, "kda": 1, "last_hits": 1, "actions_per_min": 1, "gold_per_min": 1, "xp_per_min": 1}},   # Exclude the _id from the result
    ]
    
    if rank_nin:
        pipeline.insert(1, {"$match": {"players.rank_tier": {"$nin": rank_nin}}})
        
    if role != Role.ANY:
        role_ids: list[int] = get_hero_ids_of_role(role)
        pipeline.insert(2, {"$match": { "players.hero_id": { "$in": role_ids }}})

    # Execute the aggregation pipeline
    result = list(col.aggregate(pipeline))

    if not len(result) == 1:
        print(result)
        raise Exception("More than one results returned")

    df = pd.DataFrame.from_dict(result[0])

    if role != Role.ANY:
        # check if role filtering worked
        assert(set(df.hero_id).issubset(set(role_ids)))

    # inject hero name (just for fun)
    # df.hero_id = df.hero_id.map(heroes_ids_roles.localized_name.to_dict())
    return df
    

def get_hero_ids_of_role(role: Role) -> list[int]:
    # prepare sql
    if not role == Role.ANY:
        sql: str = f"SELECT id from heroes WHERE LOWER('{role.name}') = ANY(ARRAY(SELECT LOWER(role) FROM unnest(roles) AS role)) ORDER BY heroes.id ASC;"
    else:
        sql: str = f"SELECT id from heroes ORDER BY heroes.id ASC;"

    # make api request
    res: requests.Response = pgdu.make_request_with_retries(f"https://api.opendota.com/api/explorer?sql={sql}")
    role_ids: list[dict] = []
    if res.status_code != 200:
        raise ValueError(f'Failed to retrieve data: {res.status_code}')
    else:
        # process response
        role_ids = json.loads(res.text)
        assert "rows" in role_ids.keys() and len(role_ids["rows"]) > 0, "no rows to process for role ids"
        return [e["id"] for e in list(role_ids["rows"])]