from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.schemas import Book, BookCreate, BookUpdate
from typing import List
from src.db.main import get_session
from src.books.service import BookService

router = APIRouter(prefix="/api/books", tags=["books"])
book_service = BookService()


@router.get('/', response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_id, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return book


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BookCreate)
async def create_book(book_data: BookCreate, session: AsyncSession = Depends(get_session)) -> dict:
    created_book = await book_service.create_book(book_data, session)
    return created_book



@router.put("/update/{book_id}", response_model=BookUpdate)
async def update_book(book_id: str, book_data: BookUpdate, session: AsyncSession = Depends(get_session))->dict :
    updated_book = await book_service.update_book(book_id, book_data, session)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return updated_book


@router.delete("/delete/{book_id}", response_model=Book)
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    deleted_book = await book_service.delete_book(book_id, session)
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return deleted_book


