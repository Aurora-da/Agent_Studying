from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 基础模型
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None

# 创建用户时的输出模型 （包含密码）
class UserCreate(UserBase):
    password: str

# 返回用户信息时的输出模型（不包含密码）
class UserOut(UserBase):
    id: int

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump(exclude={"password"})}