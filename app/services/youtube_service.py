from googleapiclient.discovery import build
from ..config import settings
from ..schemas.models import Comment
from typing import List
import re
class YouTubeService:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    def fetch_comments(self, video_id: str) -> List[Comment]:
        """
        YouTube 동영상의 상위 10개 댓글을 가져오는 메서드

        Args:
            video_id (str): YouTube 동영상 ID

        Returns:
            List[Comment]: 댓글 목록
        """
        try:
            # 댓글 스레드 요청
            response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=10,
                order='relevance'  # 관련성 순으로 정렬
            ).execute()

            comments = []
            for item in response.get('items', []):
                comment_data = item['snippet']['topLevelComment']['snippet']
                comment = Comment(
                    author=comment_data['authorDisplayName'],
                    text=comment_data['textDisplay'],
                    likes=comment_data['likeCount'],  # like_count를 likes로 변경
                    published_at=comment_data['publishedAt']
                )
                comments.append(comment)

            return comments
        except Exception as e:
            raise Exception(f"Failed to fetch comments: {str(e)}")

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        YouTube URL에서 Video ID를 추출하는 메서드.

        Args:
            url (str): YouTube 동영상 URL.

        Returns:
            str: 추출된 Video ID. URL이 잘못되었을 경우 None.
        """
        # 다양한 YouTube URL 패턴
        patterns = [
            r"v=([^&]+)",  # https://www.youtube.com/watch?v=VIDEO_ID
            r"youtu\.be/([^?]+)",  # https://youtu.be/VIDEO_ID
            r"youtube\.com/embed/([^?&]+)"  # https://www.youtube.com/embed/VIDEO_ID
        ]
     

        # 패턴 순회하여 매칭
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)  # Video ID 반환

        # URL이 유효하지 않으면 None 반환
        return None