
import os
import json

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

if __name__ == "__main__":
    files = get_filenames_without_extension("resources/data")
    print(files[:10])
    print(len(files))
    with open("match_id_diff.json", "w") as fi:
        json.dump(files, fi)
