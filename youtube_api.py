import os
from googleapiclient.discovery import build

os.environ["YOUTUBE_API_KEY"] = ""

class YouTubeAPI:
    def __init__(self):
        self.api = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

    def search_videos(self, keywords, filters, max_results):
        request = self.api.search().list(
            q=keywords,
            part='snippet',
            type='video',
            maxResults=max_results,
            videoDefinition=filters.get('videoDefinition', 'any'),
            videoDimension=filters.get('videoDimension', 'any'),
            videoDuration=filters.get('videoDuration', 'any'),
            videoEmbeddable=filters.get('videoEmbeddable', 'any'),
            videoLicense=filters.get('videoLicense', 'any'),
            videoType=filters.get('videoType', 'any'),
            location=filters.get('location', None),
            locationRadius=filters.get('locationRadius', None),
            order=filters.get('order', 'relevance'),
            publishedAfter=filters.get('publishedAfter', None)
        )
        response = request.execute()
        return response['items']

    def get_video_details(self, video_id):
        request = self.api.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()
        return response['items'][0]['snippet']