import json
import argparse
import sys
import logging
import os

sys.path.insert(1, "../../src/database")

import mongodb

logging.basicConfig(
    level=logging.INFO,  # Set the minimum level of messages to capture
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the format of the log messages
)


def add_games_from_directory(game_db: mongodb.MongoDB, directory: str, batch) -> None:

    if batch:
        all_games = []

    for file in os.listdir(directory):

        if file.endswith(".json"):

            file_path = os.path.join(directory, file)

            try:
                with open(file_path, "r") as f:
                    game_data = json.load(f)
            except Exception as e:
                raise RuntimeError(
                    f"Some error occurred in reading game data from {file_path}: {e}"
                )

            game_data["_id"] = game_data[
                "match_id"
            ]  # so that database id and match id are the same
            if batch:
                all_games.append(game_data)
            else:
                game_db.insert_item(game_db.collection_name, game_data)

    if batch:

        game_db.insert_item(game_db.collection_name, all_games)


def create_game_db(
    host: str = "localhost",
    port: int = 27017,
    username: str = "root",
    password: str = "example",
    database_name: str = "mmr_predictor",
    collection_name: str = "dota_game_collection",
    path: str = None,
    batch: bool = True,
) -> None:

    # we are keeping all the game data in directories

    game_db = mongodb.MongoDB(
        host=host, port=port, username=username, password=password
    )

    logging.info(type(game_db))

    game_db.connect_db()
    game_db.get_database(database_name)
    game_db.get_collection(collection_name)

    if len(path) > 1:
        logging.info("Found a list of directories.")
    else:
        logging.info("Found a single directory")

    for directory in path:

        logging.info(f"Adding files from directory: {directory}")

        add_games_from_directory(game_db, directory, batch)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Parse arguments to add game data to the database")
    parser.add_argument(
        "--host", default="localhost", type=str, help="MongoDB instance host address"
    )
    parser.add_argument(
        "--port", default=27017, type=int, help="MongoDB instance port id"
    )
    parser.add_argument(
        "--username", default="root", type=str, help="MongoDB instance username"
    )
    parser.add_argument(
        "--password", default="example", type=str, help="MongoDB instance password"
    )
    parser.add_argument(
        "--database_name",
        default="mmr_predictor",
        type=str,
        help="MongoDB database name to create the collection",
    )
    parser.add_argument(
        "--collection_name",
        default="dota_game_collection",
        type=str,
        help="MongoDB collection name to add game data to",
    )
    parser.add_argument(
        "--path",
        nargs="+",
        help="Absolute path of the directory/ies where the game data is. If a list of directories is given, each directory will be parsed sequentially",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Enable batch insertion of game data per directory. Otherwise each game will be added sequantially",
    )

    args = parser.parse_args()

    logging.info(
        f"Following are passed to the argument parser\
        {vars(args)}"
    )

    create_game_db(
        args.host,
        args.port,
        args.username,
        args.password,
        args.database_name,
        args.collection_name,
        args.path,
        args.batch,
    )
