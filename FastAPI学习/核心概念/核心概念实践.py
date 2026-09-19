from fastapi import FastAPI, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import asyncio

app = FastAPI(
    title="博客 API",
    description = "展示 FastAPI 核心概念的博客系统",
    version="0.1"
)

# 数据模型
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    published: bool = Field(True)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 模拟数据库
posts_db = []
next_id = 1

# 依赖：获取当前用户(简化版)
async def get_current_user() -> int:
    return 1

@app.get("/posts", response_model=List[PostResponse], tags=["文章"])
async def list_posts(
    skip: int = Query(0, ge=0, description="跳过的文章数"),
    limit: int = Query(10, ge=1, le=100, description="返回的文章数"),
    published_only: bool = Query(True, description="只返回已经发布的文章")
):
    """
   获取文章列表

   支持分页和筛选功能
   """
    # 模拟异步数据库查询
    await asyncio.sleep(0.1)

    filtered_posts = posts_db
    if published_only:
        filtered_posts = [p for p in posts_db if p["published"]]

    return filtered_posts[skip:skip + limit]


@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED, tags=["文章"])
async def create_post(
        post: PostCreate,
        current_user_id: int = Depends(get_current_user)
):
    """
    创建新文章

    需要用户认证
    """
    global next_id

    # 模拟异步数据库操作
    await asyncio.sleep(0.1)

    new_post = {
        "id": next_id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "author_id": current_user_id,
        "created_at": datetime.now(),
        "updated_at": None
    }

    posts_db.append(new_post)
    next_id += 1

    return new_post


@app.get("/posts/{post_id}", response_model=PostResponse, tags=["文章"])
async def get_post(post_id: int):
    """
    获取特定文章

    根据文章 ID 返回文章详情
    """
    # 模拟异步数据库查询
    await asyncio.sleep(0.1)

    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post


# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "posts_count": len(posts_db)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)