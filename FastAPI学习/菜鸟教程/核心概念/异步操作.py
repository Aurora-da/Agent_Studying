import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

# 同步路径操作
@app.get("/sync")
def sync_endpoint():
    time.sleep(2)
    return {"message": "同步响应"}

# 异步路径操作
@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(2)
    return {"message": "异步响应"}

# 异步数目库操作示例
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await datebase.fetch_one(
        "select * from users where id =: user_id",
        {"user_id": user_id}
    )
    return user