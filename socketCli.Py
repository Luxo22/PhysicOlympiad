import socket
import network
import time
from m5stack import *
from m5ui import *

nic = network.WLAN(network.STA_IF) #crée l'interface station
nic.active(True) #Active le wifi
# Create a TCP/IP socket

def getId():
    file = open('clientId.key', 'r')
    clientId = file.read()
    file.close()
    return clientId

selfId = getId()

def connectToWifi(wifiname='Olympiade', password=''):
    lcd.clear()
    wifiList = nic.scan()
    for wifi in wifiList:
        wifiName = wifi[0].decode()
        lcd.print(wifiName)
        print(wifi)
        if wifiname == wifiName:
            nic.connect(wifiname, password)
            while nic.isconnected() != True:
                lcd.clear()
                lcd.println('Connexion en cours - ' + wifiname)
                time.sleep(1)
            lcd.clear()
            lcd.println('Connexion avec le serveur établie')
            break

def sendDataToServer(rate = 0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = ('192.168.1.1', 80)
    print('Connecting to {}:{}'.format(*server_address))
    sock.connect(server_address)
    try:
        api_endpoint = '/api'
        message = b'your data here'
        data = 'GET {}?rate={}-id={} HTTP/1.1\r\nHost: 192.168.1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n'.format(api_endpoint, rate, selfId, 256).encode()
        sock.sendall(data)
    finally:
        # Clean up the connection
        sock.close()

buttonA.wasPressed(connectToWifi)

import utime
import machine as m

def getCO2(timer):
    uart2.write(co2_cmd)
    utime.sleep_ms(100)
    res = uart2.read(7)
    high = res[3]
    low = res[4]
    co2 = (high*256)+low
    draw(co2)
    sendDataToServer(co2)

def draw(RATE):
    lcd.clear()
    updatedVar = _Update(RATE)
    lcd.font(lcd.FONT_DejaVu24)
    lcd.text(150,150, str(RATE))

    lcd.rect(110,16,20,288,0xFFFFFF, 0xFFFFFF)
    lcd.rect(100,110,40,3, 0XF8D800, 0XF8D800)#ORANGE INDICATOR
    lcd.rect(100,137,40,3, 0XEA5455, 0XEA5455)

    lcd.rect(110,16,20, updatedVar[0],updatedVar[1] , updatedVar[1])

def _Update(N):
    color = "0X28C76F"
    number = int(288*N/3000)
    if N > 1000 and N < 1300:
        color = 0XF8D800

    elif N >= 1300:
        #speaker.tone(freq= 440,duration=1000)
        color = 0XEA5455

    if number >= 288:
        number = 288

    return [int(number), int(color)]



speaker.volume(0.1)
lcd.setRotation(2)

uart2 = machine.UART(2, tx=17, rx=16)
uart2.init(9600, bits=8, parity=None, stop=1, timeout=3000)
utime.sleep(1)
co2_cmd = b'\xFE\x44\x00\x08\x02\x9F\x25'

timer = m.Timer(2)

def start():
    global t0
    t0 = utime.ticks_ms()
    timer.init(period=5000, mode=timer.PERIODIC, callback=getCO2)
    speaker.tone(freq=300, duration=1000)
    
def stop():
    timer.deinit()
    speaker.tone(freq=500, duration=1000)

buttonB.wasPressed(stop)
buttonC.wasPressed(start)
