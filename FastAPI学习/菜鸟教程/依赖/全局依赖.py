from fastapi import Depends, FastAPI, Header, HTTPException

async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secert-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# 全局依赖：所有路由都需要通过 token 检验
app = FastAPI(dependencies=[Depends(verify_token)])

@app.get("/items/")
async def read_items():
    return [{"item": "Foo"}]

@app.get("/users/")
async def read_users():
    return [{"user": "Bar"}]