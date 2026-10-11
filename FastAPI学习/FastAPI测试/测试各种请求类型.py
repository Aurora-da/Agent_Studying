from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float | int

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "name": item.name}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"deleted": item_id}

client = TestClient(app)

def test_create_time():
    response = client.post(
        "/items",
        json={"name": "Bar", "price": 50.0},
    )
    assert response.status_code == 200

def test_update_time():
    response = client.put(
        "/items/1",
        json={"name": "Bar", "price": 50.0}
    )
    assert response.status_code == 200

def test_delete_time():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"deleted": 1}