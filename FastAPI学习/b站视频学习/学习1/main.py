from fastapi import FastAPI, Path, Query
from typing import Annotated
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def root():
    return  {"message": "你好！"}


@app.get("/hello")
async def hello():
    return {"msg": "你好FastAPI"}


@app.get("/user/hello")
async def user_hello():
    return {"msg": "我正在学习FastAPI..."}


# =========== 带路径参数的路由 ===========
@app.get("/user1/{id}")
async def user_id_get(id: int = Path(..., gt=0, le=10000, description="用来记录用户的id，取值范围是1-10000")):
    return {"id": id, "info": f"您是第{id}位用户"}

@app.get("/user2/{name}")
async def user_name_get(
    name: Annotated[str, Path(min_length=1, max_length=20, description="用户的名称，长度范围为1-20")],
):
    return {"name": name}


# ============ 查询参数 ============
@app.get("/books/book1")
async def user3_get(
    title: Annotated[str, Query(min_length=1, max_length=10, description="书的名称")],
    description: Annotated[str, Query(min_length=1, max_length=20, description="书的概述")],
):
    return {"title": title, "description": description}


# ============ 请求体参数 =============
class User(BaseModel):
    id: int
    user_name: str
    password: str

@app.post("/register")
async def register(user: User):
    return user

class Book(BaseModel):
    title: str
    author: str
    description: str

@app.post("/post_book")
async def post_book(book: Book):
    return book