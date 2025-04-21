from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.schemas import BookCreate, BookUpdate
from sqlmodel import select, desc

class BookService():

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()


    async def get_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).filter(Book.id == book_id)
        result = await session.exec(statement)
        return result.first()
    

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book

        

    async def update_book(self, book_id: str, book_data: BookUpdate, session: AsyncSession):
        book = await self.get_book(book_id, session)
        if not book:
            return None
    
        update_data_dict = book_data.model_dump()
        
        for k, v in update_data_dict.items():
            setattr(book, k, v)

        await session.commit()

        return book

    async def delete_book(self, book_id: str, session: AsyncSession):
        book = await self.get_book(book_id, session)
        if not book:
            return
        
        await session.delete(book)
        await session.commit()
        return book