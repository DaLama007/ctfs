import requests
import json 
import socket 
import ssl
HOST = "10.83.12.242"
PORT = 80
PATH = "/api/bet"
SUFFIX = b'}'



headers_sent = False
suffix_sent = False
sock = socket.create_connection((HOST, PORT))
while (True):
    x = requests.get(f'http://{HOST}/api/state')
    time = x.json()['timer']
    print(time)
    if time<5:
        suffix_sent =False 
        headers_sent =False 
    if time>=28 and not headers_sent:
        points = str(x.json()['user_points'])
        PREFIX = b'{"amount":'+ points.encode() +b',"horse":'
        lengthCont = len(PREFIX) + 2 + len(SUFFIX)
        headers = (
            f"POST {PATH} HTTP/1.1\r\n"
                f"Host: {HOST}\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: {lengthCont}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
        ).encode()
        sock.sendall(headers+PREFIX)
        print("sent headers")
        headers_sent = True
    if time > 37 and headers_sent and not suffix_sent:
        horses = x.json()['horses']
        print(horses)
        horseMax = -1
        horseI = 0
        for i in range(16):
            if horseMax < horses[i]:
                horseMax = horses[i]
                horseI = i

        print(f"Fav horse {horseI}")
        #PETA THE HOSE IS HERE
        horse_bytes =f"{horseI:>2d}".encode()
        sock.sendall(horse_bytes+SUFFIX)
        print("sent suffix")
        suffix_sent = True
