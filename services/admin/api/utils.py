from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from api.models import Book, User, BookBorrowRequest
from database import SessionLocal


def process_message(event: str, data: str):
    db = SessionLocal()
    if event == "user.enrolled":
        new_user = User(**data)
        db.add(new_user)
        db.commit()
        print("User created")
    elif event == "book.borrowed":
        new_borrow_request = BookBorrowRequest(
            uid=data["uid"], 
            book_uid=data["book"],
            user_uid=data["user"],
            period=data["period"],
            request_date=data["request_date"]
        )
        db.add(new_borrow_request)
        db.commit()
        print("Book borrowed.")