import datetime
from typing import Optional
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Date, func, select, SQLColumnExpression
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Session
from api.models.base import SoftDeleteMixin
from database import Base


class Book(SoftDeleteMixin, Base):
    __tablename__ = "books"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    author = Column(String(100), nullable=True)
    title = Column(String(100), nullable=False)
    publisher = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    
    borrow_requests = relationship("BookBorrowRequest", back_populates="book")

    @hybrid_property
    def is_available(self):
        last_request = max(self.borrow_requests, key=lambda req: req.request_date, default=None)
       
        if last_request:
            return last_request.return_date <= datetime.date.today()
        return True
    
    @hybrid_property
    def return_date(self):
        last_request = max(self.borrow_requests, key=lambda req: req.request_date, default=None)
       
        if last_request:
            return last_request.return_date
        return None
    
    

class BookBorrowRequest(SoftDeleteMixin, Base):
    __tablename__ = 'book_borrow_requests'
    
    uid = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    user_uid = Column(UUID(as_uuid=True), ForeignKey('users.uid', ondelete='SET NULL'), nullable=True)
    book_uid = Column(UUID(as_uuid=True), ForeignKey('books.uid', ondelete='SET NULL'), nullable=True)
    period = Column(Integer, nullable=False)
    request_date = Column(Date, server_default=func.now(), nullable=False)
    
    book = relationship("Book", back_populates="borrow_requests")
    user = relationship("User", back_populates="borrow_requests")

    @hybrid_property
    def return_date(self):
        return self.request_date + datetime.timedelta(days=self.period)