from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/items/")
async def read_items(
    skip: int = 0,
    limit: int = 10,
    x_token: Annotated[str |None, Header()] = None,
):
    return {"skip": skip, "limit": limit, "x_token": x_token}

client = TestClient(app)

# 测试查询参数
def test_read_items_with_params():
    response = client.get("/items/?skip=5&limit=20")
    assert response.status_code == 200
    assert response.json() == {"skip": 5, "limit": 20, "x_token": None}


# 测试请求头
def test_read_items_with_header():
    response = client.get(
        "/items/",
        headers={"X-Token": "fake-token"},  # 发送自定义请求头
    )
    assert response.status_code == 200
    assert response.json()["x_token"] == "fake-token"