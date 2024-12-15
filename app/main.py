from fastapi import FastAPI, HTTPException
from .services.youtube_service import YouTubeService
from .services.notion_service import NotionService
from .schemas.models import CommentResponse
from .config import settings
app = FastAPI()
youtube_service = YouTubeService()
notion_service = NotionService()

@app.post("/process-comments/", response_model=CommentResponse)
async def process_comments(youtube_url: str):
    try:
        video_id = youtube_service.extract_video_id(youtube_url)
        print(settings.YOUTUBE_API_KEY)
        print(video_id)
        comments = youtube_service.fetch_comments(video_id)
        notion_service.update_database(comments)
        
        return CommentResponse(
            video_id=video_id,
            message="Notion database updated successfully",
            comment_count=len(comments),
            comments=comments
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 