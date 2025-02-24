import requests
from ..config import settings
from ..schemas.models import Review
from typing import List

class NotionService:
    def __init__(self):
        # 빈 초기화 함수로 변경
        pass

    def update_database(self, reviews: List[Review], api_key: str, database_id: str) -> None:
        """
        노션 데이터베이스에 리뷰 목록을 업데이트하는 메서드
        
        Args:
            reviews (List[Review]): 업데이트할 리뷰 목록
            api_key (str): Notion API 키
            database_id (str): Notion 데이터베이스 ID
        """
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # 데이터베이스 존재 여부 먼저 확인
        check_url = f"https://api.notion.com/v1/databases/{database_id}"
        try:
            check_response = requests.get(check_url, headers=headers)
            check_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception(
                    "데이터베이스를 찾을 수 없습니다. 다음을 확인해주세요:\n"
                    "1. 데이터베이스 ID가 올바른지 확인\n"
                    "2. Notion 통합(Integration)이 데이터베이스에 연결되어 있는지 확인"
                )
            raise

        url = "https://api.notion.com/v1/pages"

        print("Database ID:", database_id)  # 디버깅을 위한 출력
        print("Comments:", reviews)

        for review in reviews:
            # 노션 페이지 생성을 위한 요청 본문
            payload = {
                "parent": {"database_id": database_id},
                "properties": {
                    "작성자": {
                        "title": [
                            {
                                "text": {
                                    "content": review.writer
                                }
                            }
                        ]
                    },
                    "별점": {
                        "number": review.rating
                    },
                    "작성일": {
                        "rich_text": [
                            {
                                "text": {"content": review.date}
                            }
                        ]
                    },
                    "제품명": {  
                        "rich_text": [
                            {
                                "text": {"content": review.product_name}
                            }
                        ]
                    },
                    "리뷰내용": {
                        "rich_text": [
                            {
                                "text": {"content": review.content}
                            }
                        ]
                    }

                }
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                print(f"Successfully added review from {review.writer}")
            except requests.exceptions.HTTPError as http_err:
                print(f"Error response: {http_err.response.text}")
                raise Exception(f"HTTP error occurred: {http_err.response.text}")
            except requests.exceptions.RequestException as req_err:
                raise Exception(f"Request error occurred: {str(req_err)}")