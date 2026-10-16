from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

# 默认类型为json类型
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 相应类型为HTML类型
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一个标题</h1>"

# 相应类型为文件类型
@app.get("/file")
async def get_file():
    file_path = "1.png"
    return FileResponse(file_path, media_type="image/png")

# 自定义响应格式
class User(BaseModel):
    user_id: int = Field(..., gt=0, lt=100)
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=6, max_length=20)

@app.get("/user/{id}", response_model=User)
async def get_user(id: int):
    return {
        "user_id": id,
        "username": "张三",
        "password": "123123",
    }