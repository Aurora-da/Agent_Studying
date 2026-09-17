from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

# ———————————————————————————— 类作为依赖 ————————————————————————————————
# 用类声明依赖
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# 使用类作为依赖
@app.get("/items/1/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}

# —————————————————————————————— 普通类型的依赖 ——————————————————————————————————————
# 定义依赖函数
def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 在路由中使用依赖
@app.get("/items/2/")
async def read_items(commons: dict = Depends(common_parameters)):
    # commons接收依赖函数的返回值
    return commons

@app.get("/users/1")
async def read_users(commons: dict = Depends(common_parameters)):
    # 多个路由可以复用同一个依赖
    return commons

# —————————————————————————————— 子依赖 ——————————————————————————————————————
# 依赖函数
def query_extractor(q: str | None = None):
    return q

# 子依赖
def query_checker(q: str = Depends(query_extractor)):
    if q == "admin":
        return q + " (checked)"
    return q

# 路由使用子依赖
@app.get("/items/3/")
async def read_items(q: str = Depends(query_checker)):
    return {"q": q}

# —————————————————————————————— 在装饰器中使用依赖 ——————————————————————————————————
async def verify_api_key(x_api_key: str = Header()):
    if x_api_key != "secret-key":
        raise HTTPException(status_code=400, detail="X-API-Key invalid")

@app.get("/items/3/", dependencies=[Depends(verify_api_key)])
async def read_items():
    return [{"item": "Foo"}]

@app.get("/users/2/", dependencies=[Depends(verify_api_key)])
async def read_users():
    return [{"user": "Bar"}]
