from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import get_store_filepath, write_json_to_disk, is_valid_response
import os
import argparse

class YTSearch:
    def __init__(self, filepath_api_key: str, output_dir: str = ".", 
                 write_always: bool = False):
        self.api_key = get_api_key(filepath_api_key)
        self.output_dir = output_dir
        self.write_always = write_always

    def set_output_dir(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    
    def search_by_query(self, query: str, max_results: int):
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
        youtube = build('youtube', 'v3', developerKey=self.api_key)

        try:
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results
            ).execute()

            # write to disk
            store_dir = self.output_dir
            identifier = query.replace("-", " ").replace("_", " ")
            filepath = get_store_filepath(store_dir, identifier, max_results)
            
            if self.write_always or is_valid_response(search_response):
                write_json_to_disk(search_response, filepath)

            return {
                'query': query,
                'max_results': max_results,
                'filepath': filepath,
                'response': search_response
            }

        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
            return None

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
    parser.add_argument("--api_key", type=str, help="Filepath to apikey of YouTube Data API", default="apikey.txt")
    parser.add_argument("--output_dir", type=str, help="Output directory", default=".")
    parser.add_argument("--write_always", action="store_true", help="Write to disk even if response is invalid")
    return parser.parse_args()

def main():

    args = parse_args()
    q = args.q
    m = args.m

    ytsearch = YTSearch(args.api_key, args.output_dir, args.write_always)
    ytsearch.search_by_query(query=q, max_results=m )

if __name__ == "__main__":
    main()
