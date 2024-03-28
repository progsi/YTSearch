import pandas as pd
import os
from datetime import datetime
import json


def parse_filename(filename: str):
    """
    Parse filename into timestamp, query, and number.

    Args:
    - filename (str): The filename string.

    Returns:
    - tuple: (timestamp, query, number)
    """
    parts = filename.split('-')
    
    # Parse timestamp
    timestamp_str = parts[0]
    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
    
    # Extract query and replace underscores with spaces
    query = parts[1].replace('_', ' ')
    
    # Extract number and convert to integer
    number = int(parts[2].split('.')[0])  # Remove extension and convert to int
    
    return timestamp, query, number

def parse(filepath: str):

    timestamp, query, max_results = parse_filename(os.path.basename(filepath))

    with open(filepath, "r") as f:
        response = json.load(f)
    
    video_data = pd.json_normalize(response["items"])
    video_data["timestamp"] = timestamp
    video_data["query"] = query
    video_data["max_results"] = max_results
    video_data["regionCode"] = response["regionCode"]

    return video_data


def parse_all(dirpath: str):

    data = pd.DataFrame()
    for file in os.listdir(dirpath):
        
        video_data = parse(os.path.join(dirpath, file))
        data = pd.concat([data, video_data], ignore_index=True)

    return data

def rename_columns(data):

    data.columns = [col.replace("snippet.", "") for col in data.columns]
    data = data.rename({
        "id.videoId": "yt_id",
        "channelTitle": "channel_name",
        "channelId": "channel_id",
        "publishedAt": "publish_date"
    }, axis=1)
    return data

def main():
    data = parse_all("response")    
    data = rename_columns(data)
    data.to_parquet("responses.parquet")


if __name__ == "__main__":
    main()