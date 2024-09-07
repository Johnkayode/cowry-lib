from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class CreateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    category: str


class BookModel(BaseModel):
    uid: UUID
    title: str
    author: Optional[str]
    publisher: str
    category: str
    is_available: bool
    created_at: datetime
    return_date: Optional[date]

    @property
    def is_available(self):
        return self.is_available
    
    @property
    def return_date(self):
        return self.return_date

    class Config:
        from_attributes = True  
        arbitrary_types_allowed=True


class BookBorrowRequestModel(BaseModel):
    uid: UUID
    book_uid: UUID
    period: int
    request_date: date
    return_date: Optional[date]

    @property
    def return_date(self):
        return self.return_date