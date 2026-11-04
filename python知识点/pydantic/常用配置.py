from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int

    class Config:
        allow_mutation = False      # 表示模型实例是不允许被修改的
        extra = 'forbid'            # 处理未定义的字段
        validate_all = True         # 所有字段在实例化时都会被验证

