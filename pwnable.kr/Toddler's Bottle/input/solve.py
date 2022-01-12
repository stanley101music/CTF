import os
import subprocess
import socket

# Stage 1
binary = '/home/input2/input'
argv = ['A'] * 100
argv[0] = binary
argv[ord('A')] = ""
argv[ord('B')] = "\x20\x0a\x0d"

# Stage2
r_in, w_in = os.pipe()
r_err, w_err = os.pipe()
os.write(w_in, "\x00\x0a\x00\xff")
os.write(w_err, "\x00\x0a\x02\xff")

# Stage 3
env = {"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"}

# Stage 4
with open("\x0a", 'w') as f:
    f.write("\x00\x00\x00\x00")
    f.close()

# Stage 5
s = socket.socket()
port = argv[ord('C')] = '10101'
subprocess.Popen(argv, stdin=r_in, stderr=r_err, env=env)
s.connect(("localhost", int(port)))
s.send("\xde\xad\xbe\xef")
print(s.recv(100))
s.close()
# ls -n /home/input2/flag flag