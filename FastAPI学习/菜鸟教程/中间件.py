import time
import logging
from fastapi import FastAPI, Request
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# —————————————————————————————————— 创建中间件 ——————————————————————————————————
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

# —————————————————————————————————— 请求日志中间件 ————————————————————————————————————
logger = logging.getLogger("uvicorn.access")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"请求: {request.method} {request.url}")

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"响应：{request.method} {request.url}",
        f"状态码={response.status_code} 耗时={process_time}",
    )

    return response

# —————————————————————————————————— 使用Starlette内置中间件 ————————————————————————————————————
app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/items/")
async def root():
    return {"message": "使用 HTTPS 访问"}