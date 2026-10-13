from enum import Enum
from fastapi import FastAPI

# 创建枚举类，继承  str 和 Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # 可以与枚举成员比较
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message":"Deep Learning FWT!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}