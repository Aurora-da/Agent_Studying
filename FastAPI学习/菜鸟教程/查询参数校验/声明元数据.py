from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(
        title="查询字符串",
        description="用于筛选商品的查询字符串",
        min_length=3,
        max_length=50,
        alias="item-query",
        deprecated=True,
    )] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results