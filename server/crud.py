from sqlalchemy.orm import Session

from . import models

# 记录温度
def add_tempe(db: Session, tempe: int):
    db_tempe = models.Temperature(tem=tempe)
    db.add(db_tempe)
    db.commit()
    db.refresh(db_tempe)
    return db_tempe
# 记录每日报警数
def add_alert_num(db: Session, num: int):
    db_alert = models.AlertNum(count=num)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert
# 改变有人、着火状态
def change_status(db: Session, issomeone: bool, isonfire: bool):
    db_status = models.securityStatus(someone=issomeone,onfire=isonfire)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status
# 记录人脸识别日志
def add_record(db: Session, face: str,time: str):
    db_record = models.faceRecord(face=face,time=time)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_tempe(db: Session):
    return db.query(models.Temperature).limit(30).all()

def get_alert_num(db: Session):
    return db.query(models.AlertNum).limit(30).all()

def get_security_status(db: Session):
    return db.query(models.securityStatus).order_by(models.securityStatus.id.desc()).first()
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()