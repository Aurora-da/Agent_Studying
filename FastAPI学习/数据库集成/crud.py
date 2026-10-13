from sqlalchemy.orm import Session
import models, schemas


def get_user(db: Session, user_id: int):
    """根据 ID 获取用户"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """根据邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """获取用户列表"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """创建用户"""
    fake_hashed_password = user.password + "notreallyhashed"  # 实际应使用 passlib 哈希
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()        # 提交事务
    db.refresh(db_user)  # 刷新对象，获取数据库生成的 id
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """获取商品列表"""
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """创建商品"""
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item