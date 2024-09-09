import uvicorn
from contextlib import asynccontextmanager
from decouple import AutoConfig
from typing import List
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.models import Book, User
from api.schemas import CreateBookModel, BookModel, UserModel
from database import Base, engine, get_db
from rabbitmq import RabbitMQClient

config = AutoConfig()

rabbitmq_url = config("AMQP_URL", default="amqp://guest:guest@rabbitmq:5672/")
rabbitmq_client = RabbitMQClient(rabbitmq_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_client.start_consume("admin_updates")
    print("RabbitMQ consumer started.")
    yield
    await rabbitmq_client.close()


app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)


## API ROUTES ##
@app.get("/api/books", response_model=List[BookModel])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.post("/api/books", response_model=BookModel)
async def create_book(book: CreateBookModel, db: Session = Depends(get_db)):
    db_book = Book(**book.dict()) 
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    await rabbitmq_client.publish("core_updates", {
        "event_type": "book.created",
        "data": {"uid": str(db_book.uid), **book.dict()}
    })
    return db_book

@app.get("/api/books/unavailable", response_model=List[BookModel])
def get_unavailable_books(db: Session = Depends(get_db)):
    # TODO: Set sql expressions for properties and use filter 
    unavailable_books = [book for book in db.query(Book).all() if not book.is_available]
    return unavailable_books

@app.get("/api/books/{book_uid}", response_model=BookModel)
def get_book(book_uid: UUID, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.uid == book_uid).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/api/books/{book_uid}")
async def delete_book(book_uid: UUID, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.uid == book_uid).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=404, detail="Book is not available.")
    
    db.delete(book)
    db.commit()
    await rabbitmq_client.publish("core_updates", {
        "event_type": "book.deleted",
        "data": {"uid": str(book.uid)}
    })
    return 

@app.get("/api/users", response_model=List[UserModel])
def get_enrolled_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_uid}", response_model=UserModel)
def get_enrolled_user(user_uid: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uid == user_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)