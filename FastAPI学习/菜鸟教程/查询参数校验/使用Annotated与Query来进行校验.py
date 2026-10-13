from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    # str | None 表示q可以是字符串或者None
    # Query中min_length表示最小长度，max_length表示最大长度，pattern表示正则表达式
    # = None 使参数变得可选
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results