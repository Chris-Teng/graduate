from machine import ADC,Pin
import time,network,urequests

DO = Pin(15,Pin.OUT)
AO = ADC(Pin(32),atten=ADC.ATTN_11DB)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to wifi...')
        wlan.connect('NFPC-QXGA', 'police110')
    print('network config:', wlan.ifconfig())

do_connect()
time.sleep(20)
pushed = 0
while True:
    smoke_value = AO.read()
    print(smoke_value,DO.value())
    if (DO.value()==0 or smoke_value>1000) and pushed==0:
        r = urequests.get('http://192.168.3.35:8001/smokealert/'+str(smoke_value))
        print(r.text)
        pushed = 10
    elif pushed > 0:
        pushed -= 1
    time.sleep(3)