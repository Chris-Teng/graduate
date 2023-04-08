import cv2,threading,requests,subprocess

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
def compareFace():
    headers = {
    "x-api-key": "80dc6f1b-9968-42f2-8660-167549ca28fc",
    }
    files = {'file': open('tmp.jpg','rb')}
    r = requests.post('http://localhost:8000/api/v1/recognition/recognize', files=files,headers=headers)
    if 'No face' in r.text:
        return 2
    result = r.json()['result']
    for person in result:
        if person['subjects'][0]['similarity'] < 0.97:
            return 1
    return 0
    
class RTSCapture(cv2.VideoCapture):
    _cur_frame = None
    _reading = False
    schemes = ["rtsp://","rtmp://"]
    @staticmethod
    def create(url, *schemes):
        rtscap = RTSCapture(url)
        rtscap.frame_receiver = threading.Thread(target=rtscap.recv_frame, daemon=True)
        rtscap.schemes.extend(schemes)
        if isinstance(url, str) and url.startswith(tuple(rtscap.schemes)):
            rtscap._reading = True
        elif isinstance(url, int):
            pass
        return rtscap

    def isStarted(self):
        ok = self.isOpened()
        if ok and self._reading:
            ok = self.frame_receiver.is_alive()
        return ok

    def recv_frame(self):
        while self._reading and self.isOpened():
            ok, frame = self.read()
            if not ok: break
            self._cur_frame = frame
        self._reading = False

    def read2(self):
        frame = self._cur_frame
        self._cur_frame = None
        return frame is not None, frame

    def start_read(self):
        self.frame_receiver.start()
        self.read_latest_frame = self.read2 if self._reading else self.read

    def stop_read(self):
        self._reading = False
        if self.frame_receiver.is_alive(): self.frame_receiver.join()

frame_count = 0
rtscap = RTSCapture.create('rtsp://192.168.1.110:8554/live')
rtscap.start_read()
while rtscap.isStarted():
    ok, frame = rtscap.read_latest_frame()
    if frame is None or not ok:
        continue
    if frame_count % 50 == 0:
        cv2.imwrite('tmp.jpg', frame)
        result = subprocess.getoutput("yolo detect predict model=yolov8n.pt source='tmp.jpg'")
        if "person" in result:
            recg = compareFace()
            if recg == 0:
                print('欢迎')
            elif recg == 1:
                pushAlert('未知人员闯入')
            else:
                print('未检测到人脸')
            with open('someone','w')as f:
                f.write('1')
        elif "Fall" in result:
            pushAlert('家里有人摔倒')
        elif "Fire" in result:
            pushAlert('家里可能着火')
            with open('onfire','w')as f:
                f.write('1')
        else:
            print('Normal')
            with open('onfire','w')as f:
                f.write('0')
            with open('someone','w')as f:
                f.write('0')
    frame_count += 1
rtscap.stop_read()
rtscap.release()
cv2.destroyAllWindows()