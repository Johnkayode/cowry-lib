# Project

This project is a simple **Library Management System** built with two independent API services: **Core (Frontend)** and **Admin**. These services communicate via **RabbitMQ** for event-driven updates and synchronization.

## Architecture Overview

The system consists of two services:

- **Core (Frontend)**: Allows users to enroll, view available books, and borrow books.
- **Admin**: Enables admins to manage the book catalog and retrieve information about users and borrowed books.

---

## Services

### Core (Frontend) API
- **Framework**: Python/Django
- **Database**: PostgreSQL
- **Description**: This service manages user enrollment, browsing the book catalog, and borrowing books.

#### Endpoints:
- **Enrol User**: `POST /api/users/enrol/`
  - Request Body:
    ```json
    { 
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```
- **List and Filter Available Books**: `GET /api/books?publisher=?category=`
  - Query Parameters: `publisher`, `category`, `author`
- **Retrieve a Single Book**: `GET /api/books/<book_uid>/`
- **Borrow Book**: `POST /api/books/<book_uid>/borrow/`
  - Request Body:
    ```json
    { 
      "user": "user-uid",
      "period": 7 
    }
    ```

### Admin API
- **Framework**: Python/FastAPI
- **Database**: PostgreSQL
- **Description**: This service allows admins to manage the book catalog, view enrolled users, and see which books have been borrowed.

#### Endpoints:
- **Create Book**: `POST /api/books`
  - Request Body:
    ```json
    { 
      "title": "Book Title",
      "publisher": "Publisher Name",
      "category": "Fiction",
      "author": "Author Name",
    }
    ```
- **Remove Book**: `DELETE /api/books/<book_id>`
- **Get Enrolled Users**: `GET /api/users`
- **Retrieve Unavailable Books**: `GET /api/books/unavailable`

---

## Models

### User
Represents a user who can enroll and borrow books.
- **Fields**:
  - `email`: User’s email (unique)
  - `first_name`: First name
  - `last_name`: Last name

### Book
Represents a book in the library catalog.
- **Fields**:
  - `title`: The title of the book.
  - `publisher`: Publisher name.
  - `category`: Book category. 
  - `author`: Book's author.

### BookBorrowRequest
Book borrow requests from users
- **Fields**:
  - `book`: Reference to the `Book`
  - `user`: Reference to the `User`
  - `request_date`: Date when the borrow request was made
  - `period`: The borrowing period in days

---

## Messaging - RabbitMQ Events

The system uses **RabbitMQ** to handle communication between the Core (Frontend) and Admin services. The following events are supported:

- `user_enrolled` (Core -> Admin): Triggered when a user enrolls in the system.
- `book_created` (Admin -> Core): Triggered when a new book is added via the Admin service.
- `book_deleted` (Admin -> Core): Triggered when a book is removed via the Admin service.
- `book_borrowed` (Core -> Admin): Triggered when a book is borrowed via the Core service.

---

## Setup and Installation

1. Ensure Docker is installed on your machine.
2. Clone the repository:
    ```bash
    git clone https://github.com/johnkayode/cowry-lib.git
    cd cowry-lib
    ```
3. Build and run the services:
    ```bash
    docker-compose up --build
    ```
3. The services will be available at:
    - **Core**: `http://localhost:8000`
    - **Admin**: `http://localhost:8001`
    - **RabbitMQ Management**: `http://localhost:15672`
---

## Testing

Unit and integration tests are included in both services. You can run tests using:

- **Core** (Django):
  ```bash
  python manage.py test api/apps
- **Admin** (Django):
  ```bash
  pytest
