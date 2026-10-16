from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Books(BaseModel):
    title: str = Field(..., min_length=2, max_length=20, description="图书名称，长度为2到20")
    author: str = Field(min_length=2, max_length=20)
    publisher: str = Field("人民出版社")
    price: float | int = Field(..., gt=0)

@app.post("/books")
async def create_books(books: Books):
    return books
