import requests
from ..config import settings
from ..schemas.models import Comment
from typing import List

class NotionService:
    def __init__(self):
        self.token = settings.NOTION_TOKEN
        self.database_id = settings.NOTION_DATABASE_ID
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def update_database(self, comments: List[Comment]) -> None:
        # Notion 데이터베이스 업데이트 로직
        pass 