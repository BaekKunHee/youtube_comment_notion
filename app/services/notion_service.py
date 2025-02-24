import requests
from ..config import settings
from ..schemas.models import Comment
from typing import List

class NotionService:
    def __init__(self, api_key: str, database_id: str):
        self.token = api_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def update_database(self, comments: List[Comment]) -> None:
        """
        노션 데이터베이스에 댓글 목록을 업데이트하는 메서드
        
        Args:
            comments (List[Comment]): 업데이트할 댓글 목록
        """
        url = f"https://api.notion.com/v1/pages"

        print("Database ID:", self.database_id)  # 디버깅을 위한 출력
        print("Comments:", comments)

        for comment in comments:
            # 노션 페이지 생성을 위한 요청 본문
            payload = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "작성자": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": comment.author
                                }
                            }
                        ]
                    },
                    "내용": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": comment.text[:2000] if comment.text else ""  # Notion API 제한
                                }
                            }
                        ]
                    },
                    "좋아요": {
                        "number": comment.likes
                    },
                    "비고": {  # Title 필드는 항상 포함되어야 함
            "title": [
                {
                                "text": {"content": "Example Title"}
                            }
                        ]
                    }
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                print(f"Successfully added comment from {comment.author}")
            except requests.exceptions.HTTPError as http_err:
                print(f"Error response: {http_err.response.text}")  # 자세한 에러 메시지 출력
                raise Exception(f"HTTP error occurred: {http_err.response.text}")
            except requests.exceptions.RequestException as req_err:
                raise Exception(f"Request error occurred: {str(req_err)}")