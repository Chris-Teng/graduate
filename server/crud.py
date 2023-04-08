from sqlalchemy.orm import Session

from . import models


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def add_tempe(db: Session, tempe: int):
    db_tempe = models.Temperature(tem=tempe)
    db.add(db_tempe)
    db.commit()
    db.refresh(db_tempe)
    return db_tempe


def add_alert_num(db: Session, num: int):
    db_alert = models.AlertNum(count=num)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_tempe(db: Session):
    return db.query(models.Temperature).limit(30).all()


def get_alert_num(db: Session):
    return db.query(models.AlertNum).limit(30).all()
