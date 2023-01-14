import network
import time
import socket
from m5stack import *
import machine as m
import co2lib as olympiade
import gc

SERVER_RUNNING = False
server = network.WLAN(network.AP_IF)#Initialise le point d'accès
server.active(True)
SERVER_RUNNING = True
server.ifconfig(('192.168.1.1', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
server.config(essid='Olympiade')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 80))
server_socket.listen(8)

sensor_list = []

while SERVER_RUNNING:
    try:
        conn, addr = server_socket.accept()
        request = conn.recv(1024)
        request = str(request.decode())
        splited_request = request.split('/')
        splited_request = splited_request[1].split(' ')[0]
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        
        olympiade.handler(splited_request, conn, sensor_list)
        
    except OSError as err:
        print(err)
        speaker.volume(0.5)
        speaker.tone(freq= 440,duration=1000)
        continue
    finally:
        conn.close()

