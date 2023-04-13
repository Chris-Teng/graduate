from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import requests,uvicorn

from server import crud, models
from server.database import SessionLocal, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

welcomeStatus = {
    'temperature': str,
    'humidity': str,
    'isThereSomeone': bool,
    'onFire': bool,
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/welcome/tempdata')
def read_tempdata(db: Session = Depends(get_db)):
    tempData = crud.get_tempe(db)
    return tempData

@app.get('/welcome/alertdata')
def read_alertdata(db: Session = Depends(get_db)):
    alertData = crud.get_alert_num(db)
    return alertData


@app.get("/welcome/Status")
def read_status(db: Session = Depends(get_db)):
    status = crud.get_security_status(db)
    r = requests.get('https://www.yiketianqi.com/free/day?appid=58594862&appsecret=r75QnFGN&unescape=1') 
    welcomeStatus['temperature'] = r.json()['tem']
    welcomeStatus['humidity'] = r.json()['humidity']
    welcomeStatus['isThereSomeone'] = status.someone
    welcomeStatus['onFire'] = status.onfire
    
    return {"temperature": welcomeStatus['temperature'], 'humidity': welcomeStatus['humidity'], 'isThereSomeone': welcomeStatus['isThereSomeone'], 'onFire': welcomeStatus['onFire']}

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8001, reload=True)