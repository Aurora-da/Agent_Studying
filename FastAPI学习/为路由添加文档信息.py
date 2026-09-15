from typing import Annotated
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

# 自定义 API 文档信息
app = FastAPI(
    title="我的API",
    description="示例API",
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name":"开发者",
        "url":"http://example.com/contact/",
        "email":"dev@example.com",
    },
    license_info={
        "name":"MIT",
        "url":"https://opensource.org/licenses/MIT",
    },
    docs_url=None,  # 如果这个值等于None的话就相当于禁用交互式api文档
    redoc_url=None,
)

# 定义请求体数据模型
class Item(BaseModel):
    name: str                           # 商品名称
    description: str | None = None      # 商品描述
    price: float                   # 商品价格
    tax: float | None = None       # 税费

@app.get(
    "/items/{item_id}",
    summary="获取商品信息",                   # 路由的简短摘要
    description="根据商品ID获取商品的详细信息",  # 路由的详细描述
    response_description="商品信息对象",      # 响应的描述
    tags=["商品管理"]                        # 路由的分组
)
async def read_item(
    item_id: Annotated[int, Path(ge=1, description="商品ID")],
    q: Annotated[str| None, Query(description="搜索关键词")]=None,
):
    """获取商品信息

    :param item_id: 商品唯一的标识符
    :param q: 可选的搜索关键词
    :return:
    """
    return {"item_id": item_id, "q": q}
