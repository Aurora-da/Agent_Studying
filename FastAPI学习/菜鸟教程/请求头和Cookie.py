from fastapi import FastAPI, Header, Cookie, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI()

@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"user_agent": user_agent, "session_token": session_token}

@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/items/")

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    content = {"item_id": item_id}
    headers = {"X-Custom-Header": "custom-header-value"}
    return JSONResponse(content=content, headers=headers)