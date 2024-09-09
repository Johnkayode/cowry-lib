from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

from .book import BookBorrowRequestModel


class UserModel(BaseModel):
    uid: UUID
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    borrow_requests: Optional[List[BookBorrowRequestModel]]

    class Config:
        from_attributes = True  
        arbitrary_types_allowed=True
