from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI
import json

app = FastAPI()

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    # JSON 序列化配置
    class Config:
        # 允许使用字段别名
        allow_population_by_field_name = True
        # JSON 编码器
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class APIResponse(BaseModel):
    """标准 API 响应格式"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[dict] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# 分页响应格式
class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int

def get_users_paginated():
    pass

def count_users():
    pass

@app.get("/users", response_model=PaginatedResponse)
async def get_users(page: int = 1, size: int = 10):
    """返回分页的用户列表"""
    users = get_users_paginated(page, size)
    total = count_users()

    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=(total+size-1)//size
    )