# point P is for verifying of d
# Send message '0' and '1' respectively to get the corresponding signatures
# the corresponding signatures are values of sigs in solve.sage
# username = "Kuruwa"
# r and s are calculated by solve.sage
from pwn import *

r = remote('edu-ctf.csie.org', 42074)
print(r.recv())
r.sendline('1')
r.recv()
r.sendline('0')
print(r.recv())
r.sendline('1')
r.recv()
r.sendline('1')
print(r.recv())
r.sendline('2')
r.recv()
r.sendline(input('username'))
r.recv()
r.sendline(input('r'))
r.recv()
r.sendline(input('s'))
print(r.recv())