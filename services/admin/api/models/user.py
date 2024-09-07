import uuid
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.base import SoftDeleteMixin
from database import Base


class User(SoftDeleteMixin, Base):
    __tablename__ = 'users'
    
    uid = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(50), unique=True, nullable=True)

    borrow_requests = relationship("BookBorrowRequest", back_populates="user")
    
    __table_args__ = (
        UniqueConstraint('email', name='uq_email'),
    )

    def __str__(self):
        return self.email
    