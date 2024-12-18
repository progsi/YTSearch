
import json
import os
from datetime import datetime


def write_json_to_disk(data, filepath):
    """
    Write JSON data to a file on disk.

    Args:
    - data (dict): JSON data to be written to the file.
    - filepath (str): Path to the file where JSON data will be written.
    """
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"JSON data has been written to '{filepath}' successfully.")
    except Exception as e:
        print(f"An error occurred while writing JSON data to '{filepath}': {e}")

    
def get_current_timestamp():
    """
    Get the current timestamp in the format: YYYYMMDD_HHMMSS.

    Returns:
    - str: Current timestamp in the specified format.
    """
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")
    return timestamp

def get_store_filepath(store_dir: str, identifier: str, max_results: int):
    filename = '-'.join((get_current_timestamp(), identifier.replace(" ", "_"), str(max_results)))
    sanitized_filename = sanitize_filename(filename)
    return os.path.join(store_dir, sanitized_filename + '.json') 

def sanitize_filename(filename):
    """
    Transform a string into a valid filename.

    Args:
    - filename (str): The string to be transformed into a filename.

    Returns:
    - str: Valid filename derived from the input string.
    """
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    cleaned_filename = ''.join(c if c in valid_chars else '_' for c in filename)
    cleaned_filename = cleaned_filename.strip()
    cleaned_filename = '_'.join(part for part in cleaned_filename.split('_') if part)
    if not cleaned_filename:
        cleaned_filename = 'untitled'
    return cleaned_filename

def is_valid_response(r: dict) -> bool:
    KIND_LABEL = "youtube#searchListResponse"
    return r.get("kind") == KIND_LABEL