import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Literal, Optional

app = FastAPI()

BOOKS_FILE = "books.json"
BOOKS = {}

if os.path.exists(BOOKS_FILE) and os.path.getsize(BOOKS_FILE) > 0:
    with open(BOOKS_FILE) as f:
        BOOKS = json.load(f)
else:
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOKS, f)


class Book(BaseModel):
    title: str
    author: str
    genre: Literal["fantasy", "mystery", "romance", "scifi", "thriller",
                   "western", "biography", "history", "poetry", "nonfiction", "fiction"]
    price: float
    year: int
    book_id: UUID = Field(default_factory=uuid4)


@app.get("/")
def root():
    return {"Welcome to the virtual bookstore app!"}


@app.get("/random")
def random():
    return random.choice(BOOKS)


@app.get("/list-books")
def list_books():
    return {"books": BOOKS}


@app.get("/book_by_index/{index}")
def get_book_by_id(index: int):
    if index < len(BOOKS):
        return BOOKS[index]
    else:
        raise HTTPException(
            status_code=404, detail="No book found with that id.")


@app.post("/add-book")
def add_book(book: Book):
    book_id = uuid4().hex
    book.book_id = uuid4().hex
    BOOKS[book_id] = book.model_dump()

    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOKS, f)
    return {"Book added successfully! Book id: " + book.book_id}


@app.delete("/delete-book/{book_id}")
def delete_book(book_id: str):
    if book_id in BOOKS:
        del BOOKS[book_id]
        with open(BOOKS_FILE, "w") as f:
            json.dump(BOOKS, f)
        return {"Book deleted successfully!"}
    else:
        raise HTTPException(
            status_code=404, detail="No book found with that id.")


@app.put("/update-book/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id in BOOKS:
        BOOKS[book_id].update(book.model_dump())
        with open(BOOKS_FILE, "w") as f:
            json.dump(BOOKS, f)
    return {"Book updated successfully!"}

    raise HTTPException(status_code=404, detail="No book found with that id.")


@app.get("/book_by_id/{book_id}")
def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.book_id == book_id:
            return book

    raise HTTPException(status_code=404, detail="No book found with that id.")
