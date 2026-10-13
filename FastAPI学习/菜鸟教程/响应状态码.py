from fastapi import FastAPI, status

app = FastAPI()

# —————————————————————————————————— 使用 status 常量 ————————————————————————————————
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    pass

# GET - 获取资源，默认返回200
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

