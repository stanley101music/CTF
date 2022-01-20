from pwn import *

r = remote('umbccd.io', 3000)

r.recv()
r.sendline('Admin')
r.recv()
r.sendline('goBigDawgs123')

r.recvuntil('Leaked ciphertext: ')
cipher = r.recvlineS().strip('\n')
x = ord('a') ^ ord('A') ^ int(cipher[:2], 16)

cipher = hex(x)[2:] + cipher[2:]

r.recv()
r.sendline(cipher)
print(r.recv())