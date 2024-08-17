import time
import argparse
import logging
import os

from game_data_collector import parse_game_data


# Automatic background data collection script,
# will QUIT when daily limit reached
#
# Example usage
# python ./collect_data.py --output_dir '.\resources\data' --wait_time 900

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
    parser.add_argument('--wait_time', type = int, default=900, required=False, help= "Seconds to wait between fetching attempts")
    
    args = parser.parse_args()
    
    # stats
    it = 0
    total = 0
    
    while True:
        parsed_match_ids = [int(fi_name) for fi_name in get_filenames_without_extension(args.output_dir)]
        logger.info(f"Found {len(parsed_match_ids)} existing match dumps")

        # latest_matches = parse_game_data.get_latest_match_ids(limit=1000)
        
        try:
            latest_matches = parse_game_data.get_parsed_matches()
        except ValueError as e:
            logger.error(f"Failed to fetch latest parsedMatches: {e}")
            quit()
            
        parse_game_data.parse_and_dump_match_data(match_ids=latest_matches, output_dir=args.output_dir, parsed_match_ids=parsed_match_ids) 
        
        logger.info(f"Done parsing, collected {len(get_filenames_without_extension(args.output_dir))-len(parsed_match_ids)} new matches")
        total += len(get_filenames_without_extension(args.output_dir))-len(parsed_match_ids)
        it += 1
        logger.info(f"Finished iteration {it}, collected {total} parsedMatches in total. Now waiting {args.wait_time/60} mins ..\n")
        time.sleep(args.wait_time) # wait 30 min