from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from api.models import Book, User, BookBorrowRequest
from database import SessionLocal


def process_message(event: str, data: str):
    db = SessionLocal()
    if event == "user.enrolled":
        user = db.query(User).filter(User.email == data["email"]).first()
        if not user:
            new_user = User(**data)
            db.add(new_user)
            db.commit()
            print("User created")
    elif event == "book.borrowed":
        borrow = db.query(BookBorrowRequest).filter(BookBorrowRequest.uid == data["uid"]).first()
        if not borrow:
            user = db.query(User).filter(User.uid == data["user"]).first()
            if not user:
                return
            book = db.query(Book).filter(Book.uid == data["book"]).first()
            if not book:
                return
            
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