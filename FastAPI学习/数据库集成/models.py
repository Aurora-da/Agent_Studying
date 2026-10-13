from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"  # 表名

    id = Column(Integer, primary_key=True, index=True)  # 主键，自增
    email = Column(String, unique=True, index=True)      # 唯一，建索引
    hashed_password = Column(String)                      # 哈希密码
    is_active = Column(Boolean, default=True)             # 是否活跃


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)                   # 标题，建索引
    description = Column(String)                          # 描述
    owner_id = Column(Integer, ForeignKey("users.id"))   # 外键关联 users 表