from fastapi import FastAPI, Query, Depends


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 中间件，负责控制全局代码
@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 开始执行")
    response = await call_next(request)
    print("中间件1 结束")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 开始")
    response = await call_next(request)
    print("中间件2 结束")
    return response


# 依赖注入，只控制程序员指定的代码片段
async def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    return {"skip": skip, "limit": limit}

@app.get("/news/news_list")
async def get_news(commons = Depends(common_parameters)):
    return commons

@app.get("/users/users_list")
async def get_users(commons = Depends(common_parameters)):
    return commons