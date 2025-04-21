from fastapi import FastAPI
from src.books.routes import router as book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield 
    print(f"Server has been stopped")


version = "v1"

app = FastAPI(version=version, title="Books Backend", description="A REST API for book web service.", lifespan=life_span)


@app.get("/")
async def get_root():
    return {"message": "Backend running!!!"}


app.include_router(book_router)

