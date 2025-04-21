from sqlmodel import SQLModel, Field
from datetime import datetime, date
from uuid import UUID, uuid4


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    def __repr__(self):
        return f"<Book {self.title}, Author: {self.author}>"

