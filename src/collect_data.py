import time
import argparse

from game_data_collector import parse_game_data
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s [%(levelname)s]: %(message)s', datefmt='%H:%M')

        
# created by Chad GPT
def get_filenames_without_extension(directory):
    """
    Reads the filenames in the given directory (non-recursively) and returns the names without the filetype extension in a list.

    Parameters:
    directory (str): The path to the directory.

    Returns:
    list: A list of filenames without their filetype extensions.
    """
    filenames = []
    
    try:
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                # Split the filename into name and extension and append the name part to the list
                name, _ = os.path.splitext(filename)
                filenames.append(name)
    except Exception as e:
        print(f"An error occurred: {e}")
            
    return filenames


if __name__  == '__main__':
    
    parser = argparse.ArgumentParser(description="Parsing arguments to fetch, process, and save game data")
    parser.add_argument('--output_dir', type = str, required=True, help= "Path to the output root directory. Each game data will be saved to this directory separately as {match_id}.json")
    args = parser.parse_args()
    
    parsed_match_ids = [int(fi_name) for fi_name in get_filenames_without_extension(args.output_dir)]
    logger.info(f"Found {len(parsed_match_ids)} existing match dumps")

    # latest_matches = parse_game_data.get_latest_match_ids(limit=1000)
    latest_matches = parse_game_data.get_parsed_matches()
    parse_game_data.parse_and_dump_match_data(match_ids=latest_matches, output_dir=args.output_dir, parsed_match_ids=parsed_match_ids) 
    
    logger.info(f"Done parsing, collected {len(get_filenames_without_extension(args.output_dir))-len(parsed_match_ids)} new matches")