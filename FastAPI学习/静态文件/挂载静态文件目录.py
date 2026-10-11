from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 挂载静态文件目录
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}