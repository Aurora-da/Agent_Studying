from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# —————————————————————————————— 使用返回类型注解 ————————————————————————————————————————
class Item(BaseModel):
    name: str = Field(min_length=1, max_length=20, description="商品名称")
    description: Annotated[str | None, Field(default=None, max_length=200, description="商品描述")]
    price: float| int

# 通过声明响应模型，FastAPI 会自动完成输出数据的校验、序列化和过滤，确保客户端只接收到预期的数据。
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return {
        "name": "Foo",
        "description": "A very nice item",
        "price": 2.22,
        "secret": "this should not be visible",  # 不在 Item 中的字段会被过滤
    }

# —————————————————————————————— 返回类型与数据过滤 ————————————————————————————————————————
class BaseUser(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=20, description="用户姓名")]
    email: EmailStr

# 输入模型
class UserIn(BaseUser):
    password: str = Field(min_length=6, max_length=20, description="登入密码")

@app.post("/users/")
async def create_user(user: UserIn) -> BaseUser:
    return user