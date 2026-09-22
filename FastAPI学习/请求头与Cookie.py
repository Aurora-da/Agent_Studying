from typing import Annotated
from fastapi import FastAPI, Header, Cookie

app = FastAPI()

@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None,
    session_token: Annotated[str | None, Cookie()] = None,
    ads_id: Annotated[str | None, Cookie()] = None,
):
    return {
        "User_Agent": user_agent,
        "Session-Token": session_token,
        "Ads-ID": ads_id,
    }