from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID


class Book(BaseModel):
    id: UUID
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str

