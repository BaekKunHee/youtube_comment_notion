from pydantic import BaseModel
from datetime import datetime
from typing import List

class Comment(BaseModel):
    text: str
    likes: int
    author: str
    published_at: datetime

class CommentResponse(BaseModel):
    message: str
    comment_count: int
    comments: List[Comment] 