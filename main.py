from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import requests, uvicorn

from server import crud, models
from server.database import SessionLocal, engine
def pushAlert(m:str):
    headers = {
    "Content-Type":"application/json",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "PostmanRuntime/7.31.3",
    "Connection":"keep-alive"
    }

    msg = {"msgtype": "text","text": {"content":f"监控报警: {m}"}}

    # 发送请求
    x = requests.post('https://oapi.dingtalk.com/robot/send?access_token=506e02c8f76fc6feb75885e65c1e1b7909779999e20b0cd4b141e6813711048c', json=msg,headers=headers)
    print(x.text)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

welcomeStatus = {
    "temperature": str,
    "humidity": str,
    "isThereSomeone": bool,
    "onFire": bool,
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/welcome/tempdata")
def read_tempdata(db: Session = Depends(get_db)):
    tempData = crud.get_tempe(db)
    return tempData


@app.get("/welcome/alertdata")
def read_alertdata(db: Session = Depends(get_db)):
    alertData = crud.get_alert_num(db)
    return alertData


@app.get("/welcome/Status")
def read_status(db: Session = Depends(get_db)):
    status = crud.get_security_status(db)
    r = requests.get(
        "https://www.yiketianqi.com/free/day?appid=58594862&appsecret=r75QnFGN&unescape=1"
    )
    welcomeStatus["temperature"] = r.json()["tem"]
    welcomeStatus["humidity"] = r.json()["humidity"]
    welcomeStatus["isThereSomeone"] = status.someone
    welcomeStatus["onFire"] = status.onfire

    return {
        "temperature": welcomeStatus["temperature"],
        "humidity": welcomeStatus["humidity"],
        "isThereSomeone": welcomeStatus["isThereSomeone"],
        "onFire": welcomeStatus["onFire"],
    }


@app.get("/record")
def read_record(db: Session = Depends(get_db)):
    recordData = crud.get_record(db)
    return recordData

@app.get("/smokealert/{alert_value}")
def smoke_alert(alert_value: int):
    pushAlert('危险气体浓度超标！ '+str(alert_value))
    return 'ok '+str(alert_value)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8001, reload=True)
