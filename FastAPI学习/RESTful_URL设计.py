from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI(title = "User & Post API")

# —————————————————————— 数据模型 ————————————————————————————
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class Post(PostCreate):
    id: int
    user_id: int

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(UserBase):
    password: str = Field(..., min_length=6)

class UserPatch(BaseModel):
    """PATCH: 部分更新，所有字段可选"""
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class UserOut(UserBase):
    id: int
    posts: List[Post] = []

# —————————————————————————— 内存数据库 ——————————————————————
users_db: dict[int, dict] = {}
posts_db: dict[int, dict] = {}
_user_id_counter = 1
_post_id_counter = 1

# ——————————————————————————— 业务逻辑函数 ————————————————————————————
def find_user(user_id: int) -> dict:
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user

def _check_duplicate(username: str, email: str, exclude_id: Optional[int]=None):
    for uid, u in users_db.items():
        if uid == exclude_id:
            continue
        if u["username"] == username:
            raise HTTPException(400, f"Username '{username} already exists")
        if u["email"] == email:
            raise HTTPException(400, f"Email '{email}' already exists")

def create_new_user(user: UserCreate) -> dict:
    global _user_id_counter
    _check_duplicate(user.username, user.email)
    new_user = {
        "id": _user_id_counter,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "posts": [],
    }
    users_db[_user_id_counter] = new_user
    _user_id_counter += 1
    return new_user

def update_existing_user(user_id: int, user: UserUpdate) -> dict:
    existing = find_user(user_id)
    _check_duplicate(user.username, user.email, exclude_id=user_id)
    existing.update({
        "username": user.username,
        "email": user.email,
        "password": user.password,
    })
    return existing

def patch_existing_user(user_id: int, user: UserPatch) -> dict:
    existing = find_user(user_id)
    data = user.model_dump(exclude_unset=True)
    if "username" in data or "email" in data:
        _check_duplicate(
            data.get("username", existing["username"]),
            data.get("email", existing["email"]),
            exclude_id=user_id,
        )
    existing.update(data)
    return existing

def delete_existing_user(user_id: int) -> dict:
    find_user(user_id)
    deleted = users_db.pop(user_id)
    # 同时删除该用户的所有帖子
    for pid in [p["id"] for p in deleted["posts"]]:
        posts_db.pop(pid, None)
    return {"message": f"User {user_id} deleted", "user": deleted}

def get_posts_by_user(user_id: int) -> List[dict]:
    find_user(user_id)  # 确保用户存在
    return users_db[user_id]["posts"]

def create_post_for_user(user_id: int, post: PostCreate) -> dict:
    global _post_id_counter
    find_user(user_id)
    new_post = {
        "id": _post_id_counter,
        "user_id": user_id,
        "title": post.title,
        "content": post.content,
    }
    posts_db[_post_id_counter] = new_post
    users_db[user_id]["posts"].append(new_post)
    _post_id_counter += 1
    return new_post

# ———————————————————————————— 路由 ——————————————————————————————————
@app.get("/users", response_model=List[UserOut])
async def get_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return find_user(user_id)

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return create_new_user(user)

@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate):
    return update_existing_user(user_id, user)

@app.patch("/users/{user_id}", response_model=UserOut)
async def patch_user(user_id: int, user: UserPatch):
    return patch_existing_user(user_id, user)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return delete_existing_user(user_id)

@app.get("/users/{user_id}/posts", response_model=List[Post])
async def  get_users_posts(user_id: int):
    return get_posts_by_user(user_id)

@app.post("/users/{user_id}/posts",
          response_model=Post,
          status_code=status.HTTP_201_CREATED)
async def create_user_post(user_id: int, post: PostCreate):
    return create_post_for_user(user_id, post)