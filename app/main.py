from fastapi import FastAPI, HTTPException
from .services.youtube_service import YouTubeService
from .services.notion_service import NotionService
from .services.legal_service import LegalService
from .schemas.models import CommentResponse, ApiResponseBody
from .services.coupang_service import CoupangService
from .config import settings
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import uvicorn

app = FastAPI()

# 다른 서비스들은 상태를 유지하지 않으므로 전역 변수로 유지
youtube_service = YouTubeService()
notion_service = NotionService(
    api_key=settings.NOTION_TOKEN,
    database_id=settings.NOTION_DATABASE_ID
)
legal_service = LegalService()

# @app.post("/process-comments/", response_model=CommentResponse)
# async def process_comments(youtube_url: str):
#     try:
#         video_id = youtube_service.extract_video_id(youtube_url)
#         print(settings.YOUTUBE_API_KEY)
#         print(video_id)
#         comments = youtube_service.fetch_comments(video_id)
#         notion_service.update_database(comments)
        
#         return CommentResponse(
#             video_id=video_id,
#             message="Notion database updated successfully",
#             comment_count=len(comments),
#             comments=comments
#         )
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) 

# @app.get("/legal", response_model=ApiResponseBody)
# async def process_legal():
#     try:
     
#         legal_list = legal_service.fetch_incident_info(event_no='2009헌라8')
#         print(legal_list)
   
#         # notion_service.update_database(legal_list)

#         if not legal_list:
#             legal_list = [
#             {
#                 "event_no": "N/A",
#                 "event_nm": "No Data",
#                 "inq_date": None,
#                 "req_law": None,
#                 "law_suit": None,
#                 "end_date": None,
#                 "end_rsta": None,
#                 "adju_date": None,
#                 "chg_date": None,
#                 "decision_details": []
#             }
#         ]
        
#         return ApiResponseBody(
#             items=legal_list,
#             num_of_rows=len(legal_list),
#             page_no=1,
#             total_count=len(legal_list)
#         )
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) 

@app.post("/coupang")
async def process_coupang(product_url: str, review_count: int = 5):
    try:
        coupang_service = CoupangService()
        reviews = coupang_service.fetch_reviews(product_url, review_count)
        return {
            "message": "Reviews fetched successfully",
            "review_count": len(reviews),
            "reviews": reviews
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    
