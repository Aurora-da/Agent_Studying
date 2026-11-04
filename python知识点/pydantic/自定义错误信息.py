from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    name: str
    age: int

    class Config:
        error_msg_templates = {
            'value_error.any_str.max_length': '字符串长度不能超过 {limit_value} 个字符',
            'value_error.any_str.min_length': '字符串长度不能少于 {limit_value} 个字符'
        }

    """
    field_validator: 用于单个字段的检验，可选mode=before/after
    - before：在 Pydantic 类型转换之前跑（原始输入）
    - after：在类型转好之后跑（推荐，类型安全）
    
    为何要加@classmethod：@field_validator 在Pydantic v2里要求这个校验函数必须是类方法，所以要加这个装饰器。
    """
    @field_validator('name', mode="after")
    @classmethod
    def name_length(cls, v):
        if len(v) > 50:
            raise ValueError("name too long, please retry it.")
        return v