from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional

class Comment(BaseModel):
    text: str
    likes: int
    author: str
    published_at: datetime

class CommentResponse(BaseModel):
    message: str
    comment_count: int
    comments: List[Comment] 

class DecisionDetail(BaseModel):
    law_seq: Optional[int]
    data_tp: Optional[int]
    law_nm: Optional[str]
    provision: Optional[str]
    provision2: Optional[str]
    clause: Optional[str]
    item: Optional[str]
    sub_item: Optional[str]
    etc: Optional[str]
    law_num_tp: Optional[int]
    fr_law_num: Optional[int]
    to_law_num: Optional[int]
    fr_law_date: Optional[str]
    to_law_date: Optional[str]
    etc1: Optional[str]
    end_rsta: Optional[str]
    law_arti_clent: Optional[str]

class EventDetail(BaseModel):
    eventNo: str = "N/A"
    eventNm: str = "No Data"
    inqDate: Optional[str] = None
    reqLaw: Optional[str] = None
    lawSuit: Optional[str] = None
    dList: Optional[dict] = None
    dsList: Optional[dict] = None
    odList: Optional[dict] = None
    odsList: Optional[dict] = None
    inquirRsta: Optional[str] = None
    endDate: Optional[str] = None
    endRsta: Optional[str] = None
    adjuDate: Optional[str] = None
    chgDate: Optional[str] = None
    dscsList: Optional[List[dict]] = None
    annexList: Optional[dict] = None
    relateList: Optional[str] = None
    dtmPpXml: Optional[str] = None
    dtmPpHp: Optional[str] = None
    dtmPpApi: Optional[str] = None
    pdntList: Optional[dict] = None
    pdntGstList: Optional[dict] = None
    ogList: Optional[dict] = None
    dtmXpn: Optional[str] = None
    dtmGst: Optional[str] = None
    decision_details: Optional[List[DecisionDetail]] = []

class ApiResponseHeader(BaseModel):
    result_code: str
    result_msg: str

class ApiResponseBody(BaseModel):
    items: List[EventDetail]
    num_of_rows: int
    page_no: int
    total_count: int

    @field_validator("items", mode="before")
    @classmethod
    def validate_items(cls, value):
        if isinstance(value, dict):
            value = [value.get("item")] if "item" in value else []
        elif not isinstance(value, list):
            raise ValueError("`items` must be a list or contain an `item` field.")
        return value

class ApiResponse(BaseModel):
    header: ApiResponseHeader
    body: ApiResponseBody 

class Review(BaseModel):
    rating: Optional[int]
    content: str
    date: str
    images: List[str] = []
    product_name: str
    writer: str

    def __init__(self, **data):
        super().__init__(**data)
        self.product_name = data.get('product_name', '')
        self.writer = data.get('writer', '')

    @field_validator("rating", mode="before")
    @classmethod
    def validate_rating(cls, value):
        if value is None or not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, value):
        if not value:
            raise ValueError("Content cannot be empty")
        return value

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        if not value:
            raise ValueError("Date cannot be empty")
        return value

    @field_validator("images", mode="before")
    @classmethod
    def validate_images(cls, value):
        if not isinstance(value, list) or not all(isinstance(img, str) for img in value):
            raise ValueError("Images must be a list of strings")
        return value

    @field_validator("product_name", mode="before")
    @classmethod
    def validate_product_name(cls, value):
        if not value:
            raise ValueError("Product name cannot be empty")
        return value

    @field_validator("writer", mode="before")
    @classmethod
    def validate_writer(cls, value):
        if not value:
            raise ValueError("Writer cannot be empty")
        return value 