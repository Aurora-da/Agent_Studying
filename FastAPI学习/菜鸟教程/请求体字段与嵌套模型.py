from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

# —————————————————————————— Field 字段 ————————————————————————————————————————
class Item(BaseModel):
    name : str = Field(min_length=1, max_length=100, description="商品名称")
    description: str | None = Field(default=None, max_length=300, description="商品描述")
    price: float = Field(gt=0, description="商品价格")
    tax: float | None = Field(default=None, ge=0, description="税费")

@app.get("/items/")
async def create_item(item: Item):
    return item

# ———————————————————————————— 嵌套模型 —————————————————————————————————————————
class Image(BaseModel):
    url: HttpUrl
    name : str

class Goods(BaseModel):
    name: str
    description: Annotated[str, Field(max_length=300, description="商品描述")]
    price: float
    tax: float | None
    tags: set[str] = set()          # 使用set对标签进行去重
    image: Image | None = None      # 可选的图片信息

@app.post("/goods/")
async def create_item(goods: Goods):
    return goods

# ———————————————————————————— 深度嵌套模型 ——————————————————————————————————————
# 对 Goods 再次进行一次嵌套
class Offer(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=20, description="姓名")]
    description: str | None = Field(default=None, max_length=200, description="描述")
    price: float
    items: list[Goods]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer