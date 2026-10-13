from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

items = {"Foo": "The Foo Wrestlers", "bar": "The Bar Fighters"}

# —————————————————————————— 使用HTTPException来返回错误响应 ————————————————————————————
@app.get("/items1/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# —————————————————————————— 自定义错误详情 ————————————————————————————
@app.get("/items2/{item_id}")
async def read_item(item_id: str):
    if item_id == "invalid":
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INVALID_ID",
                "message": "商品ID格式不正确",
                "hint": "请使用字母数字组合的ID",
            }
        )
    return {"item_id": item_id}

# —————————————————————————— 添加自定义相应头 ————————————————————————————
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id == "invalid":
        raise HTTPException(
            status_code = 404,
            detail = "Item not found",
            headers = {"X-Error": "There goes my error"},
        )
    return {"item_id": item_id}

# —————————————————————————— 自定义异常处理器 ————————————————————————————
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong"},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# —————————————————————————— 覆盖默认异常处理器 ————————————————————————————
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {"error": f"HTTP error: {exc.detail}"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "数据校验失败", "details": exc.errors()},
    )

# —————————————————————————— 重定向 ————————————————————————————
@app.get("/items3/")
async def read_items():
    return {"items": ["foo", "bar"]}

@app.get("/redirect")
async def redirect():
    return RedirectResponse(url="/items3/")

# —————————————————————————— 自定义响应头和状态码 ————————————————————————————
@app.get("/item4/{item_id}")
async def read_item(item_id: int):
    content = {"item_id": item_id}
    headers = {"X-Custom-Header": "custom-header-value"}
    return JSONResponse(content=content, headers=headers)