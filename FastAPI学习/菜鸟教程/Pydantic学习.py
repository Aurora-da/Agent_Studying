from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()

class Item(BaseModel):
    name: str                       # 商品名称（必填）
    description: str | None = None  # 商品描述
    price: float                # 商品价格（必填）
    tax: float | None = None    # 税费

    model_config = ConfigDict(
        json_schema_extra={     # 在API文档中显示示例
            "examples": [
                {
                    "name": "apple",
                    "description": "Fruit",
                    "price": 5.00,
                    "tax": 0.00
                }
            ]
        }
    )
"""
字段是否必填取决于是否有默认值，有默认值则是非必填，没有默认值则是必填
"""

@app.post("/items/")
async def create_item(item: Item):
    """访问和操作模型数据

    :param item:
    :return:
    """
    # 访问模型数据
    print(item.name)
    print(item.price)

    # 序列化为字典
    item_dict = item.model_dump()
    print(item_dict)

    # 序列化为JSON字符串
    item_json = item.model_dump_json()
    print(item_json)

    return item_dict