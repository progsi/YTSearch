from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import get_store_filepath, write_json_to_disk
import os
import argparse


def search_by_query(api_key: str, query: str, max_results: int):
    """
    Search for YouTube videos based on a query string.

    Args:
    - api_key (str): Your YouTube Data API key.
    - query (str): The search query.
    - max_results (int): Maximum number of results to return (default is 50).

    Returns:
    - List of dictionaries, each representing a video, with keys:
        - title (str): Title of the video.
        - video_id (str): ID of the video.
        - thumbnail_url (str): URL of the video's thumbnail.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results
        ).execute()

        # write to disk
        store_dir = "response"
        identifier = query.replace("-", " ").replace("_", " ")
        filepath = get_store_filepath(store_dir, identifier, max_results)
        write_json_to_disk(search_response, filepath)

        return search_response

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
        return None
    

def search_by_song(api_key: str, song_title: str, expansion: str, max_results: int = 50):

    q = ' '.join((song_title, expansion)).strip().lower()

    videos = search_by_query(api_key=api_key, query=q, max_results=max_results)

    return videos


def get_api_key(file_path='apikey.txt'):
    """
    Get the API key from a file.

    Args:
    - file_path (str): Path to the file containing the API key.

    Returns:
    - str: API key read from the file.
    """
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


def parse_args():

    parser = argparse.ArgumentParser(description="Search on YouTube given a song title and an expansion...")
    parser.add_argument("-q", type=str, help="The search query.")
    parser.add_argument("-m", type=int, help="Maximum search results to return per query.", default=50)
    return parser.parse_args()

def main():

    args = parse_args()
    q = args.q
    m = args.m
    api_key = get_api_key()

    search_by_query(api_key=api_key, query=q, max_results=m )


if __name__ == "__main__":
    main()
