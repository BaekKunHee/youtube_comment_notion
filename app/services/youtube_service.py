from googleapiclient.discovery import build
from ..config import settings
from ..schemas.models import Comment
from typing import List

class YouTubeService:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    def fetch_comments(self, video_id: str, keyword: str) -> List[Comment]:
        # YouTube 댓글 가져오는 로직
        pass

    @staticmethod
    def extract_video_id(url: str) -> str:
        # URL에서 video_id 추출하는 로직
        pass 