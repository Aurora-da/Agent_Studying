from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id")
async def read_items(
    # Path 表示这个形参的值来源于路径
    item_id: Annotated[int, Path(gt=0, le=1000)],
    # Query 表示这个形参的值来源于查询字符串，例如：?size=5.0
    size: Annotated[float, Query(gt=0, lt=10.5)] = 5.0,
):
    return {"item_id": item_id, "size": size}

