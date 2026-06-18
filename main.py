from typing import Any

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="Library Book Storage API")


class Book(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int = Field(..., ge=0)
    available: bool = True


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int = Field(..., ge=0)
    available: bool = True


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    author: str | None = Field(default=None, min_length=1)
    year: int | None = Field(default=None, ge=0)
    available: bool | None = None


# In-memory storage. Restarting the app resets this data.
books_db: dict[int, Book] = {
    1: Book(id=1, title="Clean Code", author="Robert C. Martin", year=2008, available=True),
    2: Book(id=2, title="The Pragmatic Programmer", author="Andy Hunt", year=1999, available=False),
}
next_book_id = 3


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Library Book Storage API is running"}


@app.get("/books", response_model=list[Book])
def list_books() -> list[Book]:
    return list(books_db.values())


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> Book:
    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate) -> Book:
    global next_book_id

    book = Book(id=next_book_id, **payload.model_dump())
    books_db[next_book_id] = book
    next_book_id += 1
    return book


@app.put("/books/{book_id}", response_model=Book)
def replace_book(book_id: int, payload: BookCreate) -> Book:
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    updated_book = Book(id=book_id, **payload.model_dump())
    books_db[book_id] = updated_book
    return updated_book


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate) -> Book:
    existing = books_db.get(book_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    patch_data: dict[str, Any] = payload.model_dump(exclude_unset=True)
    merged = existing.model_copy(update=patch_data)
    books_db[book_id] = merged
    return merged


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> Response:
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    del books_db[book_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
