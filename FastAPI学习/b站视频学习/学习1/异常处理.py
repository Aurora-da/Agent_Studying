from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{id}")
async def get_user(id: int):
    if id<1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": id}