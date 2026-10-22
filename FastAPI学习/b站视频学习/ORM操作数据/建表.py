import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Path, Query, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, Float, String, func, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("环境变量 ASYNC_DATABASE_URL 未设置，请检查 .env")

# 创建异步引擎
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)


# ---------- ORM ----------
class Base(DeclarativeBase):
    pass


class TimestampMixin:
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="修改时间"
    )


class Book(Base, TimestampMixin):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(225), comment="书名")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(225), comment="出版社")


# ---------- Pydantic 响应模型 ----------
class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bookname: str
    price: float
    publisher: str
    create_time: datetime
    update_time: datetime


# ---------- 会话 & 依赖 ----------
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,     # 提交后会话不过期，防止重新查询数据库，节约资源
)


async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# ---------- 建表 ----------
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


# ---------- 路由 ----------
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/book/books", response_model=BookOut)
async def get_books(db: AsyncSession = Depends(get_database)):
    # result = await db.execute(select(Book))
    # return result.scalars().all()  获取所有数据
    # return result.scalars().first()     # 获取第一条数据
    book = await db.get(Book, 1)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# 模糊查询
@app.get("/book/search", response_model=list[BookOut])
async def select_book_by_publisher(
    publisher: str | None = Query(default=None, description="出版社模糊检索，包含该文字"),
    db: AsyncSession = Depends(get_database)
):
    stmt = select(Book)
    if publisher:
        # 包含匹配 %xxx%
        stmt = stmt.where(Book.publisher.like(func.concat("%", publisher, "%")))
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/book/{book_id}", response_model=BookOut)
async def get_particular_book(book_id: int, db: AsyncSession = Depends(get_database)):
    book = (await db.execute(select(Book).where(Book.id == book_id))).scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# 查询价格大于某个数值的所有物品
@app.get("/book/search_book/{designated_price}", response_model=list[BookOut])
async def get_search_book(
    designated_price: Annotated[float, Path(..., gt=0, le=5000)],
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.price>=designated_price))
    return result.scalars().all()